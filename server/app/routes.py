from . import app
import uuid
import json
import copy
import random
import math
from flask import Flask, make_response, jsonify, request
from app.initFirestore import db

from  story.scene import Story
from  story.story import mh370_crash
from data import data

# initializing the storyline
plane_crash = Story()
plane_crash.serialize_story(mh370_crash)

model = data.trainNewModel()

# helper method for .index method
def safeIndex(lsd, e, start=0, end=-1):
    if end==-1:
        end = len(lsd)
    return lsd.index(e, start, end) if e in lsd[start:end] else -1

# helper method for find the lasst occurrence of the element e
def lastSafeIndex(lsd, e):
    lst = copy.deepcopy(lsd)
    lst.reverse()
    index = safeIndex(lst,e)
    # print(f"rev. index: {index}")
    return (len(lst) - index - 1) if index != -1 else -1

def flipBiased(index, p):
    return index if random.random() < p else 1-index

# firestore collection
games_collection = db.collection('game_played')
hints_taken = db.collection('hints_taken')

@app.route('/')
@app.route('/api')
def index():
    return "Welcome to the flask API"

'''
creating new game
'''
@app.route('/api/create_game', methods=['GET','POST'])
def create_game():
    game_id = uuid.uuid4()

    print(model)
    plane_crash.serialize_story(mh370_crash)
    # pushing start scene
    
    plane_crash.refreshGame()
    
    # backend dataset
    dataset = { 'game_id' : game_id.hex }
    forks = plane_crash.getAllForkScenes() + ['dead_or_alive']

    # recording each decision as index, default to -1
    for fork in forks:
        dataset[fork] = -1

    # storing path so far
    dataset['path'] = [ele.dictify() for ele in plane_crash.getPath()]
    dataset['mood'] = 0.33

    payload = { 
        'game_id' : game_id.hex, 
        'story_so_far': plane_crash.getStorySoFar(),
        'choices': [(choice[0],choice[1].dictify()) for choice in plane_crash.getCurrChoices()],
    }

    games_collection.document(game_id.hex).set(dataset)
    return make_response(payload, 200)

'''
posting game updates as new choices made by the user
'''
@app.route('/api/game/<string:game_id>', methods=['PATCH'])
def game_update(game_id):

    game_doc = games_collection.document(game_id)
    game_ref = game_doc.get()

    # if such a game exists
    if game_ref.exists:
        game_status = game_ref.to_dict()
        data = request.json

        # add to path
        plane_crash.makePath(game_status['path'])
        current_scene = plane_crash.getPath()[-1]

        # getting an index for the choice from the original graph if valid
        choice_index = plane_crash.isValidChoice(data["choice_made"])

        if choice_index != -1:
            game_status['path'] = [ele.dictify() for ele in plane_crash.getPath()]
            if game_status.get(current_scene.title,None):
                game_status[current_scene.title] = choice_index
            game_status['mood'] = data['mood']
            game_doc.update(game_status)

            hint_selection = hints_taken.where('choice', '==', current_scene.title).stream()
            hint_id = ""
            hint_dict = {}
            for doc in hint_selection:
                # print(f'{doc.id} => {doc.to_dict()}')
                hint_id, hint_dict = doc.id, doc.to_dict()

            if hint_dict:
                if data['hint_taken']:
                    hint_dict['taken'] = hint_dict['taken'] + 1
                elif data['hint_agreed_with'] and not data['hint_taken']:
                    return make_response("ERROR: something goofy is happening with hint selection", 500)
                if data['hint_agreed_with']:
                        hint_dict['agreed_with'] = hint_dict['agreed_with'] + 1

                print(hint_dict)
                hints_taken.document(hint_id).update(hint_dict)

            print(data)

            return make_response("SUCCESS: game updated", 200)
        else:
            return make_response("ERROR: invalid choice", 403)

    return make_response("ERROR: can't load the game", 404)

@app.route('/api/game/<string:game_id>', methods=['GET'])
def get_update(game_id):

    game_doc = games_collection.document(game_id)
    game_ref = game_doc.get()
    
    # if such a game exists
    if game_ref.exists:
        game_status = game_ref.to_dict()

        # print(game_status)
        
        # look for current path
        path = plane_crash.makePath(game_status['path'])

        # testing 
        # plane_crash.pushToPathTag('alarm')
        # plane_crash.pushToPathTag('airport_arrival')
        # plane_crash.pushToPathTag('starbucks')
        # plane_crash.pushToPathTag('board_flight')
        # plane_crash.pushToPathTag('watch_her')
        # plane_crash.pushToPathTag('get_coffee')

        dead_or_alive = plane_crash.isGameOver()
        current_title = plane_crash.getCurrentTitle()
        nextChoices = []
        ref_dict = { 0: "dead", 1: "alive"}
        if dead_or_alive == -1:
            nextChoices = [(choice[0],choice[1].dictify()) for choice in plane_crash.getCurrChoices()]
        else:
            nextChoices = [(dead_or_alive, ref_dict[dead_or_alive])]
            game_status['dead_or_alive'] = dead_or_alive
            game_doc.update(game_status)

        non_features = ['game_id','dead_or_alive','path','mood']
        features_set = copy.deepcopy(game_status)
        for nf in non_features:
            features_set.pop(nf)
        # print(features_set)

        survival_chance = 0.0

        # getting survival current chance 
        current_status = data.getChoiceVector(features_set)
        print(current_status)
        lastChoiceIndex = max(lastSafeIndex(current_status,0),lastSafeIndex(current_status,1))
        # print(f"dead:{dead_or_alive}")
        # print(f"last found: {lastChoiceIndex}")

        if lastChoiceIndex != -1:
            if dead_or_alive != -1:
                survival_chance = dead_or_alive
            else:
                last_choice = current_status[lastChoiceIndex]
                current_status[lastChoiceIndex] = -1
                last_choice_title = 'airport_arrival'

                for k,v in data.FEATURE_IDX.items():
                    if v == lastChoiceIndex:
                        last_choice_title = k

                last_prediction = data.getPrediction(current_status, last_choice_title, model)
                # print(last_prediction)

                survival_chance = last_prediction[str(last_choice)][0][1]

        print(f"Survival: {survival_chance}")

        best_option = -1
        trust = 0.0

        model_hint = "sorry bois, no hint"
        
        if len(nextChoices) > 1:
            features_vector = data.getChoiceVector(features_set)
            prediction_vector = data.getPrediction(features_vector, current_title, model)
            print(prediction_vector)

            best_chance = -1
            for k, v in prediction_vector.items():
                if v[0][1] > best_chance:
                    best_chance = v[0][1]
                    best_option = int(k)
            
            
            if best_option != -1:
                best_option = flipBiased(best_option,0.02**(math.pow(game_status['mood'],2)))

            if best_option == 0 or best_option == 1:
                model_hint = {}
                model_hint['choice'] = nextChoices[best_option][1]['title']
                model_hint['hint'] = prediction_vector[str(best_option)][1]

            # print(model_hint)

            # get hints data from firestore for trust %
            hint_selection = hints_taken.where('choice', '==', current_title).stream()
            hint_id = ""
            hint_dict = {}
            for doc in hint_selection:
                # print(f'{doc.id} => {doc.to_dict()}')
                hint_id, hint_dict = doc.id, doc.to_dict()

            
            if hint_dict:
                trust = hint_dict['agreed_with'] / hint_dict['taken']
            
        print(f"trust: {trust}")

        payload = { 
            'game_id' : game_id, 
            'story_so_far': plane_crash.getStorySoFar(),
            'choices': nextChoices,
            'hint': model_hint,
            'survival_chance': survival_chance,
            'trust': trust,
            'mood': game_status['mood']
        }

        if best_option == -1:
            payload['hint'] = []


        return make_response(payload, 200)

    return make_response("ERROR: can't load the game", 404)


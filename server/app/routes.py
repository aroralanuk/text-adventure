from . import app
import uuid
import json
from flask import Flask, make_response, jsonify, request
from app.initFirestore import db

from  story.scene import Story
from  story.story import mh370_crash

# initializing the storyline
plane_crash = Story()
plane_crash.serialize_story(mh370_crash)


# firestore collection
games_collection = db.collection('game_played')

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

        # testing 
        # data = { 'choice_made': 'alarm'}

        # getting an index for the choice from the original graph if valid
        choice_index = plane_crash.isValidChoice(data["choice_made"])

        if choice_index != -1:
            game_status['path'] = [ele.dictify() for ele in plane_crash.getPath()]
            if game_status.get(current_scene.title,None):
                game_status[current_scene.title] = choice_index
            game_doc.update(game_status)
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
        nextChoices = []
        ref_dict = { 0: "dead", 1: "alive"}
        if dead_or_alive == -1:
            nextChoices = [(choice[0],choice[1].dictify()) for choice in plane_crash.getCurrChoices()]
        else:
            nextChoices = [(dead_or_alive, ref_dict[dead_or_alive])]

        payload = { 
            'game_id' : game_id, 
            'story_so_far': plane_crash.getStorySoFar(),
            'choices': nextChoices
        }

        return make_response(payload, 200)

    return make_response("ERROR: can't load the game", 404)


from . import app
import uuid
import json
from flask import Flask, make_response, jsonify

from  story.scene import Story
from  story.story import mh370_crash

plane_crash = Story()
plane_crash.serialize_story(mh370_crash)


@app.route('/')
@app.route('/api')
def index():
    return "Hello, World!"

@app.route('/api/create_game', methods=['GET'])
def create_game():
    game_id = uuid.uuid4()
    headers = {"Content-Type": "application/json"}
    # print(plane_crash.start)
    plane_crash.pushToPath(plane_crash.getStart())
    dataset = { 'game_id' : game_id }
    forks = plane_crash.getAllForkScenes() + ['dead_or_alive']
    for fork in forks:
        dataset[fork] = -1

    core_payload = dataset
    core_payload['path'] = [ele.dictify() for ele in plane_crash.getPath()]

    payload = { 
        'game_id' : game_id, 
        'story_so_far': plane_crash.getStorySoFar(),
        'choices': [choice[1].dictify() for choice in plane_crash.getCurrChoices()],
    }
    print(payload)
    return make_response(core_payload, 200)

# @app.route('/api/game/<string:game_id>', methods=['GET','POST'])
# def 





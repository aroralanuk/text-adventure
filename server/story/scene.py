import sys, os
import time
import random

# scene class for each scene in the story
class Scene(object):
    def __init__(self, title, desc):
        self.title = title
        self.desc = desc

    # formatting for json frendliness
    def dictify(self):
        return {
            'title': self.title,
            'desc': self.desc
        }

    # overwritting == method for ease of comparsion
    def __eq__(self, other):
        if type(other) is type(self):
            return self.title == other.title 
        else:
            return False
    
    # scenes are unique
    def __hash__(self):
        return hash((self.title))

    def __str__(self):
        return ('Scene(' + self.title + ')')

    __repr__ = __str__



# story as a graph of the scenes
# self.path holding the list of scenes visited
class Story(object):
    def __init__(self, graph_dict=None):
        if graph_dict == None:
            self.graph_dict = {}
            self.start = None
            self.path = []
        else:
            self.graph_dict = graph_dict

    def getStart(self):
        return self.start

    def getCurrentTitle(self):
        if len(self.path) != 0:
            return self.path[-1].title

    # for finding the last fork for the ML algorithm
    def getLastChoiceTitle(self):
        path_len = len(self.path)
        if path_len != 0:
            for i in range(path_len,0):
                print(self.path[i])
                if len(self.graph_dict[self.path[i]]) > 1:
                    return self.path[i].title

    def getChoices(self, current_scene):
        for keys in self.graph_dict:
            if keys.title == current_scene.title:
                return self.graph_dict[keys]
        return []

    def getCurrChoices(self):
        if len(self.path) != 0:
            return self.getChoices(self.path[-1])
        else:
            raise RuntimeError('Can\'t get choices for null scene')

    # add choices to the graph
    def addChoice(self, curr, choice):
        if self.graph_dict.get(curr, -1) == -1:
            raise ValueError('Out scene not found')
        else:
            self.graph_dict[curr].append(choice)
            self.graph_dict[choice[1]] = []

    def addStart(self,scene):
        self.start = scene

    def getPath(self):
        return self.path

    # storing choices made as an extension to the path
    def pushToPath(self, scene):
        if isinstance(scene, Scene):
            self.path.append(scene)
        else:
            raise ValueError('Path needs a valid scene to be pushed')

    def refreshGame(self):
        self.path = []
        self.pushToPath(self.start)


    def pushToPathTag(self, scene_tag):
        for key in self.graph_dict:
            if key.title == scene_tag:
                self.pushToPath(key)

    # restoring Story object from the path provided
    def makePath(self,jsonPath):
        self.path = []
        for jsonScene in jsonPath:
            currScene = Scene(jsonScene['title'], jsonScene['desc'])
            self.pushToPath(currScene)

    # return 0 for dead or 1 for alive if game over
    def isGameOver(self):
        choices = self.getCurrChoices()
        if choices[0] == 1 or choices[0] == 0:
            return choices[0]
        else:
            return -1

    # check for valid choice at the current scene
    def isValidChoice(self,choice):
        if not self.path and self.isGameOver() != -1:
            return False
        curr = self.graph_dict[self.path[-1]]
        choice_len = len(curr)
        for i in range(choice_len):
            validChoice = curr[i]
            if choice == validChoice[1].title:
                self.pushToPath(validChoice[1])
                return i
        return -1

    # getting all scenes with > 1 choices for the ML algorithm
    def getAllForkScenes(self):
        scenes_text = []
        for scene in self.graph_dict:
            if len(self.graph_dict[scene]) > 1:
                scenes_text.append(scene.title)
        return scenes_text

    # getting display text for the front-end
    def getStorySoFar(self):
        storyline = []
        prev = None
        for scene in self.path:
            if prev:
                for choice in self.graph_dict[prev]:
                    if choice[1] == scene:
                        storyline.append(['> ' + choice[0]])
            storyline.append([scene.desc])
            prev = scene
        return storyline


    # converting story from json object in story.py to a story object using DFS
    def serialize_story(self, story):
        
        def helper(key):
            scene = Scene(key,'\n'.join(story[key]['text']))
            if self.graph_dict.get(scene,0) == 0:
                self.graph_dict[scene] = []

            if story[key]['choices'] == 0:
                self.graph_dict[scene].append(0)
                return scene
            elif story[key]['choices'] == 1:
                self.graph_dict[scene].append(1)
                return scene
            choices = [x for x in story[key]['choices']]

            for choice in choices:
                recurse = helper(choice[1])
                if recurse not in self.graph_dict[scene]:
                    self.graph_dict[scene].append((choice[0],recurse))
            return scene

        helper('start')
        self.clean_graph()
        game_start = Scene('start','\n'.join(story['start']['text']))
        self.addStart(game_start)

    # doubling of fork scenes removed
    def clean_graph(self):
        for scene in self.graph_dict:
            uniq = []
            for child in self.graph_dict[scene]:
                if child not in uniq:
                    uniq.append(child)
            self.graph_dict[scene] = uniq


            

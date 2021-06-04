import sys, os
import time
import random

class Scene(object):
    def __init__(self, title, desc):
        self.title = title
        self.desc = desc

    def dictify(self):
        return {
            'title': self.title,
            'desc': self.desc
        }

    def __eq__(self, other):
        if type(other) is type(self):
            return self.title == other.title 
        else:
            return False
    
    def __hash__(self):
        return hash((self.title))

    def __str__(self):
        return ('Scene(' + self.title + ')')

    __repr__ = __str__



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

    # def getChoiceIndex(self, curr, choice):
    #     if self.graph_dict.get(curr,False):
    #         return self.graph_dict[curr]

    def getCurrChoices(self):
        if len(self.path) != 0:
            return self.getChoices(self.path[-1])
        else:
            raise RuntimeError('Can\'t get choices for null scene')

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


    def makePath(self,jsonPath):
        self.path = []
        for jsonScene in jsonPath:
            currScene = Scene(jsonScene['title'], jsonScene['desc'])
            self.pushToPath(currScene)

    def isGameOver(self):
        choices = self.getCurrChoices()
        # print(f"vfsvfsvsvdd:{choices}")
        if choices[0] == 1 or choices[0] == 0:
            return choices[0]
        else:
            return -1

    def isValidChoice(self,choice):
        # print(self.path)
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

    def getAllForkScenes(self):
        scenes_text = []
        for scene in self.graph_dict:
            if len(self.graph_dict[scene]) > 1:
                scenes_text.append(scene.title)
        return scenes_text

    def getStorySoFar(self):
        storyline = []
        prev = None
        for scene in self.path:
            if prev:
                # print(self.path)
                for choice in self.graph_dict[prev]:
                    if choice[1] == scene:
                        storyline.append(['> ' + choice[0]])
            storyline.append([scene.desc])
            prev = scene
        return storyline



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
            # print(f"graph: {self.graph_dict}")
            # print(f"curr: {scene} and choices: {choices}\n")

            for choice in choices:
                recurse = helper(choice[1])
                if recurse not in self.graph_dict[scene]:
                    self.graph_dict[scene].append((choice[0],recurse))
            return scene

        helper('start')
        self.clean_graph()
        game_start = Scene('start','\n'.join(story['start']['text']))
        self.addStart(game_start)
        # print(self.graph_dict)

    def clean_graph(self):
        for scene in self.graph_dict:
            uniq = []
            for child in self.graph_dict[scene]:
                if child not in uniq:
                    uniq.append(child)
            self.graph_dict[scene] = uniq


    def start_game(self,story):
        pass

            

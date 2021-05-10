import sys, os
import time
import random

def type(text):
    """Slowly types a line to the console.
    Args:
        text (str): A line of text.
    """
    # How quickly the text appears in the console.
    typing_speed = 100

    # Slowly prints each character in the text out.
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(random.random() * 10.0 / typing_speed )


def display_page_text(lines):
    """Displays all the lines of text and prompts the user for input.
    Args:
        lines (list): [description]
    """
    for line in lines:
        # Slowly types the line.
       type(line + os.linesep)

       # Randomly waits for a time between 0s and 1s.
       time.sleep(0.1)
    print()

class Scene(object):
    def __init__(self, title, desc):
        self.title = title
        self.desc = desc

    def dictify(self):
        return {
            'title': self.title,
            'desc': self.desc
        }

    # def __eq__(self, other):
    #     return self.title == other.title 

    def __str__(self):
        return (self.title)

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

    def getChoices(self, current_scene):
        for keys in self.graph_dict:
            if keys.title == current_scene.title:
                return self.graph_dict[keys]
        return []

    def getCurrChoices(self):
        print(self.getChoices(self.path[-1]))
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
                for choice in self.graph_dict[prev]:
                    if choice[1] == scene:
                        storyline.append(['>' + choice[0]])
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
                self.graph_dict[scene].append((choice[0],helper(choice[1])))
            return scene

        helper('start')
        game_start = Scene('start','\n'.join(story['start']['text']))
        self.addStart(game_start)
        # print(self.graph_dict)


    def start_game(self,story):
        pass

    # def play(self, story):
    #     self.serialize_story(story)
    #     curr_scene = self.start  
    #     while curr_scene != None:    
    #         scene = story.get(curr_scene, None)
    #         if scene == None:
    #             curr_scene = None
    #             break
  
    #     display_page_text(scene['text'])
        
    #     if len(page['Options']) == 0:      
    #         curr_page = None      
    #         break     
        
    #     curr_page = get_response(page['Options'])
            

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

    def __str__(self):
        return (self.title + " | \"" + self.desc + "\".")


class Story(object):
    def __init__(self, graph_dict=None):
        if graph_dict == None:
            self.graph_dict = {}
            self.start = None
        else:
            self.graph_dict = graph_dict

    def getChoices(self, current_scene):
        return graph_dict.get(current_scene, {})

    def addChoice(self, curr, choice):

        if len(graph_dict.get(curr, -1)) == -1:
            raise ValueError('Out scene not found')
        else:
            graph_dict[curr].append(choice)
            graph_dict[choice[1]] = []

    def addStart(self,scene):
        graph_dict[scene] = []
        self.start = scene

    def serialize_story(self,story):
        start_scene = story.get('start',-1)
        if start_scene == -1:
            raise ValueError('Every story needs a \"start\" labeled scene')
        self.addStart(Scene('start','\n'.join(start_scene['text'])))
        for choice in start_scene['choices']:
            self.addChoice('start',choice)

        for scene in story.keys():
            if scene != 'start':
                for choice in story[scene]['choices']:
                    self.addChoice(story[scene],choice)

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
            

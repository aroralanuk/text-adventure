#database imports
#import firebase_admin
#from firebase_admin import credentials, db, initialize_app, firestore
import sys
import math
import random
sys.path.append('../')

#model training imports
import pandas as pd
import sklearn # import scikit-learn
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import numpy as np

from app.initFirestore import db

import pandas as pd

df = pd.read_csv('../language/hints.csv')

FEATURE_IDX = {
    "airport_arrival": 0,     #DTF or Starbucks
    "starbucks": 1,           #Regular coffee or 3 shots
    "board_flight": 2,        #sleep or watch her
    "watch_her": 3,           #keep watching or get coffee
    "get_coffee": 4,          #walk into cockpit or return to seat
    "walk_into_cockpit": 5,   #help captain or help first officer
    "return_seat": 6,         #call attendant or settle in seat
}


FEATURES_SIZE = len(FEATURE_IDX)
arrivalHint1 = "ARGHH I be starvin. Din Tai Fung sounds good, i wants t' go thar"
arrivalHint2 = "ARGHH I be parched. Lets get some black brew at that there Starbucks"
starbucksHint1 = "Don't let 'em take yer doubloons, a normal brew will do ye just fine"
starbucksHint2 = "Those shots oughta kick yer hangover, worth yer doubloons"
flightHint1 = "Kick yer feet up and gets t' restin, me eyes be heavy"
flightHint2 = "Turn yer screen on, I wants t' watch th' movie"
herHint1 = "ARGH screw yer brew, I wants t' see the end"
herHint2 = "That there movie is puttin' me to sleep, get yer black brew to last us this ride"
coffeeHint1 = "A pirate never turns down a fight, get yer booty in there!"
coffeeHint2 = "This pirate doesn't fight with stomach issues, get back to yer seat"
cockpitHint1 = "Mutiny! Help yer Captain and make the scallywag walk the plank"
cockpitHint2 = "Mutiny! Help yer crew and take down the rotten Captain of the ship"
seatHint1 = "Get some help for yer captain, call the attendant"
seatHint2 = "Not our fight, get yer rest and settle down"


HINTS = {
    "airport_arrival": (arrivalHint1, arrivalHint2),
    "starbucks": (starbucksHint1, starbucksHint2),
    "board_flight": (flightHint1, flightHint2),
    "watch_her": (herHint1, herHint2),
    "get_coffee": (coffeeHint1, coffeeHint2),
    "walk_into_cockpit": (cockpitHint1, cockpitHint2),
    "return_seat": (seatHint1, seatHint2),
}

# generating
indexy = 0
for k,v in FEATURE_IDX.items():
    pref_index = round(random.random() * 100)
    HINTS[k] = (df.loc[indexy*100 + pref_index,'hint'],df.loc[indexy*100 + pref_index + 100,'hint'])
    indexy = indexy + 2


def metrics(y_true, y_pred):
    print('Confusion matrix:\n', confusion_matrix(y_true, y_pred))
    print('\nReport:\n', classification_report(y_true, y_pred))

def getChoiceVector(choiceDict):
    vector = [-1]*FEATURES_SIZE
    for choice in choiceDict.keys():
        if FEATURE_IDX.get(choice, None) != None:
            vector[FEATURE_IDX[choice]] = choiceDict[choice]
    return vector

def getPrediction(currentChoices, currentScene, model):
    returnDict = {}

    currentChoices = np.array(currentChoices)
    #get the prediction for choice 0
    currentChoices[FEATURE_IDX[currentScene]] = 0
    returnDict["0"] = (model.predict_proba(currentChoices.reshape(1, -1))[0], HINTS[currentScene][0])
    #get the prediction for choice 1
    currentChoices[FEATURE_IDX[currentScene]] = 1
    returnDict["1"] = (model.predict_proba(currentChoices.reshape(1, -1))[0], HINTS[currentScene][1])
    return returnDict

def trainNewModel():
    #import data
    docs = db.collection('game_played').where('dead_or_alive', '!=', -1).stream()
    full_df = pd.DataFrame()
    for doc in docs:
        whatType = doc.to_dict()
        full_df = full_df.append(doc.to_dict(), ignore_index=True)

    features_and_label = ['airport_arrival', 'starbucks', 'board_flight', 'watch_her', 'get_coffee', 'walk_into_cockpit', 'return_seat', 'dead_or_alive']#decide if we need label here

    chosen_features = ['airport_arrival', 'starbucks', 'board_flight', 'watch_her', 'get_coffee', 'walk_into_cockpit', 'return_seat']

    #take only needed features and label to predict
    chosen_df = full_df[features_and_label]
    expanded_df = pd.DataFrame()

    for playthroughIdx in range(len(chosen_df)):
        playthrough = chosen_df.loc[playthroughIdx]
        for choice in range(len(playthrough)-2,0,-1):
            if (playthrough[choice] != -1):
                playthrough[choice] = -1
                expanded_df = expanded_df.append(playthrough, ignore_index=True)

    #split processed data into features and labels
    features = expanded_df[chosen_features]
    labels = expanded_df['dead_or_alive']
    model = RandomForestClassifier().fit(features, labels)
    print(pd)
    return model

# model = trainNewModel()
# array = np.array([0, -1, -1, -1, -1, -1, -1])
# print(getPrediction(array, "board_flight", model))

'''
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)

#gathering fully played game documents into docs
db = firestore.client()
docs = db.collection('game_played').where('dead_or_alive', '!=', -1).stream()

# #chronological progression of choices
# featureIdx = {
#   "airport_arrival": 0,     #DTF or Starbucks
#   "starbucks": 1,           #Regular coffee or 3 shots
#   "board_flight": 2,        #sleep or watch her
#   "watch_her": 3,           #keep watching or get coffee
#   "get_coffee": 4,          #walk into cockpit or return to seat
#   "walk_into_cockpit": 5,   #help captain or help first officer
#   "return_seat": 6,         #call attendant or settle in seat
# }

#converting documents to a dataframe to hold database training data
full_df = pd.DataFrame()
for doc in docs:
    whatType = doc.to_dict()
    full_df = full_df.append(doc.to_dict(), ignore_index=True)

features_and_label = ['airport_arrival', 'starbucks', 'board_flight', 'watch_her', 'get_coffee', 'walk_into_cockpit', 'return_seat', 'dead_or_alive']#decide if we need label here

chosen_features = ['airport_arrival', 'starbucks', 'board_flight', 'watch_her', 'get_coffee', 'walk_into_cockpit', 'return_seat']

#take only needed features and label to predict
chosen_df = full_df[features_and_label]


#Now we need to break up each row into a vector for each choice
expanded_df = pd.DataFrame()

for playthroughIdx in range(len(chosen_df)):
    playthrough = chosen_df.loc[playthroughIdx]
    for choice in range(len(playthrough)-2,0,-1):
        if (playthrough[choice] != -1):
            playthrough[choice] = -1
            expanded_df = expanded_df.append(playthrough, ignore_index=True)



#split processed data into features and labels
features = expanded_df[chosen_features]
labels = expanded_df['dead_or_alive']


#getting percentage of win possibility from current playthrough
X_train, X_TEMP, y_train, y_TEMP = train_test_split(features, labels, test_size=0.30) 
X_validation, X_test, y_validation, y_test = train_test_split(X_TEMP, y_TEMP, test_size=0.50) 
#print(X_train.shape, X_validation.shape, X_test.shape)

#training the decision tree or forest of decision trees
#model = DecisionTreeClassifier().fit(X_train, y_train)
model = RandomForestClassifier().fit(features, labels)

#testing predictions
array = np.array([1, 0, 1, 1, 0, 1, -1])
hint = model.predict_proba(array.reshape(1, -1))
print(hint)

#y_pred = model.predict(X_validation) 
#metrics(y_validation, y_pred) 
'''

#database imports
import firebase_admin
from firebase_admin import credentials, db, initialize_app, firestore

#model training imports
import pandas as pd
import sklearn # import scikit-learn
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier
import numpy as np

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

#training the decision tree
model = DecisionTreeClassifier().fit(features, labels)

#testing predictions
array = np.array([1, 0, 1, 1, 1, -1, -1])
hint = model.predict(array.reshape(1, -1))
print(hint)
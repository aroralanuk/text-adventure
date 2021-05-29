#database imports
import firebase_admin
from firebase_admin import credentials, db, initialize_app, firestore

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

def metrics(y_true, y_pred):
    print('Confusion matrix:\n', confusion_matrix(y_true, y_pred))
    print('\nReport:\n', classification_report(y_true, y_pred))

def probabilityOfAWin(currentPlaythrough, data):
    numWins = len(data[(data['airport_arrival'] == currentPlaythrough[0]) & (data['starbucks'] == currentPlaythrough[1]) & (data['board_flight'] == currentPlaythrough[2]) & (data['watch_her'] == currentPlaythrough[3]) & (data['get_coffee'] == currentPlaythrough[4]) & (data['walk_into_cockpit'] == currentPlaythrough[5]) & (data['return_seat'] == currentPlaythrough[6]) & (data['dead_or_alive'] == 1)])
    return numWins/(len(data))


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

#print(probabilityOfAWin(np.array([1, 0, 1, 1, 0, 1, -1]), expanded_df))

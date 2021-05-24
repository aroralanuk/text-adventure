#database imports
import firebase_admin
from firebase_admin import credentials, db, initialize_app, firestore

#model training imports
import pandas as pd
import sklearn # import scikit-learn
from sklearn import preprocessing

cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)

#gathering fully played game documents into docs
db = firestore.client()
docs = db.collection('game_played').where('dead_or_alive', '!=', -1).stream()

#converting documents to a dataframe for training
full_df = pd.DataFrame()
for doc in docs:
    whatType = doc.to_dict()
    full_df = full_df.append(doc.to_dict(), ignore_index=True)


#chosen features decides which fork this model represents
chosen_features = ['starbucks', 'get_coffee']

chosen_df = full_df[chosen_features]
print(chosen_df.head())

enc = preprocessing.OneHotEncoder()
enc.fit(chosen_df) # fit the encoder to categories in our data 
one_hot = enc.transform(chosen_df) # transform data into one hot encoded sparse array format
# Finally, put the newly encoded sparse array back into a pandas dataframe so that we can use it

chosen_df_proc = pd.DataFrame(one_hot.toarray(), columns=enc.get_feature_names())
print(chosen_df_proc.head())

labels = full_df['dead_or_alive']

#maybe fill NaN here

#building the decision tree
from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier().fit(chosen_df_proc, labels) # first fit (train) the model
#hint = model.predict(currentRunData)
#Start of the data file
# here is where we will get the feature vectors, train the model, etc
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import initialize_app
from firebase_admin import firestore
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
docs = db.collection(u'game_played').where(u'dead_or_alive', u'!=', -1).stream()
for doc in docs:
    print(doc.to_dict()['game_id'])
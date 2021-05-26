import os
from firebase_admin import credentials, firestore, initialize_app

firestore_key = {
  "type": os.environ["TYPE"],
  "project_id": os.environ["PROJECT_ID"],
  "private_key_id": os.environ["PRIVATE_KEY_ID"],
  "private_key": os.environ["PRIVATE_KEY"].replace('\\n', '\n'),
  "client_email": os.environ["CLIENT_EMAIL"],
  "client_id": os.environ["CLIENT_ID"],
  "auth_uri": os.environ["AUTH_URI"],
  "token_uri": os.environ["TOKEN_URI"],
  "auth_provider_x509_cert_url": os.environ["AUTH_PROVIDER_X509_CERL_URL"],
  "client_x509_cert_url": os.environ["CLIENT_X509_CERT_URL"]
}

cred = credentials.Certificate(firestore_key)
default_app = initialize_app(cred)
db = firestore.client()
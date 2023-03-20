from google.cloud import firestore
from google.oauth2 import service_account
import json


# Authenticate to Firestore with the JSON account key.
key_dict = json.loads(st.secrets['textkey'])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)

# Create a reference to the Google post.
doc_ref = db.collection('master_data')
from google.cloud import firestore
from google.oauth2 import service_account
import json
import os
import pandas as pd

# Get the directory of the file with secret key and firestore information
secret_file = os.getcwd() + "/.streamlit/firestore-key.json"

# Authenticate to Firestore with the JSON account key.
with open(secret_file) as user_file:
  file_contents = user_file.read()

key_dict = json.loads(file_contents)
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)

# Obtain access to all collection names

collections = [c.id for c in db.collections()]
collections.remove("master_data")
feedback_dic = {}

# Iterate through each collection and obtain the feedback documents into a dataframe style dictionary

for collection in collections:
  collection_ref = db.collection(collection)

  # Checks if the collection is empty

  try:
    doc_ref = collection_ref.document("row0")
  except:
    print("No document in collection", collection)

  # Gets all the keys in the document

  all_keys = doc_ref.get().to_dict().keys()

  # Gets all the keys that contain the word "feedback" and removes the None values

  feedback_keys = [key if "feedback" in key else None for key in all_keys]
  feedback_keys = [key for key in feedback_keys if key is not None]

  # Creates a dictionary of arrays with the feedback keys as the keys and the feedback as the values

  feedback_documents = {}
  for document in collection_ref.stream():
    for key in feedback_keys:
      if key in feedback_documents:
        feedback_documents[key].append(document.to_dict()[key])
      else:
        feedback_documents[key] = [document.to_dict()[key]]

  # Adds the dictionary to the feedback dictionary

  feedback_dic[collection] = feedback_documents

print(feedback_dic)
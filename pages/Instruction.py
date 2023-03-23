import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json


# Authenticate to Firestore with the JSON account key.
key_dict = json.loads(st.secrets['textkey'])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)

# Create a reference to the Google post.
doc_ref = db.collection('master_data')

for doc in doc_ref.stream():
    data = doc.to_dict()
    event = data["form_name"]
    course_rating = data["course_rating"]
    instructor_rating = data["instructor_rating"]
    accessibility_rating = data["accessibility_rating"]
    navigation_rating = data["navigation_rating"]
    st.title(event)
    st.write("Course Rating: ", event)
    st.write("Instructor Rating: ", course_rating)


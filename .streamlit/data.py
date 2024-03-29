import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json
import pandas as pd

# Authenticate to Firestore with the JSON account key.
key_dict = json.loads(st.secrets['textkey'])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)

# Create a reference to the Google post.
doc_ref = db.collection('master_data')

# Create dictionary that will be used to create dataframe
data_dict = { "Form Name": [], "Timestamp": [], "Course Rating": [], 
"Guidelines Before": [], "Guidelines After": [], "Improvement Efforts": [], 
"Sharing Interest": [], "Instructor Rating": [], "Accessibility Rating": [], 
"Navigation Rating": [], "Current Profession": [], "Student Count": [], "Student Location": []}

# Iterate through every document in the collection and append each value to the dictionary
for doc in doc_ref.stream():
    data = doc.to_dict()
    data_dict["Form Name"].append(data["form_name"])
    data_dict["Timestamp"].append(data["timestamp"])
    data_dict["Course Rating"].append(data["course_rating"])
    data_dict["Guidelines Before"].append(data["guidelines_before"])
    data_dict["Guidelines After"].append(data["guidelines_after"])
    data_dict["Improvement Efforts"].append(data["improvement_efforts"])
    data_dict["Sharing Interest"].append(data["sharing_interest"])
    data_dict["Instructor Rating"].append(data["instructor_rating"])
    data_dict["Accessibility Rating"].append(data["accessibility_rating"])
    data_dict["Navigation Rating"].append(data["navigation_rating"])
    data_dict["Current Profession"].append(data["current_profession"])
    data_dict["Student Count"].append(data["student_count"])
    data_dict["Student Location"].append(data["student_location"])

# for i in data_dict:
#     print(i)
#     print(len(data_dict[i]))

final_data = pd.DataFrame(data_dict)
print(final_data)

if "master_data" not in st.session_state:
    st.session_state["master_data"] = final_data
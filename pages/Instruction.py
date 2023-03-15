import streamlit as st
from google.cloud import firestore
import json


key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds, project="eenc")

doc_ref = db.collection("master_data").document("row1")

doc = doc_ref.get()

st.write("Test accessibility_rating:" + doc.accessibility_rating)

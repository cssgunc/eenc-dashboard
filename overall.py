import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
from bokeh.models.widgets import Div
from google.cloud import firestore
from google.oauth2 import service_account
import json

@st.cache_resource # Caches the connection to the database
def get_database(key_data):
    creds = service_account.Credentials.from_service_account_info(key_data)
    db = firestore.Client(credentials=creds)
    return db

@st.cache_data(ttl = 1800) # Caches the updates and forces an update every 30 minutes
def get_data(_db):
    # Create a reference to the Google post.
    doc_ref = _db.collection('master_data')

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

    return pd.DataFrame(data_dict)


# Set page title and favicon
st.set_page_config(page_title="Homepage", page_icon="assets/EENC-logo.png", layout="wide")

# Authenticate to Firestore with the JSON account key.
key_dict = json.loads(st.secrets['textkey'])
st.session_state["database_connection"] = get_database(key_dict)
st.session_state["master_data"] = get_data(st.session_state["database_connection"])

# Load the data
# Data from Streamlit state
data = st.session_state["master_data"]

# replace 'N/A' with NaN
data = data.replace('N/A', float('nan'))

# logo
st.image("assets/EENC-logo.png", width=100)

st.title("Welcome to the EENC dashboard")
st.markdown("This page displays overall information for the EENC courses. Use the filter on the left to customize the results.")
st.markdown('---')

primary_color = "#195E4C"
secondary_color = "#3C9E8D"
text_color = "#6D7183"

# Sidebar
st.sidebar.title("Filters")
form_name = st.sidebar.selectbox("Form Name", ['All'] + sorted(data['Form Name'].unique()))
st.sidebar.caption("Need more help? Refer to our documentation here")

# Filter the data
if form_name != 'All':
    data = data[data['Form Name'] == form_name]


# Check that this translates over guidelines qualitative values to quantitative
guidelines_before = data['Guidelines Before']
guidelines_after = data['Guidelines After']

c1, c2 = st.columns((7,3))
with c1:
    st.header("Demographics")
with c2:
    guidelines_button = st.button("More details about demographics")
    if guidelines_button:
        switch_page("Demographics")

col2, col3, col4 = st.columns(3)

col2.metric("No. of Attendees", str(len(data)))
profession_count = data['Current Profession'].value_counts()
max_attendees = profession_count.max()
highest_attendees_profession = profession_count[profession_count == max_attendees].index.tolist()
highest_attendees_profession_str = ", ".join(highest_attendees_profession)
col3.metric("Highest Attendee Profession", highest_attendees_profession_str)


c1, c2 = st.columns((7,3))
with c1:
    st.header("Improvement & Guidelines")
with c2:
    guidelines_button = st.button("More details about guidelines")
    if guidelines_button:
        switch_page("Guidelines")

col2, col3, col4 = st.columns(3)

col2.metric("Avg. Improvement Efforts", round(data["Improvement Efforts"].mean(), 2))
col3.metric("Avg. Guidelines Before", round(guidelines_before.mean(),2))
col4.metric("Avg. Guidelines After", round(guidelines_after.mean(),2))

st.info("All average scales are calculated out of 5.")

# include third metric for  growth in guidelines? or maybe one for avg. guidelines before, avg. guidelines after, and avg. growth
st.markdown('   ')


c1, c2 = st.columns((7,3))
with c1:
    st.header("Ratings")
with c2:
    ratings_button = st.button("More details about ratings")
    if ratings_button:
        switch_page("ratings")


# total number of respondents, course rating, average ratings
# put some stuff that links to mel's rating page
col1, col2, col3, col4 = st.columns(4)
col1.metric("Avg. Course", round(data['Course Rating'].mean(), 2))
col2.metric("Avg. Instructor", round(data['Instructor Rating'].mean(), 2))
col3.metric("Avg. Accessibility", round(data['Accessibility Rating'].mean(), 2))
col4.metric("Avg. Navigation", round(data['Navigation Rating'].mean(), 2))

st.info("All average ratings are calculated out of 5.")

st.markdown('   ')
st.markdown('   ')


# st.header("\nGraphs & Trends")
# # Average knowledge gain, most popular classes, trends over time


# st.markdown('### Guidelines Before & After')

# # Get value counts for "Guidelines Before"
# value_counts_before = data['Guidelines Before'].value_counts().reset_index()
# value_counts_before.columns = ['Guidelines', 'Count']

# labels_order_before = ["Very Low", "Low", "Average", "High", "Very High"]
# labels_order_after = ["Average", "High", "Very High"]
# bar_color_before = '#4AE19C'
# bar_color_after = secondary_color


# # Create the first bar chart
# fig = px.bar(value_counts_before, x='Guidelines', y='Count', text='Count',
#              category_orders={'Guidelines': labels_order_before},
#              color_discrete_sequence=[bar_color_before])

# # Update the chart title and axis labels
# fig.update_layout(
#                   xaxis_title='Guidelines',
#                   yaxis_title='Count')

# # Get value counts for "Guidelines After"
# value_counts_after = data['Guidelines After'].value_counts().reset_index()
# value_counts_after.columns = ['Guidelines', 'Count']

# # Create the second bar chart
# fig.add_trace(go.Bar(x=value_counts_after['Guidelines'],
#                      y=value_counts_after['Count'],
#                      name='Guidelines After',
#                      marker_color=bar_color_after))

# # Update the trace labels
# fig.update_traces(texttemplate='%{y}', textposition='auto')

# fig.update_layout(legend=dict(
#     orientation='v',
#     xanchor='right',
#     itemsizing='constant',
#     itemwidth=50,
#     bgcolor='rgba(255, 255, 255, 0.5)'),
# )

# # Display the chart
# st.plotly_chart(fig)



# st.markdown('   ')

# st.markdown('### On a scale of 1 to 5, how interested are you in sharing what you learned with others?')

# value_counts = data['Sharing Interest'].value_counts().reset_index()
# value_counts.columns = ['Sharing Interest', 'Count']

# # Define the order of the labels
# labels_order = ["Average", "High", "Very High"]

# bar_color = secondary_color

# fig = px.bar(value_counts, x='Sharing Interest', y='Count', text='Count',
#              category_orders={'Sharing Interest': labels_order},
#              color_discrete_sequence=[bar_color])
# fig.update_traces(texttemplate='%{text}', textposition='auto')

# fig.update_layout(xaxis_title='Sharing Interest',
#                   yaxis_title='Count')

# st.plotly_chart(fig)


# Add CSS to customize text colors
st.markdown(f"""
    <style>
        div.css-edivx2.e16fv1kl3 {{
            color: {secondary_color};
        }}
        p {{
            color: {text_color};
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: {primary_color};
        }}
        button {{
            float: right;
        }}
        a {{
            color: {secondary_color};
        }}
    </style>
""", unsafe_allow_html=True)

# Hide footer and menu
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)
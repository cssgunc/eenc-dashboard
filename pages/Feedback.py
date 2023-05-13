import pandas as pd
import streamlit as st
import random

# Set page title and favicon
st.set_page_config(page_title="Feedback",
                   page_icon="assets/EENC-logo.png", layout="wide")

# Data from Streamlit state
data = st.session_state["master_data"]
feedback_data = st.session_state["feedback_data"]

# replace 'N/A' with NaN
data = data.replace('N/A', float('nan'))

# Set constants for theme colors
primary_color = "#195E4C"
secondary_color = "#3C9E8D"
text_color = "#6D7183"

# Sidebar
st.sidebar.title("Filter")
unique_form_names = sorted(data['Form Name'].unique())
cleaned_form_names = [name.replace('_', ' ').title() for name in unique_form_names]

options = ["All"] + cleaned_form_names

form_name = st.sidebar.selectbox("Select Form Name", options, options.index(st.session_state["formname"]))

st.sidebar.caption("Need more help? Refer to our documentation here")

if form_name != 'All':
    formatted_form_name = f"{form_name.lower().replace(' ', '_')}"
    data = data[data['Form Name'] == formatted_form_name]
    feedback_data = feedback_data[formatted_form_name]
    st.session_state["formname"] = form_name
else:
    feedback_data = {k: v for d in feedback_data.values() for k, v in d.items()}
    st.session_state["formname"] = "All"
# Logo
st.image("assets/EENC-logo.png", width=100)

# Main content
st.title("EENC Feedback")
st.write("This page displays every feedback participants have in all workshops from EENC. Use the filter on the left to customize the results.")
st.markdown('  ')

def generate_feedback_list(feedback_type):
    if feedback_type in feedback_data and len(feedback_data[feedback_type]) > 0:
        feedback_list = [feedback for feedback in feedback_data[feedback_type] if feedback.lower() != "n/a"]
        if len(feedback_list) > 0:
            title = " ".join([word.capitalize() for word in feedback_type.split("_")])
            return (title, feedback_list)
        else:
            return None

feedback_tabs = []
feedback_types = ["general_feedback", "instructor_feedback", "accessibility_feedback", 
                  "rating_feedback", "accessibility_feedback", "structure_feedback", 
                  "topics_feedback", "activity_removal_feedback"]
for feedback_type in feedback_types:
    feedback = generate_feedback_list(feedback_type)
    if feedback is not None:
        feedback_tabs.append(feedback)

if len(feedback_tabs) > 0:
    tabs = st.tabs([feedback[0] for feedback in feedback_tabs])
    for feedback, tab in zip(feedback_tabs, tabs):
        with tab:
            if len(feedback[1]) > 0:
                feedback_str = "\n".join([f"- {f}\n" if f else "" for f in feedback[1]])
                st.info(f"\n\n{feedback_str}")
            else:
                st.info(f"No {feedback[0]} found.")


# Add CSS to customize text colors
st.markdown(f"""
    <style>
        div.css-edivx2.e16fv1kl3 {{
            color: {secondary_color};
        }}
        p {{
            color: {text_color};
        }}
        h1, h2, h3, h4 {{
            color: {primary_color};
        }}
    </style>
""", unsafe_allow_html=True)

# Hide footer and menu
hide_default_format = """
       <style>
       # MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

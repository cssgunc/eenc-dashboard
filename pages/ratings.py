import pandas as pd
import streamlit as st
import plotly.express as px
from data.feedback_data import feedback_dic
import random

# Set page title and favicon
st.set_page_config(page_title="Ratings",
                   page_icon="assets/EENC-logo.png", layout="wide")

# Load the data
# data = pd.read_csv("data/data.csv")

# Data from Streamlit state
data = st.session_state["master_data"]
feedback_data = feedback_dic

# replace 'N/A' with NaN
data = data.replace('N/A', float('nan'))

# Set constants for theme colors
primary_color = "#195E4C"
secondary_color = "#3C9E8D"
text_color = "#6D7183"

# Logo
st.image("assets/EENC-logo.png", width=100)

# Sidebar
st.sidebar.title("Filters")
form_name = st.sidebar.selectbox(
    "Select Form Name", ['All'] + sorted(data['Form Name'].unique()))
st.sidebar.caption("Need more help? Refer to our documentation here")

if form_name != 'All':
    data = data[data['Form Name'] == form_name]
    collection_name = form_name.replace('_', ' ').title().replace("Test", "TEST")
    print(collection_name)
    feedback_data = feedback_data[collection_name]

# Main content
st.title("EENC Ratings Summary")
st.write("This page displays a summary of ratings for EENC courses. Use the filter on the left to customize the results.")
st.markdown('---')


def generate_rating_chart(column_name, chart_title, feedback_type=None):
    column_data = data[column_name]
    column_data = column_data.astype(float)
    column_data = data[column_name].fillna(3)
    average_rating = round(column_data.mean(), 2)
    mode_rating = column_data.mode()[0] if not column_data.empty else 0
    median_rating = column_data.median() if not column_data.empty else 0

    if average_rating == 0 and mode_rating == 0 and median_rating == 0:
        print("no available data for " + column_name)
    else:
        fig = px.histogram(data, x=column_name, nbins=5, opacity=1, color_discrete_sequence=[secondary_color], height=350)

        fig.update_layout(
            xaxis_title="Rating",
            yaxis_title="Count",
            showlegend=False,
            margin=dict(t=0),
            plot_bgcolor="white",
            paper_bgcolor="white",
        )

        st.subheader(chart_title)
        st.markdown("  ")
        with st.container():
            col1, col2 = st.columns([1, 2])
            if average_rating != 0:
                with col1:
                    st.metric("Average", f"{average_rating:.2f}", delta_color='normal')
            if mode_rating != 0:
                with col1:
                    st.metric("Mode", mode_rating, delta_color='normal')
            if median_rating != 0:
                with col1:
                    st.metric("Median", median_rating, delta_color='normal')
            with col2:
                st.plotly_chart(fig, use_container_width=True)

        if feedback_type in feedback_data and len(feedback_data[feedback_type]) > 0:
            st.write("Random feedback:")
            random_feedback = random.sample(feedback_data[feedback_type], min(3, len(feedback_data[feedback_type])))
            for feedback in random_feedback:
                st.write(f"- {feedback}")

# Course Rating
generate_rating_chart('Course Rating', 'On a scale of 1 to 5, how do you rate this course overall?','general_feedback')

# Instructor Rating
generate_rating_chart('Instructor Rating', 'On a scale of 1 to 5, how do you rate the instructor of this course?','instructor_feedback')

# Accessibility Rating
generate_rating_chart('Accessibility Rating', 'How accessible do you find this course?','accessibility_feedback')

# Navigation Rating
generate_rating_chart('Navigation Rating', 'On a scale of 1 to 5, how easy was it to navigate this course?','structure_feedback')

# Improvement Efforts Rating
generate_rating_chart('Improvement Efforts', 'On a scale of 1 to 5, how satisfied are you with the improvement efforts made after feedback?')

# Sharing Interest Rating
generate_rating_chart('Sharing Interest', 'On a scale of 1 to 5, how interested are you in sharing what you learned with others?')

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
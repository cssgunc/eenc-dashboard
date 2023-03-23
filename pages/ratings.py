import pandas as pd
import streamlit as st
import plotly.express as px

# Load the data
data = pd.read_csv("data/data.csv")

# put logo on sidebar

# create a dictionary that maps string values to numerical values
mapping = {'Very Low': 1, 'Low': 2, 'Average': 3, 'High': 4, 'Very High': 5}

# map the string values to numerical values
data['Sharing Interest'] = data['Sharing Interest'].map(mapping)

# Set constants for theme colors
PRIMARY_COLOR = "#195E4C"
SECONDARY_COLOR = "#3C9E8D"
TEXT_COLOR = "#6D7183"

# Set page title and favicon
st.set_page_config(page_title="Ratings", page_icon="assets/EENC-logo.png", layout="wide")

# Logo
st.image("assets/EENC-logo.png", width=100)

# Sidebar
st.sidebar.title("Filters")
form_name = st.sidebar.selectbox("Select Form Name", ['All'] + sorted(data['Form Name'].unique()))

# Show location filter only when "All" is selected in "Form Name"
if form_name == "All":
    location = st.sidebar.radio("Select Location", ['All', 'Online', 'In-Person'])
else:
    location = "All"


# Filter the data
if form_name != 'All':
    data = data[data['Form Name'] == form_name]
if location != 'All':
    data = data[data['Online/In-Person'] == location]


# Main content
st.title("EENC Ratings Summary")
st.markdown("This page displays a summary of ratings for EENC courses. Use the filters on the left to customize the results.")
st.markdown('---')

def generate_rating_chart(column_name, chart_title):
    column_data = data[column_name]
    average_rating = round(column_data.mean(), 2)
    mode_rating = column_data.mode()[0]
    median_rating = column_data.median()

    fig = px.histogram(data, x=column_name, nbins=5, opacity=1, color_discrete_sequence=[SECONDARY_COLOR], height=350)

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
        with col1:
            st.metric("Average", f"{average_rating:.2f}", delta_color='normal')
            st.metric("Mode", mode_rating, delta_color='normal')
            st.metric("Median", median_rating, delta_color='normal')
        with col2:
            st.plotly_chart(fig, use_container_width=True)

# Course Rating
generate_rating_chart('Course Rating', 'On a scale of 1 to 5, how do you rate this course overall?')

# Instructor Rating
generate_rating_chart('Instructor Rating', 'On a scale of 1 to 5, how do you rate the instructor of this course?')

# Accessibility Rating
generate_rating_chart('Accessibility Rating', 'How accessible do you find this course?')

# Navigation Rating
generate_rating_chart('Navigation Rating', 'On a scale of 1 to 5, how easy was it to navigate this course?')

# Improvement Efforts Rating
generate_rating_chart('Improvement Efforts', 'On a scale of 1 to 5, how satisfied are you with the improvement efforts made after feedback?')

# Sharing Interest Rating
generate_rating_chart('Sharing Interest', 'On a scale of 1 to 5, how interested are you in sharing what you learned with others?')

# Add CSS to customize text colors
st.markdown(f"""
    <style>
        div.css-edivx2.e16fv1kl3 {{
            color: {SECONDARY_COLOR};
        }}
        p {{
            color: {TEXT_COLOR};
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: {PRIMARY_COLOR};
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
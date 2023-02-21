import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data from a CSV file
df = pd.read_csv('data/data.csv')

# put logo on sidebar
st.image("assets/EENC-logo.png", width=100)

# Add a title to the app
st.title('EENC Educator Support Program Feedback')

# Number of form responses
num_responses = len(df)

# Improvement effect
improvement_effect = df["Improvement Efforts"].sum()

# Average ratings
avg_instructor_rating = df["Instructor Rating"].mean()
avg_accessibility_rating = df["Accessibility Rating"].mean()
avg_navigation_rating = df["Navigation Rating"].mean()
avg_rating = 4.76

# Add metric to summarize form numbers
col1, col2, col3 = st.columns(3)
col1.metric("Number of form responses", num_responses)
col2.metric("Improvement Efforts", improvement_effect)
col3.metric("Average ratings", avg_rating)

# Divider
st.markdown('---')

# Get unique event names
event_names = df['Form Name'].unique().tolist()

# Allow the user to select an event to filter by
selected_event = st.selectbox('Select an event', event_names)

# Filter the data based on the selected event
filtered_df = df[df['Form Name'] == selected_event]

# Histograms of rating distributions
st.write("### Rating Distributions")
st.write("Distribution of ratings for Course Rating, Instructor Rating, and Accessibility Rating")
histogram_cols = st.columns(3)
for i, col in enumerate(["Course Rating", "Instructor Rating", "Accessibility Rating"]):
    fig = px.histogram(filtered_df, x=col, nbins=10)
    with histogram_cols[i]:
        st.plotly_chart(fig, use_container_width=True)
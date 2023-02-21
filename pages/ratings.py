import pandas as pd
import numpy as np
import streamlit as st
import altair as alt

# Load the data
data = pd.read_csv("data/data.csv")


# put logo on sidebar
st.image("assets/EENC-logo.png", width=100)

# Sidebar
st.sidebar.title("Filters")
form_name = st.sidebar.selectbox("Form Name", ['All'] + sorted(data['Form Name'].unique()))
location = st.sidebar.radio("Location", ['All', 'Online', 'In-Person'])

# Filter the data
if form_name != 'All':
    data = data[data['Form Name'] == form_name]
if location != 'All':
    data = data[data['Online/In-Person'] == location]

# Main content
st.title("Ratings Summary")
st.markdown("This page displays a summary of ratings for EENC courses. Use the filters on the left to customize the results.")
st.markdown('   ')

# Set theme colors
primary_color = "#195E4C"
secondary_color = "#3C9E8D"
text_color = "#6D7183"

# Course Rating
course_rating = data['Course Rating']
average_course_rating = round(course_rating.mean(), 2)
mode_course_rating = course_rating.mode()[0]
median_course_rating = course_rating.median()
course_rating_hist = alt.Chart(data).mark_bar(color=secondary_color).encode(
    alt.Y('count()', title='Count', axis=alt.Axis(grid=False)),
    alt.X('Course Rating:Q', bin=alt.Bin(step=1), title='Rating', axis=alt.Axis(grid=False)),
    tooltip=['count()', 'Course Rating']
)
st.subheader("How do you rate this course overall?")
st.markdown("  ")
with st.container():
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("Average", f"{average_course_rating:.2f}", delta_color='normal')
        st.metric("Mode", mode_course_rating, delta_color='normal')
        st.metric("Median", median_course_rating, delta_color='normal')
    with col2:
        st.altair_chart(course_rating_hist)

# Instructor Rating
instructor_rating = data['Instructor Rating']
average_instructor_rating = round(instructor_rating.mean(), 2)
mode_instructor_rating = instructor_rating.mode()[0]
median_instructor_rating = instructor_rating.median()
instructor_rating_hist = alt.Chart(data).mark_bar(color=secondary_color).encode(
    alt.Y('count()', title='Count', axis=alt.Axis(grid=False)),
    alt.X('Instructor Rating:Q', bin=alt.Bin(step=1), title='Rating', axis=alt.Axis(grid=False)),
    tooltip=['count()', 'Instructor Rating']
)
st.subheader("How do you rate the instructor of this course?")
st.markdown("  ")
with st.container():
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("Average", f"{average_instructor_rating:.2f}", delta_color='normal')
        st.metric("Mode", mode_instructor_rating, delta_color='normal')
        st.metric("Median", median_instructor_rating, delta_color='normal')
    with col2:
        st.altair_chart(instructor_rating_hist)

# Accessibility Rating
accessibility_rating = data['Accessibility Rating']
average_accessibility_rating = round(accessibility_rating.mean(), 2)
mode_accessibility_rating = accessibility_rating.mode()[0]
median_accessibility_rating = accessibility_rating.median()
accessibility_rating_hist = alt.Chart(data).mark_bar(color=secondary_color).encode(
    alt.Y('count()', title='Count', axis=alt.Axis(grid=False)),
    alt.X('Accessibility Rating:Q', bin=alt.Bin(step=1), title='Rating', axis=alt.Axis(grid=False)),
    tooltip=['count()', 'Accessibility Rating']
)
st.subheader("How accessible do you find this course?")
st.markdown("  ")
with st.container():
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("Average", f"{average_accessibility_rating:.2f}", delta_color='normal')
        st.metric("Mode", mode_accessibility_rating, delta_color='normal')
        st.metric("Median", median_accessibility_rating, delta_color='normal')
    with col2:
        st.altair_chart(accessibility_rating_hist)

# Navigation Rating
navigation_rating = data['Navigation Rating']
average_navigation_rating = round(navigation_rating.mean(), 2)
mode_navigation_rating = navigation_rating.mode()[0]
median_navigation_rating = navigation_rating.median()
navigation_rating_hist = alt.Chart(data).mark_bar(color=secondary_color).encode(
    alt.Y('count()', title='Count', axis=alt.Axis(grid=False)),
    alt.X('Navigation Rating:Q', bin=alt.Bin(step=1), title='Rating', axis=alt.Axis(grid=False)),
    tooltip=['count()', 'Navigation Rating']
)
st.subheader("How easy is it to navigate this course?")
st.markdown("  ")
with st.container():
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("Average", f"{average_navigation_rating:.2f}", delta_color='normal')
        st.metric("Mode", mode_navigation_rating, delta_color='normal')
        st.metric("Median", median_navigation_rating, delta_color='normal')
    with col2:
        st.altair_chart(navigation_rating_hist)


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
    </style>
""", unsafe_allow_html=True)

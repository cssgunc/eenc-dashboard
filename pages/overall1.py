import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv("data/data.csv")

# logo
st.image("assets/EENC-logo.png", width=100)

st.title("Overall Information for EENC Dashboard")
st.markdown("This page displays overall information for the EENC courses. Use the filters on the left to customize the results.")
st.markdown('   ')

primary_color = "#195E4C"
secondary_color = "#3C9E8D"
text_color = "#6D7183"

# Sidebar
st.sidebar.title("Filters")
form_name = st.sidebar.selectbox("Form Name", ['All'] + sorted(data['Form Name'].unique()))
location = st.sidebar.radio("Location", ['All', 'Online', 'In-Person'])

# Filter the data
if form_name != 'All':
    data = data[data['Form Name'] == form_name]
if location != 'All':
    data = data[data['Online/In-Person'] == location]


st.header("Metrics")
# total number of respondents, course rating, average ratings
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Responses", len(data))
col2.metric("Avg. Course", round(data['Course Rating'].mean(), 2))
col3.metric("Avg. Instructor", round(data['Instructor Rating'].mean(), 2))
col4.metric("Avg. Accessibility", round(data['Accessibility Rating'].mean(), 2))
col5.metric("Avg. Navigation", round(data['Navigation Rating'].mean(), 2))


st.markdown('   ')
st.header("\nGraphs & Trends")
# Average knowledge gain, most popular classes, trends over time
st.markdown('### Guidelines Before')

value_counts = data['Guidelines Before'].value_counts()
fig, ax = plt.subplots()
bar_color = primary_color
ax.bar(value_counts.index, value_counts.values, color=bar_color)
ax.set_title("Count of values in 'Guidelines Before' column")
ax.set_xlabel('Guidelines Before')
ax.set_ylabel("Count")
st.pyplot(fig)

st.markdown('   ')
st.markdown('### Guidelines After')

value_counts = data['Guidelines After'].value_counts()
fig, ax = plt.subplots()
ax.bar(value_counts.index, value_counts.values, color=bar_color)
ax.set_title("Count of values in 'Guidelines After' column")
ax.set_xlabel('Guidelines After')
ax.set_ylabel("Count")
st.pyplot(fig)

st.markdown('   ')
st.markdown('### Sharing Interest')

value_counts = data['Sharing Interest'].value_counts()
fig, ax = plt.subplots()
ax.bar(value_counts.index, value_counts.values, color=bar_color)
ax.set_title("Count of values in 'Sharing Interest' column")
ax.set_xlabel('Sharing Interest')
ax.set_ylabel("Count")
st.pyplot(fig)

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

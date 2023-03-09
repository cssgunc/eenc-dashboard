import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from bokeh.models.widgets import Div

# Set page title and favicon
st.set_page_config(page_title="Homepage", page_icon="assets/EENC-logo.png", layout="wide")

# Load the data
data = pd.read_csv("data/data.csv")

# logo
st.image("assets/EENC-logo.png", width=100)

st.title("Welcome to the EENC dashboard")
st.markdown("This page displays overall information for the EENC courses. Use the filters on the left to customize the results.")
st.markdown('---')

primary_color = "#195E4C"
secondary_color = "#3C9E8D"
text_color = "#6D7183"

# Sidebar
st.sidebar.title("Filters")
form_name = st.sidebar.selectbox("Form Name", ['All'] + sorted(data['Form Name'].unique()))
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

st.markdown('   ')
col1, col2 = st.columns(2)
col1.metric("Total Responses", len(data))
col2.metric("Improvement Efforts", data["Improvement Efforts"].sum())
st.markdown('   ')


c1, c2 = st.columns((7,3))
with c1:
    st.header("Ratings")
with c2:
    if st.button('Go to Ratings Page'):
        js = "window.open('https://www.streamlit.io/')"  # New tab or window
        js = "window.location.href = 'https://www.streamlit.io/'"  # Current tab
        html = '<img src onerror="{}">'.format(js)
        div = Div(text=html)
        st.bokeh_chart(div)

# total number of respondents, course rating, average ratings
# put some stuff that links to mel's rating page
col1, col2, col3, col4 = st.columns(4)
col1.metric("Avg. Course", round(data['Course Rating'].mean(), 2))
col2.metric("Avg. Instructor", round(data['Instructor Rating'].mean(), 2))
col3.metric("Avg. Accessibility", round(data['Accessibility Rating'].mean(), 2))
col4.metric("Avg. Navigation", round(data['Navigation Rating'].mean(), 2))


st.markdown('   ')
st.markdown('   ')
st.header("\nGraphs & Trends")
# Average knowledge gain, most popular classes, trends over time


st.markdown('### Guidelines Before')

value_counts = data['Guidelines Before'].value_counts().reset_index()
value_counts.columns = ['Guidelines Before', 'Count']

# Define the order of the labels
labels_order = ["Very Low", "Low", "Average", "High", "Very High"]

bar_color = secondary_color

fig = px.bar(value_counts, x='Guidelines Before', y='Count', text='Count',
             category_orders={'Guidelines Before': labels_order},
             color_discrete_sequence=[bar_color])
fig.update_traces(texttemplate='%{text}', textposition='auto')

fig.update_layout(xaxis_title='Guidelines Before',
                  yaxis_title='Count')

st.plotly_chart(fig)


st.markdown('   ')

st.markdown('### Guidelines After')

value_counts = data['Guidelines After'].value_counts().reset_index()
value_counts.columns = ['Guidelines After', 'Count']

# Define the order of the labels
labels_order = ["Average", "High", "Very High"]

bar_color = secondary_color

fig = px.bar(value_counts, x='Guidelines After', y='Count', text='Count',
             category_orders={'Guidelines After': labels_order},
             color_discrete_sequence=[bar_color])
fig.update_traces(texttemplate='%{text}', textposition='auto')

fig.update_layout(xaxis_title='Guidelines After',
                  yaxis_title='Count')

st.plotly_chart(fig)

st.markdown('   ')

st.markdown('### Sharing Interest')

value_counts = data['Sharing Interest'].value_counts().reset_index()
value_counts.columns = ['Sharing Interest', 'Count']

# Define the order of the labels
labels_order = ["Average", "High", "Very High"]

bar_color = secondary_color

fig = px.bar(value_counts, x='Sharing Interest', y='Count', text='Count',
             category_orders={'Sharing Interest': labels_order},
             color_discrete_sequence=[bar_color])
fig.update_traces(texttemplate='%{text}', textposition='auto')

fig.update_layout(xaxis_title='Sharing Interest',
                  yaxis_title='Count')

st.plotly_chart(fig)

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

# Hide footer and menu
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)
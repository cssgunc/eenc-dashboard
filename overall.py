import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
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


# Check that this translates over guidelines qualitative values to quantitative
guidelines_before = data['Guidelines Before']
guidelines_after = data['Guidelines After']
guidelines_scale = {"Very Low": 1, "Low": 2, "Average": 3, "High": 4, "Very High": 5}

counts_before = guidelines_before.value_counts().reindex(["Very Low", "Low", "Average", "High", "Very High"])
counts_after = guidelines_after.value_counts().reindex(["Very Low", "Low", "Average", "High", "Very High"])

st.markdown('   ')
st.markdown("All average ratings are calculated out of 5.")
st.markdown('   ')

c1, c2 = st.columns((7,3))
with c1:
    st.header("Improvement & Guidelines")
with c2:
    if st.button('Go to the Guidelines Page'):
        js = "window.open('https://www.streamlit.io/')"  # New tab or window
        js = "window.location.href = 'https://www.streamlit.io/'"  # Current tab
        html = '<img src onerror="{}">'.format(js)
        div = Div(text=html)
        st.bokeh_chart(div)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Responses", len(data))
col2.metric("Avg. Improvement Efforts", round(data["Improvement Efforts"].mean(), 2))
col3.metric("Avg. Guidelines Before", round(counts_before.mean(), 0) / 10)
col4.metric("Avg. Guidelines After", round(counts_after.mean()) / 10)

st.markdown("The following scale corresponds to Guidelines: Very Low: 1, Low: 2, Average: 3, High: 4, Very High: 5")

# include third metric for  growth in guidelines? or maybe one for avg. guidelines before, avg. guidelines after, and avg. growth
st.markdown('   ')


c1, c2 = st.columns((7,3))
with c1:
    st.header("Ratings")
with c2:
    if st.button('Go to the Ratings Page'):
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


st.markdown('### Guidelines Before & After')

# Get value counts for "Guidelines Before"
value_counts_before = data['Guidelines Before'].value_counts().reset_index()
value_counts_before.columns = ['Guidelines', 'Count']

labels_order_before = ["Very Low", "Low", "Average", "High", "Very High"]
labels_order_after = ["Average", "High", "Very High"]
bar_color_before = 'blue'
bar_color_after = secondary_color


# Create the first bar chart
fig = px.bar(value_counts_before, x='Guidelines', y='Count', text='Count',
             category_orders={'Guidelines': labels_order_before},
             color_discrete_sequence=[bar_color_before])

# Update the chart title and axis labels
fig.update_layout(title='Guidelines Before & After',
                  xaxis_title='Guidelines',
                  yaxis_title='Count')

# Get value counts for "Guidelines After"
value_counts_after = data['Guidelines After'].value_counts().reset_index()
value_counts_after.columns = ['Guidelines', 'Count']

# Create the second bar chart
fig.add_trace(go.Bar(x=value_counts_after['Guidelines'],
                     y=value_counts_after['Count'],
                     name='Guidelines After',
                     marker_color=bar_color_after))

# Update the trace labels
fig.update_traces(texttemplate='%{y}', textposition='auto')

fig.update_layout(legend=dict(
    orientation='v',
    xanchor='right',
    itemsizing='constant',
    itemwidth=50,
    bgcolor='rgba(255, 255, 255, 0.5)'),
)

# Display the chart
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
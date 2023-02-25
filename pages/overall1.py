import streamlit as st
import pandas as pd
import plotly.express as px
import plost as pt

# Load the data
data = pd.read_csv("data/data.csv")

st.title("Overall Information for EENC Dashboard")

st.header("Metrics")
# total number of respondents, course rating, average ratings
col1, col2, col3 = st.columns(3)
col1.metric("Responses", len(data))

# inperson, ip_sum, online, on_sum = 0

# for i in len(data):
#     if data[i]['Form Name'] == "In-Person General Guidelines":
#         inperson += 1
#         ip_sum 
#     else:
#         online += 1

col2.metric("Average Course Rating", )

st.header("Graphs & Trends")
# Average knowledge gain, most popular classes, trends over time
st.markdown('### Guidelines Before')
pt.donut_chart(data = data['Guidelines Before'])

st.markdown('### Guidelines After')
pt.donut_chart(data = data['Guidelines After'])
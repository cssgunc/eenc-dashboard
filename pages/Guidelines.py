import pandas as pd
import numpy as np
import streamlit as st
import matplotlib as mat
import matplotlib.pyplot as plt
import plotly.express as px

# Set page title and favicon
st.set_page_config(page_title="Guidelines",
                   page_icon="assets/EENC-logo.png", layout="wide")

# data = pd.read_csv("data/data.csv")

# Data from Streamlit state
data = st.session_state['master_data']
#data = st_data


st.image("assets/EENC-logo.png", width = 100)
unique_form_names = sorted(data['Form Name'].unique())
cleaned_form_names = [name.replace('_', ' ').title() for name in unique_form_names]



# sidebar
st.sidebar.title("Filters")

options = ["All"] + cleaned_form_names

form_name = st.sidebar.selectbox("Select Form Name", options, options.index(st.session_state["formname"]))

# Filter the data
if form_name != 'All': #event name
    formatted_form_name = f"{form_name.lower().replace(' ', '_')}"
    data = data[data['Form Name'] == formatted_form_name]
    st.session_state["formname"] = form_name
else:
    st.session_state["formname"] = "All"

# Get unique locations and remove "None"
unique_locations = data['Student Location'].dropna().unique()
# Group "Mix of Areas" and "A Mix of Areas"
unique_locations = np.where(unique_locations=="Mix of Areas", "A Mix of Areas", unique_locations)
unique_locations = data['Student Location'].dropna().replace({'A Mix of Areas': 'Mix of Areas'}).unique()
location = st.sidebar.radio("Student Location", ["All"] + list(unique_locations))
st.sidebar.caption("Need more help? Refer to our documentation [here](https://docs.google.com/document/d/19GpSxMp12O3dHoJHs6DARf3IpwtUShdqWRiDNICFZXI/edit?usp=sharing)")
if location == "Mix of Areas":
    data_Mix = data[data["Student Location"] == location]
    data_AMix = data[data["Student Location"] == "A Mix of Areas"]
    frames = [data_Mix, data_AMix]
    data = pd.concat(frames)
else:
    if location != "All":
        data = data[data["Student Location"] == location]

# Main content
st.title("Guidelines Summary")
st.markdown("This page displays a summary of guidelines for EENC courses. Use the filters on the left to customize the results.")
st.markdown('   ')

# set theme color
primary_color = "#195E4C"
secondary_color = "#3C9E8D"
text_color = "#6D7183"
mat.rcParams['text.color'] = text_color
mat.rcParams['axes.labelcolor'] = text_color
mat.rcParams['xtick.color'] = text_color
mat.rcParams['ytick.color'] = text_color

# Get guidelines data
guidelines_before = data['Guidelines Before']
guidelines_after = data['Guidelines After']
guidelines_scale = {"Very Low": 1, "Low": 2, "Average": 3, "High": 4, "Very High": 5}

# convert float values to categories
categories_before = pd.cut(guidelines_before, bins=[0.0, 1.0, 2.0, 3.0, 4.0, 5.0], labels=["Very Low", "Low", "Average", "High", "Very High"])
categories_after = pd.cut(guidelines_after, bins=[0.0, 1.0, 2.0, 3.0, 4.0, 5.0], labels=["Very Low", "Low", "Average", "High", "Very High"])
# count the categories
counts_before = categories_before.value_counts().reindex(["Very Low", "Low", "Average", "High", "Very High"])
counts_after = categories_after.value_counts().reindex(["Very Low", "Low", "Average", "High", "Very High"])
st.header("Graphs & Trends")
st.subheader("How do guidelines change before and after?")
st.markdown("*Circle size indicates number of population; Numbers of students are shown in the box.")
st.markdown("")

#calculate stats
total_students = len(guidelines_after)
perc_high_before = np.nan_to_num(100 * np.sum(guidelines_before >= 4) / total_students)
perc_high_after = np.nan_to_num(100 * np.sum(guidelines_after >= 4) / total_students)
perc_vhigh_before = np.nan_to_num(100 * np.sum(guidelines_before >= 5) / total_students)
perc_vhigh_after = np.nan_to_num(100 * np.sum(guidelines_after >= 5) / total_students)

#Figure 1: Scatter plot and lines

with st.container():
    col1, col2 = st.columns([1, 3.75])
    with col1:
        st.metric(label="Total Students", value=total_students)
        st.metric(label="High %", value=f"{round(perc_high_after, 1)}%", delta=f"{round(perc_high_after - perc_high_before, 1)}%")
        st.metric(label="Very High %", value=f"{round(perc_vhigh_after, 1)}%", delta=f"{round(perc_vhigh_after - perc_vhigh_before, 1)}%")
    with col2:
        data = pd.DataFrame({
            "When Education is Received": 5 * ["Before"] + 5 * ["After"],
            "Guidelines Rating": ["Very Low", "Low", "Average", "High", "Very High"] * 2,
            "Counts": pd.concat([counts_before, counts_after]).reset_index(drop=True)
        })
        data = data.dropna()  # drop rows with NaN values
        data["Size"] = data["Counts"] * 10
        fig = px.scatter(data, x="When Education is Received", y="Guidelines Rating", size="Size",
                         color_discrete_sequence=[secondary_color], opacity=1,
                         labels={"When Education is Received": "When Education is Received", "Guidelines Rating": "Guidelines Rating"},
                         hover_data={"Counts": True, "Size": False})
        fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')), selector=dict(mode='markers'))
        fig.update_layout(
            legend=dict(traceorder='normal'),
            xaxis=dict(tickfont=dict(size=10)),
            yaxis=dict(tickfont=dict(size=10)),
            margin=dict(l=0, r=0, t=50, b=0),
            width=1200,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)



    
st.markdown('   ')
st.subheader("How does the overall pattern change?")
st.markdown("Below shows the overall pattern of students' guidelines.")

#Figure 2: bar plot

edu_time = ["Before", "After"]
y = {
    "Very Low": [counts_before["Very Low"], counts_after["Very Low"]],
    "Low": [counts_before["Low"], counts_after["Low"]],
    "Average": [counts_before["Average"], counts_after["Average"]],
    "High": [counts_before["High"], counts_after["High"]],
    "Very High": [counts_before["Very High"], counts_after["Very High"]]
}
barcolor = ['#42B6ED', '#42DBED', '#45F7DA', '#4AE19C', '#3C9E8D']

data = []
for group, barvalue in y.items():
    data.extend([{"When Education is Received": edu_time[i], "Guidelines Rating": group, "Counts": barvalue[i]} for i in range(len(edu_time))])

fig = px.bar(data, x="When Education is Received", y="Counts", color="Guidelines Rating", text="Counts",
             color_discrete_sequence=barcolor, barmode="group", opacity=1,
             labels={"When Education is Received": "When Education is Received", "Counts": "Number of Participants", "Guidelines Rating": "Guidelines Rating"},
             hover_data={"Counts": True})

fig.update_layout(
    xaxis=dict(tickfont=dict(size=10)),
    yaxis=dict(tickfont=dict(size=10)),
    legend=dict(traceorder='normal')
)

with st.container():
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
        .css-1qpc1ke a {{
            color: {secondary_color};
        }}
    </style>
""", unsafe_allow_html=True)
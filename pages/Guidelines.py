import pandas as pd
import numpy as np
import streamlit as st
import matplotlib as mat
import matplotlib.pyplot as plt

data = pd.read_csv("data/data.csv")

st.image("assets/EENC-logo.png", width = 100)

# sidebar
st.sidebar.title("Filters")
form_name = st.sidebar.selectbox("Form Name", ['All'] + sorted(data['Form Name'].unique()))
event_type = st.sidebar.radio("Location", ['All', 'Online', 'In-Person'])
location = st.sidebar.radio("Student Location", ["All", "Mix of Areas", "Rural", "Urban", "Suburban"])

# Filter the data
if form_name != 'All':
    data = data[data['Form Name'] == form_name]
if event_type != 'All':
    event_type = data[data['Online/In-Person'] == event_type]
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
st.markdown('---')

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

counts_before = guidelines_before.value_counts().reindex(["Very Low", "Low", "Average", "High", "Very High"])
counts_after = guidelines_after.value_counts().reindex(["Very Low", "Low", "Average", "High", "Very High"])

st.header("Graphs & Trends")
st.subheader("How do guidelines change before and after?")
st.caption("*Circle size indicates number of population; Numbers of students are shown in the box.")
st.markdown("")

#calculate stats
total_students = len(guidelines_after)
perc_high_before = np.nan_to_num(100*(counts_before["High"]/total_students))
perc_high_after = np.nan_to_num(100*(counts_after["High"]/total_students))
perc_vhigh_before = np.nan_to_num(100*(counts_before["Very High"]/total_students))
perc_vhigh_after = np.nan_to_num(100*(counts_after["Very High"]/total_students))

#Figure 1: Scatter plot and lines
with st.container():
    col1, col2 = st.columns([1, 3.75])
    with col1:
        st.metric(label="Total Students", value=total_students)
        st.metric(label="High %", value=f"{round(perc_high_after, 1)}%", delta=f"{round(perc_high_after - perc_high_before, 1)}%")
        st.metric(label="Very High %", value=f"{round(perc_vhigh_after, 1)}%", delta=f"{round(perc_vhigh_after - perc_vhigh_before, 1)}%")
    with col2:
        fig, ax = plt.subplots()
        size = pd.concat([counts_before, counts_after])*25
        x = 5 * ["Before"] + 5 * ["After"]
        y = ["Very Low", "Low", "Average", "High", "Very High"] * 2
        ax.scatter(x, y, s=size.values, color=secondary_color, alpha=0.5)
        ax.set_xlabel("When Education is Received")
        ax.set_ylabel("Guidelines Rating")
        ax.margins(x=0.4, y=0.2)
        green_circle = mat.lines.Line2D([], [], color="white", marker='o', markerfacecolor=secondary_color, alpha=0.5, markersize=10)
        ax.legend([green_circle], ['Students Population'], loc="lower right")
        annotations = np.nan_to_num(pd.concat([counts_before, counts_after]))
        min_text_offset = 20
        text_offset = np.sqrt(max(size.values)) if np.sqrt(max(size.values)) > min_text_offset else min_text_offset
        for xi, yi, text in zip(x, y, annotations):
            if text != 0:
                ax.annotate(int(text), xy=(xi, yi), xycoords='data', xytext=(text_offset, 0), textcoords='offset points', bbox=dict(boxstyle="square,pad=0.3", facecolor="#1C00ff00", edgecolor=text_color))
        st.pyplot(fig)

st.markdown('   ')
st.subheader("How does the overall pattern change?")
st.caption("Below shows the overall pattern of students' guidelines.")

#Figure 2: bar plot
fig, ax = plt.subplots()
edu_time = ["Before", "After"]
y = {
    "Very Low": [counts_before["Very Low"], counts_after["Very Low"]],
    "Low": [counts_before["Low"], counts_after["Low"]],
    "Average": [counts_before["Average"], counts_after["Average"]],
    "High": [counts_before["High"], counts_after["High"]],
    "Very High": [counts_before["Very High"], counts_after["Very High"]]
}
barcolor = ["#142735", "#1f7774", "#3c9e8d", "#a6d687", "#dbe955"]
x = np.array([0, 0.7])
width = 0.1
multiplier = 0
i = 0
#create group bar chart
for group, barvalue in y.items():
    offset = width * multiplier
    p = ax.bar(x + offset, barvalue, width, label=group, color=barcolor[i])
    multiplier += 1
    i += 1
#create labels for bar chart
labels = [int(i) for tup in zip(np.nan_to_num(counts_before.values), np.nan_to_num(counts_after.values)) for i in tup]
rects = ax.patches
for rect, label in zip(rects, labels):
    height = rect.get_height()
    ax.text(
        np.nan_to_num(rect.get_x()) + rect.get_width() / 2, np.nan_to_num(height), label, ha="center", va="bottom"
    )
ax.set_xticks(x + 2*width, edu_time)
ax.margins(x=0.15, y=0.1)
ax.set_xlabel("When Education is Received")
ax.set_ylabel("Number of Participants", labelpad=10)
ax.legend(fontsize="small", loc="upper center")
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
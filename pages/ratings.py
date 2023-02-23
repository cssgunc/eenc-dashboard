import pandas as pd
import streamlit as st
import altair as alt

# Load the data
data = pd.read_csv("data/data.csv")

# create a dictionary that maps string values to numerical values
mapping = {'Very Low': 1, 'Low': 2, 'Average': 3, 'High': 4, 'Very High': 5}

# map the string values to numerical values
data['Sharing Interest'] = data['Sharing Interest'].map(mapping)

# Set constants for theme colors
PRIMARY_COLOR = "#195E4C"
SECONDARY_COLOR = "#3C9E8D"
TEXT_COLOR = "#6D7183"

# Set page title and favicon
st.set_page_config(page_title="EENC Ratings Summary", page_icon="assets/EENC-logo.png", layout="wide")

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

# Reset button
if st.sidebar.button("Reset Filters"):
    form_name = 'All'
    location = 'All'
    data = pd.read_csv("data/data.csv")

    # map the string values to numerical values
    data['Sharing Interest'] = data['Sharing Interest'].map(mapping)

    st.experimental_rerun()

# Download button
st.sidebar.markdown('---')
st.sidebar.markdown('### Download Report')
if st.sidebar.button("Download CSV"):
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="ratings_summary.csv">Download CSV</a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)

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
    rating_hist = alt.Chart(data).mark_bar(color=SECONDARY_COLOR).encode(
        alt.Y('count()', title='Count', axis=alt.Axis(grid=False)),
        alt.X(f'{column_name}:Q', bin=alt.Bin(step=1), title='Rating', axis=alt.Axis(grid=False)),
        tooltip=['count()', f'{column_name}']
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
            st.altair_chart(rating_hist)

# Course Rating
generate_rating_chart('Course Rating', 'How do you rate this course overall?')

# Instructor Rating
generate_rating_chart('Instructor Rating', 'How do you rate the instructor of this course?')

# Accessibility Rating
generate_rating_chart('Accessibility Rating', 'How accessible do you find this course?')

# Navigation Rating
generate_rating_chart('Navigation Rating', 'How easy was it to navigate this course?')

# Improvement Efforts Rating
generate_rating_chart('Improvement Efforts', 'How satisfied are you with the improvement efforts made after feedback?')

# Sharing Interest Rating
generate_rating_chart('Sharing Interest', 'How interested are you in sharing what you learned with others?')


st.markdown('    ')
st.markdown("Made with :heart: by UNC CS+SG team")
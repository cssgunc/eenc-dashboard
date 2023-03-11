import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
data = pd.read_csv("data/data.csv")

#put logo on sidebar
st.image("assets/EENC-logo.png", width=100)

#Set theme colors
primary_color = '#195E4C'
secondary_color = '#3C9E8D'
text_color = '#6D7183'
bar_colors = ['#3C9E8D', '#4AE19C', '#4FF57E', '#4AE14D', '#88F956', '#DBFA59', '#F4F281']

# Add a title to the app
st.title('Demographics for the EENC Dashboard')
st.markdown('A visualization of different statistics relating to the demographics of EENC.')

#Sidebar
st.sidebar.title("Filters")
#form_name = st.sidebar.selectbox("Form Name", ['All'] + sorted(data['Form Name'].unique()))
location = st.sidebar.radio("Location", ['All', 'Online', 'In-Person'])

#Filter the Data
#if form_name != "All":
    #data = data[data['Form Name'] == form_name]
if location != "All":
    data = data[data['Online/In-Person'] == location]

#Profession
profession = data['Current Profession']
total_professions = len(profession)

non_formal_educator = data['Current Profession'].str.contains('Non-Formal Educator')
non_formal_educator_total = non_formal_educator.sum()

conservation_professional = data['Current Profession'].str.contains('Conservation/Natural Resources Professional')
conservation_professional_total = conservation_professional.sum()

college_instructor = data['Current Profession'].str.contains('College/University Instructor')
college_instructor_total = college_instructor.sum()

program_director = data['Current Profession'].str.contains('Program Director/Administrator')
program_director_total = program_director.sum()

school_teacher = data['Current Profession'].str.contains('PreK-12 Classroom Teacher')
school_teacher_total = school_teacher.sum()

student = data['Current Profession'].str.contains('Student|student')
student_total = student.sum()

other = ~data['Current Profession'].str.contains('Non-Formal Educator|Conservation/Natural Resources Professional|College/University Instructor|Program Director/Administrator|PreK-12 Classroom Teacher|Student|student')
other_total = other.sum()

all_professions = [
    'Non-Formal Educator', 
    'Conservation/Natural Resources Professional', 
    'College/University Instructor',
    'Program Director/Administrator',
    'PreK-12 Classroom Teacher',
    'Student',
    'Other'
]
professions_percentages = [
    round((non_formal_educator_total/total_professions), 4) * 100,
    round((conservation_professional_total/total_professions), 4) * 100,
    round((college_instructor_total/total_professions), 4) * 100,
    round((program_director_total/total_professions), 4) * 100,
    round((school_teacher_total/total_professions), 4) * 100,
    round((student_total/total_professions), 4) * 100,
    round((other_total/total_professions), 4) * 100
]

professions_numbers = [
    non_formal_educator_total,
    conservation_professional_total,
    college_instructor_total,
    program_director_total,
    school_teacher_total,
    student_total,
    other_total
]

bar_color = secondary_color

st.header('Statistics for Instructor Professions')
professions_bar_fig = px.bar(x=all_professions, y=professions_percentages, labels=dict(x='Professions', y='Percentage (out of Total Instructors)'), color_discrete_sequence=[bar_color])
professions_bar_fig.update_yaxes(range=[0,100])
st.subheader('Distribution of Instructor Professions by Percentage')
st.plotly_chart(professions_bar_fig)
st.caption("This bar graph depicts the percentage of instructors in each profession.")
st.caption("Due to potential overlap, percentages may add up to greater than 100%.")

professions_pie_fig = px.pie(values=professions_numbers, names=all_professions, color_discrete_sequence=bar_colors)
professions_pie_fig.update_traces(textinfo='value')
professions_pie_fig.update_traces(sort=False)
st.subheader('Distribution of Instructor Professions by Frequency')
st.plotly_chart(professions_pie_fig)
st.caption("This pie chart depicts the number of instructors in each profession.")
st.caption("Due to potential overlap, the numbers on the pie chart might be greater than the total number of instructors.")

#student count for each teacher
data['Student Count'] = pd.to_numeric(data['Student Count'], errors="coerce")
student_count = data['Student Count']
#student_count = pd.to_numeric(data['Student Count'], errors="coerce")
average_student_count = round(student_count.mean(), 2)

st.header('Statistics for Student to Instructor Ratio')
col1, col2 = st.columns(2)
col1.metric("Average student count per instructor", average_student_count)
col1.metric("Smallest student count", data['Student Count'].min())
col2.metric("Median student count per instructor", data['Student Count'].median())
col2.metric("Largest student count", data['Student Count'].max())


#relation between student count and course rating
data['Instructor Rating'] = data['Instructor Rating'].astype(int)
course_rating = data['Instructor Rating']
student_count_to_course_rating_fig = px.scatter(x=student_count, y=course_rating, labels=dict(x='Student Count',y='Instructor Rating'), color_discrete_sequence=[bar_color])
student_count_to_course_rating_fig.update_xaxes(range=[-100,4000])
student_count_to_course_rating_fig.update_yaxes(range=[0,6])
st.subheader('Correlation between Student-to-Instructor Ratio and Instructor Rating')
st.plotly_chart(student_count_to_course_rating_fig)
st.caption("This scatterplot depicts how instructor ratings correspond to an instructor's student-to-instructor ratio, in order to determine how an instructor's abilities are affected by higher student counts.")
st.caption('Please note that some outlier values are not depicted on the graph for better visibility.')

#relation between location and course rating
rural_student_count = data[data['Student Location']=='Rural']['Student Count']
average_rural_student_count = round(rural_student_count.mean(), 2)
suburban_student_count = data[data['Student Location']=='Suburban']['Student Count']
average_suburban_student_count = round(suburban_student_count.mean(), 2)
urban_student_count = data[data['Student Location']=='Urban']['Student Count']
average_urban_student_count = round(urban_student_count.mean(), 2)
mix_student_count = data[data['Student Location'].str.contains('Mix of Areas')]['Student Count']
average_mix_student_count = round(mix_student_count.mean(), 2)

student_location = data['Student Location']
student_location = student_location.replace("A Mix of Areas", "Mix of Areas")
student_location_to_course_rating_fig = px.strip(x=student_location, y=course_rating, color_discrete_sequence=[bar_color], labels=dict(x='Student Location',y='Instructor Rating'))
student_location_to_course_rating_fig.update_yaxes(range=[0,5.4])

st.header('Statistics for Student Location')
st.caption('Number of instructors by student location')
col1, col2, col3, col4 = st.columns(4)
col1.metric("Mix of Areas", len(mix_student_count))
col2.metric("Rural Areas", len(rural_student_count))
col3.metric("Suburban Areas", len(suburban_student_count))
col4.metric("Urban Areas", len(urban_student_count))
st.caption('Average student count by student location')
col1, col2, col3, col4 = st.columns(4)
col1.metric("Mix of Areas", average_mix_student_count)
col2.metric("Rural Areas", average_rural_student_count)
col3.metric("Suburban Areas", average_suburban_student_count)
col4.metric("Urban Areas", average_urban_student_count)
st.caption('Median student count by student location')
col1, col2, col3, col4 = st.columns(4)
col1.metric("Mix of Areas", mix_student_count.median())
col2.metric("Rural Areas", rural_student_count.median())
col3.metric("Suburban Areas", suburban_student_count.median())
col4.metric("Urban Areas", urban_student_count.median())
st.caption('Smallest student count by student location')
col1, col2, col3, col4 = st.columns(4)
col1.metric("Mix of Areas", mix_student_count.min())
col2.metric("Rural Areas", rural_student_count.min())
col3.metric("Suburban Areas", suburban_student_count.min())
col4.metric("Urban Areas", urban_student_count.min())
st.caption('Largest student count by student location')
col1, col2, col3, col4 = st.columns(4)
col1.metric("Mix of Areas", mix_student_count.max())
col2.metric("Rural Areas", rural_student_count.max())
col3.metric("Suburban Areas", suburban_student_count.max())
col4.metric("Urban Areas", urban_student_count.max())

st.subheader('Correlation between Student Location and Instructor Rating')
st.plotly_chart(student_location_to_course_rating_fig)
st.caption('This strip plot depicts how instructor ratings differ based on student location. The longer the strip, the higher the number of instructor ratings at that rating value are for a given area.')

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
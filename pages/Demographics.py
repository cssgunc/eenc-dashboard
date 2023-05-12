import streamlit as st
import pandas as pd
import plotly.express as px

# Set page title and favicon
st.set_page_config(page_title="Demographics", page_icon="assets/EENC-logo.png", layout="wide")

# Load the data
#data = pd.read_csv("data/data.csv")

# Data from Streamlit state
data = st.session_state['master_data']
#data = st_data
data = data.replace('N/A', float('nan'))

#put logo on sidebar
st.image("assets/EENC-logo.png", width=100)

#Set theme colors
primary_color = '#195E4C'
secondary_color = '#3C9E8D'
text_color = '#6D7183'
bar_colors = ['#3C9E8D', '#4AC14D', '#4AE19C', '#4FF57E', '#45F7EB', '#42DBED', '#42B6ED']
other_bar_colors = ['#42B6ED', '#42DBED', '#45F7DA', '#4AE19C', '#3C9E8D']

# Add a title to the app
st.title('Demographics Summary')
st.markdown('This page displays a summary of demographics for EENC courses. Use the filter on the left to customize the results.')
st.markdown("---")
#Sidebar
st.sidebar.title("Filter")
unique_form_names = sorted(data['Form Name'].unique())
cleaned_form_names = [name.replace('test_', '').replace('_', ' ').title() for name in unique_form_names]

form_name = st.sidebar.selectbox("Select Form Name", ['All'] + cleaned_form_names)

st.sidebar.caption("Need more help? Refer to our documentation [here](https://docs.google.com/document/d/19GpSxMp12O3dHoJHs6DARf3IpwtUShdqWRiDNICFZXI/edit?usp=sharing)")

if form_name != 'All':
    formatted_form_name = f"test_{form_name.lower().replace(' ', '_')}"
    data = data[data['Form Name'] == formatted_form_name]
    

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

other = data['Current Profession'].str.contains('Non-Formal Educator|Conservation/Natural Resources Professional|College/University Instructor|Program Director/Administrator|PreK-12 Classroom Teacher|Student|student')
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

# st.header('Statistics for Instructor Professions')
professions_bar_fig = px.bar(x=all_professions, y=professions_percentages, labels=dict(x='Professions', y='Percentage (out of Total Instructors)'), color_discrete_sequence=[bar_color])
professions_bar_fig.update_yaxes(range=[0,100])

professions_pie_fig = px.pie(values=professions_numbers, names=all_professions, color_discrete_sequence=bar_colors)
professions_pie_fig.update_traces(textinfo='value')
professions_pie_fig.update_traces(sort=False)

st.header('Distribution of Instructor Professions')
professions_bar_fig = px.bar(x=all_professions, y=professions_percentages, labels=dict(x='Professions', y='Percentage (out of Total Instructors)'), color_discrete_sequence=[bar_color])
professions_bar_fig.update_yaxes(range=[0,100])

professions_pie_fig = px.pie(values=professions_numbers, names=all_professions, color_discrete_sequence=bar_colors)
professions_pie_fig.update_traces(textinfo='value',hoverinfo='name',sort=False)
professions_pie_fig.update_layout(legend=dict(yanchor="top", y=-0.05, xanchor="left", x=0.01))

col1, col2 = st.columns(2, gap="large")
col1.subheader('by Percentage')
col1.caption("This bar graph depicts the percentage of instructors in each profession.")
col1.caption("Due to potential overlap, percentages may add up to greater than 100%.")
col1.plotly_chart(professions_bar_fig,use_container_width=True)
col2.subheader('by Frequency')
col2.caption("This pie chart depicts the number of instructors in each profession.")
col2.caption("Due to potential overlap, the numbers on the pie chart might be greater than the total number of instructors.")
col2.plotly_chart(professions_pie_fig,use_container_width=True)

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
#data['Instructor Rating'] = data['Instructor Rating'].astype(int)
course_rating = data['Instructor Rating']
student_count_to_course_rating_fig = px.scatter(x=student_count, y=course_rating, labels=dict(x='Student Count',y='Instructor Rating'), color_discrete_sequence=[bar_color])


student_count_to_course_rating_fig.update_xaxes(range=[-100,3200])
student_count_to_course_rating_fig.update_yaxes(range=[0,5.2])
student_count_to_course_rating_fig.update_traces(marker=dict(size=12, line=dict(width=1.5, color='Black')), selector=dict(mode='markers'))
st.subheader('Correlation between Student-to-Instructor Ratio and Instructor Rating')
st.caption("This scatterplot depicts how instructor ratings correspond to an instructor's student-to-instructor ratio, in order to determine how an instructor's abilities are affected by higher student counts.")
st.caption('Please note that some outlier values are not depicted on the graph for better visibility.')
st.plotly_chart(student_count_to_course_rating_fig)


#relation between location and course rating
rural_student_count = data[data['Student Location']=='Rural']['Student Count']
average_rural_student_count = round(rural_student_count.mean(), 2)
suburban_student_count = data[data['Student Location']=='Suburban']['Student Count']
average_suburban_student_count = round(suburban_student_count.mean(), 2)
urban_student_count = data[data['Student Location']=='Urban']['Student Count']
average_urban_student_count = round(urban_student_count.mean(), 2)
mix_student_count = data[data['Student Location'].str.contains('Mix of Areas', na=False)]['Student Count']
average_mix_student_count = round(mix_student_count.mean(), 2)

student_location = data['Student Location']
student_location = student_location.replace("A Mix of Areas", "Mix of Areas")


student_location_to_course_rating_fig = px.strip(x=student_location, y=course_rating, color_discrete_sequence=[bar_color], labels=dict(x='Student Location',y='Instructor Rating'))
student_location_to_course_rating_fig.update_yaxes(range=[0,5.4])


st.header('Statistics for Student Location')

measures = {
    'Location':['Mix of Areas', 'Rural', 'Suburban', 'Urban'],
    'Number of instructors':[len(mix_student_count), len(rural_student_count), len(suburban_student_count), len(urban_student_count)],
    'Average student count':[average_mix_student_count, average_rural_student_count, average_suburban_student_count, average_urban_student_count],
    'Median student count':[mix_student_count.median(), rural_student_count.median(), suburban_student_count.median(), urban_student_count.median()],
    'Smallest student count':[mix_student_count.min(), rural_student_count.min(), suburban_student_count.min(), urban_student_count.min()],
    'Largest student count':[mix_student_count.max(), rural_student_count.max(), suburban_student_count.max(), urban_student_count.max()]
}
measures_frame = pd.DataFrame(data=measures)
st.dataframe(measures_frame.style.format({'Average student count': "{:.2f}", 'Median student count': "{:.2f}", 'Smallest student count': "{:.2f}", 'Largest student count': "{:.2f}"}))

rural_course_rating = data[data['Student Location']=='Rural']['Instructor Rating']
suburban_course_rating = data[data['Student Location']=='Suburban']['Instructor Rating']
urban_course_rating = data[data['Student Location']=='Urban']['Instructor Rating']
mix_course_rating = data[data['Student Location'].str.contains('Mix of Areas', na=False)]['Instructor Rating']

#location_ratings = {
    #'Student Location':['Mix of Areas', 'Rural', 'Suburban', 'Urban'],
    #'1':[round((mix_course_rating==1).sum()/len(mix_course_rating), 4) * 100, round((rural_course_rating==1).sum()/len(rural_course_rating), 4) * 100, round((suburban_course_rating==1).sum()/len(suburban_course_rating), 4) * 100, round((urban_course_rating==1).sum()/len(urban_course_rating), 4) * 100],
    #'2':[round((mix_course_rating==2).sum()/len(mix_course_rating), 4) * 100, round((rural_course_rating==2).sum()/len(rural_course_rating), 4) * 100, round((suburban_course_rating==2).sum()/len(suburban_course_rating), 4) * 100, round((urban_course_rating==2).sum()/len(urban_course_rating), 4) * 100],
    #'3':[round((mix_course_rating==3).sum()/len(mix_course_rating), 4) * 100, round((rural_course_rating==3).sum()/len(rural_course_rating), 4) * 100, round((suburban_course_rating==3).sum()/len(suburban_course_rating), 4) * 100, round((urban_course_rating==3).sum()/len(urban_course_rating), 4) * 100],
    #'4':[round((mix_course_rating==4).sum()/len(mix_course_rating), 4) * 100, round((rural_course_rating==4).sum()/len(rural_course_rating), 4) * 100, round((suburban_course_rating==4).sum()/len(suburban_course_rating), 4) * 100, round((urban_course_rating==4).sum()/len(urban_course_rating), 4) * 100],
    #'5':[round((mix_course_rating==5).sum()/len(mix_course_rating), 4) * 100, round((rural_course_rating==5).sum()/len(rural_course_rating), 4) * 100, round((suburban_course_rating==5).sum()/len(suburban_course_rating), 4) * 100, round((urban_course_rating==5).sum()/len(urban_course_rating), 4) * 100]
#}

location_ratings = {
    'Student Location':['Mix of Areas', 'Rural', 'Suburban', 'Urban'],
    '1':[(mix_course_rating==1).sum(), (rural_course_rating==1).sum(), (suburban_course_rating==1).sum(), (urban_course_rating==1).sum()],
    '2':[(mix_course_rating==2).sum(), (rural_course_rating==2).sum(), (suburban_course_rating==2).sum(), (urban_course_rating==2).sum()],
    '3':[(mix_course_rating==3).sum(), (rural_course_rating==3).sum(), (suburban_course_rating==3).sum(), (urban_course_rating==3).sum()],
    '4':[(mix_course_rating==4).sum(), (rural_course_rating==4).sum(), (suburban_course_rating==4).sum(), (urban_course_rating==4).sum()],
    '5':[(mix_course_rating==5).sum(), (rural_course_rating==5).sum(), (suburban_course_rating==5).sum(), (urban_course_rating==5).sum()]
}

location_ratings_frame = pd.DataFrame(data=location_ratings)
location_to_rating_bar_fig = px.bar(data_frame=location_ratings_frame, x='Student Location', y=['1', '2', '3', '4', '5'], color_discrete_sequence=other_bar_colors, text_auto=True)
location_to_rating_bar_fig.update_layout(legend_title_text='Instructor Rating', yaxis_title='Number of Ratings')
st.subheader('Correlation between Student Location and Instructor Rating')
st.caption('This segmented bar graph depicts how instructor ratings differ based on student location. Each bar segement represents the number of instructors that received that particular rating value.')
st.plotly_chart(location_to_rating_bar_fig)


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
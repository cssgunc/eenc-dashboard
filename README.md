# Visualization Dashboard for Course Ratings
This dashboard provides an interactive visualization dashboard of data collected at the end of every event organized by the Environmental Educators of North Carolina. Below are the intended features of this interactive visualization dashboard.

## Filters
The dashboard provides filtering options based on class and area for different ratings. Users can also filter demographic data based on profession, location, class type, and date. Guidelines can be filtered based on profession, location, event type, and event name.

## Overall Statistics
The dashboard provides an overview of the overall statistics such as the number of respondents, course ratings, average ratings between online and in-person classes, average knowledge gain, and most popular classes. Users can also see trends over time using line charts.

## Demographic Data
The dashboard displays demographic data such as the profession of respondents, student count for each teacher, correlation between the number of students to course ratings, and location/rating. Users can filter data based on class, class type, and date.

## Different Ratings
The dashboard visualizes different ratings for courses, accessibility, instructors, and navigation using bar charts, line charts, and scatter plots.

## Guidelines
The dashboard displays any change in guidelines and improvement efforts. Users can filter data based on profession, location, event type, and event name.

## Technology Used
The dashboard is built using Python and various libraries such as Streamlit and Altair. It uses data from various sources to provide an interactive visualization.

## Getting Started
To run the dashboard, users need to install the required libraries and run the main.py file. The dashboard will be available at http://localhost:8501.
```
pip install streamlit altair pandas numpy
streamlit run main.py
```
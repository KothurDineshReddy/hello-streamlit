import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud
import warnings

warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)

# Load the dataset
df = pd.read_csv("ds_salaries.csv")
df = df.drop('Unnamed: 0', axis=1)
df['experience_level'].replace({'EN': 'Entry-Level', 'MI': 'Mid-Level', 'EX': 'Executive Level', 'SE': 'Senior'},
                                inplace=True)
df['employment_type'].replace({'PT': 'Part-Time', 'FT': 'Full-Time', 'CT': 'Contract', 'FL': 'Freelance'},
                              inplace=True)

# Sidebar for selecting the graph
selected_graph = st.sidebar.selectbox("Select a Graph", ["Word Cloud", "Top 10 Roles", "Total Jobs by Experience",
                                                          "Top 15 Countries", "Salary Distribution", "Salaries by Year",
                                                          "Salaries by Experience"])


def create_word_cloud():
    job_title_counts = df['job_title'].value_counts().to_dict()
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(job_title_counts)
    
    # Create a Matplotlib figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title('Word Cloud of Job Titles Based on Frequency', fontsize=16)
    
    # Display the Matplotlib figure using st.pyplot()
    st.pyplot(fig)

# Function to create Top 10 Roles graph
def create_top_10_roles():
    z = df.groupby('job_title', as_index=False)['salary_in_usd'].mean().sort_values(by='salary_in_usd',
                                                                                     ascending=False)
    z['salary_in_usd'] = round(z['salary_in_usd'], 2)
    fig = px.bar(z.head(10), x='job_title', y='salary_in_usd', color='job_title',
                 labels={'job_title': 'job title', 'salary_in_usd': 'avg salary in usd'},
                 text='salary_in_usd', template='seaborn', title='<b> Top 10 Roles in Data Science based on Average Pay')
    fig.update_traces(textfont_size=8)
    st.plotly_chart(fig)

# Function to create Total Jobs by Experience graph
def create_total_jobs_by_experience():
    fig = px.pie(df.groupby('experience_level', as_index=False)['salary_in_usd'].count().sort_values(by='salary_in_usd',
                                                                                                      ascending=False).head(
        10), names='experience_level', values='salary_in_usd', color='experience_level', hole=0.7,
                 labels={'experience_level': 'Experience level ', 'salary_in_usd': 'count'}, template='ggplot2',
                 title='<b>Total Jobs Based on Experience Level')
    fig.update_layout(title_x=0.5, legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))
    st.plotly_chart(fig)

# Function to create Top 15 Countries graph
def create_top_15_countries():
    location_counts = df.groupby('company_location', as_index=False)['experience_level'].count().sort_values(
        by='experience_level', ascending=False).head(15)
    fig = px.funnel(location_counts, y='company_location', x='experience_level',
                    color_discrete_sequence=['darkblue'],
                    labels={'experience_level': 'Count'},
                    template='seaborn',
                    title='<b>Top 15 Countries having maximum Data Science Jobs')
    st.plotly_chart(fig)

# Function to create Salary Distribution graph
def create_salary_distribution():
    fig = px.histogram(df, x='salary_in_usd', marginal='rug', template='seaborn',
                       labels={'salary_in_usd': 'Salary in USD'},
                       title='<b> Salary Distribution')
    st.plotly_chart(fig)

# Function to create Salaries by Year graph
def create_salaries_by_year():
    fig = px.violin(df, x='work_year', y='salary_in_usd', color='work_year',
                    color_discrete_sequence=['#3498db', '#2ecc71', '#e74c3c'],
                    labels={'work_year': 'Year', 'salary_in_usd': 'Salary in USD'},
                    template='seaborn',
                    title='<b>Data Science Salaries by Year')
    st.plotly_chart(fig)

# Function to create Salaries by Experience graph
def create_salaries_by_experience():
    fig = px.box(df, x='experience_level', y='salary_in_usd', color='experience_level',
                 template='ggplot2',
                 labels={'experience_level': 'Experience Level', 'salary_in_usd': 'Salary in USD'},
                 title='<b>Data Science Salaries by Experience')
    st.plotly_chart(fig)

# Main part of the Streamlit app
st.title("Data Science Jobs Analysis")
st.sidebar.header("Select a Graph")

# Create the selected graph based on the user's choice
if selected_graph == "Word Cloud":
    create_word_cloud()
    st.markdown("""
                Analysis:
                1. The above shown chart is a word cloud which is visual representation of word data. 
                2. The word cloud shows all the Job titles present in data world.
                3. Data scientist, Data Analyst, and Data Engineer are the most famous job roles.
                """)
elif selected_graph == "Top 10 Roles":
    create_top_10_roles()
    st.markdown(""" 
                Analysis:
                1. The chart provides a visual comparison of Avg salaries among the data science roles.\n
                2. The vertical axis represents the average salary in USD, ranging from 0 to 400,000+.\n
                3. The horizontal axis lists job titles.\n
                4. Top 3 roles with highest average salaries :\n
                  \ti.) Data Analytics Lead: 405,000.\n
                  \tii.) Principal Data Engineer: 328,333.\n
                  \tiii.) Financial Data Scientist: 275,000.
                 """)
    
elif selected_graph == "Total Jobs by Experience":
    create_total_jobs_by_experience()
    import streamlit as st

    st.markdown("""
                   Analysis:\n
                   1.The above shown graph is pie chart for jobs based on experience level.\n
                   2.We have 4 different categories in our chart.Senior,Mid Level, entry level and Executive level.\n
                   3.experienced people contribute to 46.1% of jobs present in the market.
                   
                   """)
    
elif selected_graph == "Top 15 Countries":
    create_top_15_countries()
    st.markdown("""
                   Analysis:\n
                   1.The above shown is a funnel graph of jobs distribution over different countries.\n
                   2.The size of bar shows the no of jobs present in the country .\n
                   3.on the Y-axis we have countries.\n
                   4.USA has the most no of Data related jobs.
                   
                   """)
    
elif selected_graph == "Salary Distribution":
    create_salary_distribution()
    st.markdown("""
                   Analysis:\n
                   1.The above graph is histogram of Salary Distribution.\n
                   2.On the x-axis we have salary in USD.\n
                   3.On the Y-axis we have count.\n
                   4.From the histogram we can observe that Majority of companies pay salaries ranging 80k to 120k.
                   
                   """)
elif selected_graph == "Salaries by Year":
    create_salaries_by_year()
    st.markdown("""
                   Analysis:\n
                   1.The above shown is violin graph of Data Science salaries over years.\n
                   2.Here we are comparing salaries over 3 years 2020,2021,2022.\n
                   3.From the chart we can observe that over the the salaries have been increasing.
                   """)
elif selected_graph == "Salaries by Experience":
    create_salaries_by_experience()
    st.markdown("""
                   Analysis:\n
                   1.The above shown graph is Box Plot of Data Science salaries by experience.\n
                   2.This plot represents four categories on the x-axis, corresponding to different experience levels: Mid- Level, Senior, Entry-Level, and Executive Level.\n
                   3.The y-axis shows the salary in USD, ranging from 0 to 600k (which suggests a range up to $600,000).\n
                   4.In this plot, the Executive Level category appears to have the highest median salary .\n
                   5.The Mid-Level and Senior categories have lower medians and a narrower interquartile range.\n
                   6.The Entry-Level category has the lowest median salary and the least variability.
                   
                   """)

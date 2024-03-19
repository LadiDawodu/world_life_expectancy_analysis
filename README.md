# Global Health Insights: Exploring Life Expectancy Factors



This project involves exploring and visualizing data related to life expectancy, GDP, BMI, adult mortality, 
and other factors across different countries. 
The data is retrieved from my MySQL database named work_life_expectancy, from the table worldlifeexpectancy.


Firstly a Python file, 'db_conn.py', contains the code to establish a connection to the MySQL database from Python. 
The 'get_conn()' function within this file utilizes the 'mysql.connector' library to connect to the database using the provided credentials.
When connection is successful , it returns the connection as an object, allowing for interaction with the database retrieval and analysis.

To use this connection function, a simple import (from src.db.conn import get_conn) into my 'main.py' Python script as needed, 
then it call 'get_conn()' to establish a connection to the MySQL database. **File Structure is important.**


# Python Libraries
- mysql.connector
- pandas
- matplotlib
- seaborn
- plotly.express,
- plotly.graph_objects


# Data Cleaning and Exploration

**Data Cleaning**:
Identified and removed duplicate entries in the database.
Filled missing values in the 'status' column based on country status.
Calculated missing 'Life expectancy' values based on adjacent years.
Resolved data quality issues in 'Adult mortality' by adjusting values.
Investigated and addressed discrepancies in nutritional factors data.

**Exploratory Data Analysis (EDA)**:
Explored trends in life expectancy, GDP, BMI, and adult mortality over time and across countries.
Investigated correlations between various factors such as GDP and life expectancy, status (developed/developing) and life expectancy, BMI and life expectancy, etc.


# Visualizations

**Life Expectancy Analysis**:
Plotted the average life expectancy by year to identify trends over time.

**GDP Correlation**:
Explored the correlation between GDP and life expectancy using a scatter plot.

**Countries with GDP Lower than 1500**:
Visualized the count of countries with GDP lower than 1500, highlighting the countries with the lowest GDP count.

**Developed/Developing Status and Life Expectancy**:
Analyzed the correlation between the developed/developing status of countries and life expectancy.

**BMI Comparison**:
Explored the correlation between BMI and life expectancy across different countries.

**Adult Mortality Correlation**:
Investigated the correlation between adult mortality and life expectancy in the United Kingdom, visualizing the rolling total of adult mortality.

# Conclusion
This project provides insights into various factors affecting life expectancy across different countries, including socioeconomic indicators like GDP, BMI, and health-related factors like adult mortality.
The visualizations generated from the analysis help in understanding these correlations and trends effectively, and in some ways shows that not everything is an obvious correlation.


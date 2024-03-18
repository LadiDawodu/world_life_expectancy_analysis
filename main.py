import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.db.conn import get_conn
import plotly.express as px



# Database

conn = get_conn()

# SQL

cursor = conn.cursor()

# Average life expectancy by Year

query = """select year, round(AVG(`Life expectancy`),1) as AVG_Life_Expectancy
from worldlifeexpectancy
#where (`Life expectancy`) <> 0
#and (`Life expectancy`) <> 0
group by year
order by year asc;"""
cursor.execute(query)
data = cursor.fetchall()

year = [row[0] for row in data]
Avg_Life_Expectancy = [row[1] for row in data]


plt.figure(figsize=(10,6))
sns.scatterplot(x=year, y=Avg_Life_Expectancy)
#sns.lineplot(x=countries, y=min_life_exp)
plt.title('Life Expectancy')
plt.xlabel('Country')
plt.ylabel('Life Expectancy')
plt.show()


#------------------------------------------------

# Check GDP correlation and Life expectancy

conn = get_conn()

cursor= conn.cursor()

query="""
select country, round(AVG(`Life expectancy`),1) as AVG_Life_Expectancy, round(AVG(GDP),2) as Avg_GDP
from worldlifeexpectancy
group by country
having Avg_GDP > 0
and  AVG_Life_Expectancy > 0
order by Avg_GDP asc;
"""

cursor.execute(query)
data = cursor.fetchall()
country = [row[0] for row in data]
avg_life_exp = [row[1] for row in data]
avg_gdp = [row[2] for row in data]

data = pd.DataFrame({'Country': country, 'Average Life Expectancy': avg_life_exp, 'Avg_GDP': avg_gdp})


fig = px.scatter(
        data, x='Avg_GDP', y='Average Life Expectancy',hover_name='Country',
        labels={'Avg_GDP': 'Average GDP', 'avg_life_exp': 'Average Life Expectancy'},
        title="GDP correlation and Life expectancy")
        #hoverformat="Country: %{text}<br>Avg GDP: %{x:.2f}<br>Life Exp: %{y:.1f}"

fig.update_traces(marker=dict(color='red', line=dict(color='red', width=1)))
fig.show()


import plotly.graph_objects as go

conn = get_conn()

cursor= conn.cursor()

query="""
select
SUM(case when GDP >= 1500 then 1 else 0 end) High_GDP_Count,
#round out the decimals (too many)
round(AVG(case when GDP >= 1500 then `Life expectancy`  else null end),2) AVG_GDP_Life_expectancy,
SUM(case when GDP <= 1500 then 1 else 0 end) Low_GDP_Count,
#round out the decimals (too many)
round(AVG(case when GDP <= 1500 then `Life expectancy`  else null end),2) Lowest_AVG_GDP_Life_expectancy
from worldlifeexpectancy;
"""

cursor.execute(query)
data = cursor.fetchall()
High_GDP_Count = data[0][0]
Low_GDP_Count = data[0][2]
High_GDP_Life_Exp = data[0][1]
Low_GDP_Life_Exp = data[0][3]

data = pd.DataFrame({'Category': ['High_GDP_Count', 'Low_GDP_Count', 'High_GDP_Life_Exp', 'Low_GDP_Life_Exp'],
'Value':[High_GDP_Count, Low_GDP_Count, High_GDP_Life_Exp, Low_GDP_Life_Exp]})

#color_mapping={'High_GDP_Count' : ' Geyser_r ',
#               'Low_GDP_Count':'Geyser','High_GDP_Life_Exp':'indianred', 'Low_GDP_Life_Exp':'Geyser_r'
        
#}
data.sort_values('Value', ascending=False, inplace=True)

fig = px.bar( 
             data, x='Category', y='Value', template="simple_white", #integrated template
             title='<b>Countires GDP Count</b><br><sup>Lower than 1500 GDP</sup>',
             text=data['Value'].apply(lambda x: f'{x:.0f}', #apply formatted values
             ), )
             
             #title="Countires that have a higher GDP than 1500",
             #color=color_mapping)
        #hoverformat="Country: %{text}<br>Avg GDP: %{x:.2f}<br>Life Exp: %{y:.1f}"


fig.update_xaxes(tickfont=dict(size=12), title_text='', showticklabels=False )
fig.update_yaxes(tickfont=dict(size=12),title_text='')


#Highlight the Most  important category

hightlighted_bar = 'Low_GDP_Count'


fig.update_traces(marker_color=['indianred' if x == hightlighted_bar else 'grey' for x in data['Category']],)

fig.add_trace(
    go.Bar(x=['Low_GDP_Count'], y=[0], marker=dict(color='indianred'), showlegend=True, name='Lowest GDP Count')
)


fig.show()

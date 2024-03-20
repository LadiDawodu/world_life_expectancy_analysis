import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.db.conn import get_conn
import plotly.express as px
import plotly.graph_objects as go
#from plotly.graph_objs import Scatter




# Average life expectancy by Year

# Connect SQL
conn = get_conn()


cursor = conn.cursor()


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
data = pd.DataFrame({'Year': year, 'Avg Life Exp': Avg_Life_Expectancy})

data.sort_values('Year', ascending=False, inplace=True)

fig = px.histogram(
        data, x='Year', y='Avg Life Exp',
        template='simple_white',
        title="<b>Average World life expectancy </b><br><sup>By Year<sup>",
        hover_name='Avg Life Exp'
        
        )
thirteenth_value = sorted(set(data['Avg Life Exp']))[2]

fig.update_traces(marker_color=['indianred' if x == thirteenth_value else 'grey' for x in data['Avg Life Exp']],hovertemplate='%{x}')


fig.add_trace(
    go.Bar(x=['Avg Life Exp'], y=[0], marker=dict(color='indianred'), showlegend=True, name='Avg Life Exp')
)

fig.update_xaxes(tickfont=dict(size=12), title_text='', showticklabels=False )
fig.update_yaxes(tickfont=dict(size=12),title_text='')
fig.show()
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
        data, x='Average Life Expectancy', y='Avg_GDP',hover_name='Country',
        template="simple_white", color='Average Life Expectancy', color_continuous_scale='Reds',
        #labels={'Avg_GDP': 'Average GDP', 'avg_life_exp': 'Average Life Expectancy'},
        title="<b>GDP correlation </b><br><sup>& Life expectancy<sup>", custom_data=data[['Country','Average Life Expectancy', 'Avg_GDP' ]])
        #hoverformat="Country: %{text}<br>Avg GDP: %{x:.2f}<br>Life Exp: %{y:.1f}"

fig.update_traces(hovertemplate="<b>Country</b>: %{customdata[0]}<br>"
                 "<b>Avg Life Exp</b>: %{customdata[1]:.1f} years<br>"
                 "<b>Avg GDP</b>: %{customdata[2]:.2f}")
fig.update_yaxes(tickfont=dict(size=12),title_text='')
fig.update_xaxes(tickfont=dict(size=12),title_text='', showticklabels=False)

fig.show()

#------------------------------------------------

# Countries GDP Count Lower than 1500 GDP

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

# Fetch data agrregate
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
             #apply formatted values
             text=data['Value'].apply(lambda x: f'{x:.0f}', 
             ), )
             
             #title="Countires that have a higher GDP than 1500",
             #color=color_mapping)
        #hoverformat="Country: %{text}<br>Avg GDP: %{x:.2f}<br>Life Exp: %{y:.1f}"


#Remove labels on both axis

fig.update_xaxes(tickfont=dict(size=12), title_text='', showticklabels=False )
fig.update_yaxes(tickfont=dict(size=12),title_text='')


#Highlight the Most important category

hightlighted_bar = 'Low_GDP_Count'

fig.update_traces(marker_color=['indianred' if x == hightlighted_bar else 'grey' for x in data['Category']],hovertemplate='%{x}')

# Add color to only the important metric: Low_GDP_Count
fig.add_trace(
    go.Bar(x=['Low_GDP_Count'], y=[0], marker=dict(color='indianred'), showlegend=True, name='Lowest GDP Count')
)

fig.show()



#------------------------------------------------

# Seeing Correlation between 
# Developed/Developing status and Life expectancy
conn = get_conn()
cursor = conn.cursor()

query = """
select status, count(distinct country), 
round(avg(`Life expectancy`),1) as AVG_Life_Expectancy
from worldlifeexpectancy
group by status;
"""

cursor.execute(query)
data = cursor.fetchall()

status = [row[0] for row in data ]
country = [row[1] for row in data]
Avg_Life_Exp = [row[2] for row in data]


data = pd.DataFrame({
        'Status': status,
        'Country Count': country,
        'AVG_Life_Exp': Avg_Life_Exp
})

data.sort_values('Country Count', ascending=False, inplace=True)

fig = px.bar(
        data, x='Status', y='Country Count', template="simple_white", 
        title='<b>Developed/Developing status</b><br><sup>& Life expectancy</sup>',
        text=data['Country Count'].apply(lambda x: f'{x:.0f}',),
        custom_data=data[['AVG_Life_Exp']]
        )

hightlighted_bar = 'Developing'

fig.update_traces(marker_color=['indianred' if x == hightlighted_bar else 'grey' for x in data['Status']],hovertemplate='%{x} -' + ' Avg.Life Expectancy: %{customdata[0]:.1f}')

# Add color to only the important metric: Low_GDP_Count
fig.add_trace(
    go.Bar(x=['Developing'], y=[0], marker=dict(color='indianred'), showlegend=True, name='Developing Countries')
)

fig.update_xaxes(tickfont=dict(size=12), title_text='', showticklabels=False )
fig.update_yaxes(tickfont=dict(size=12),title_text='')



fig.show()

#-----------------------------------------------------------------

# BMI comparison on each countries life expectancy

conn = get_conn()
cursor = conn.cursor()

query = """
select country, round(AVG(`Life expectancy`),1) as AVG_Life_Expectancy, round(AVG(BMI),2) as Avg_BMI
from worldlifeexpectancy
group by country
having Avg_BMI > 0
and  AVG_Life_Expectancy > 0
order by Avg_BMI asc;
"""

cursor.execute(query)
data = cursor.fetchall()

country = [row[0] for row in data]
AVG_Life_Exp = [row[1] for row in data]
Avg_BMI = [row[2] for row in data]

data = pd.DataFrame({
        'Country': country,
        'Avg_BMI': Avg_BMI,
        'AVG_Life_Exp': AVG_Life_Exp
})


fig = px.scatter(data, x='AVG_Life_Exp', y='Avg_BMI', template='simple_white', color='Avg_BMI', color_continuous_scale='Reds',  
title='<b>BMI comparison</b><br><sup> based on countries life expectancy</sup>', custom_data=['Country', 'Avg_BMI', 'AVG_Life_Exp'])


fig.update_traces(hovertemplate="<b>Country</b>: %{customdata[0]}<br>"
                 "<b>Avg Life Exp</b>: %{customdata[1]:.1f} years<br>"
                 "<b>Avg BMI</b>: %{customdata[2]:.2f}")

fig.update_xaxes(tickfont=dict(size=12), title_text='')
fig.update_yaxes(tickfont=dict(size=12),title_text='', showticklabels=False)
#fig.update_traces(hovertemplate='%{x} -' + 'Avg_BM: %{customdata[0]:.1f} )
fig.show()


#--------------------------------------------------------------------

# Adult mortality correlation to Life Expectancy

conn = get_conn()
cursor = conn.cursor()


query = """
select country, year, `Life expectancy`, `Adult mortality`, 
sum(`Adult mortality`)over(PARTITION by country order by Year) as Rolling_Adult_Life_Mortality
from worldlifeexpectancy
where country like '%United Kingdom%';
"""

cursor.execute(query)
data = cursor.fetchall()

country = [row [0] for row in data]
year = [row [1] for row in data]
Life_Exp = [row [2] for row in data]
Adult_Mortality = [row [3] for row in data]


data = pd.DataFrame({
        'Country': country,
        'Year': year,
        'Life_Exp': Life_Exp,
        'Adult_Mortality': Adult_Mortality
})

fig = px.line(
        data, x='Year', y='Adult_Mortality',
        template='simple_white', custom_data=['Year', 'Life_Exp', 'Adult_Mortality'],
        title='<b>Adult mortality correlation</b><br><sup> In the UK</sup>', markers=True,
        
        
)


fig.add_trace(
    go.Scatter(x=['Adult_Mortality'],y=[], marker=dict(color='indianred'))
)




fig.update_traces(
                  hovertemplate=
                 "<b>Year</b>: %{customdata[0]}<br>"
                 "<b>Life Exp</b>: %{customdata[1]:.1f} years<br>"
                 "<b>Adult Mortality</b>: %{customdata[2]:.1f} years<br>", line_color='indianred',
                 name='Adult Mortality', showlegend=True, hoverinfo='skip'
                 )



y_values = sorted(data['Year'].unique())
#x_values = sorted(data['Year'].unique())

fig.update_xaxes(tickfont=dict(size=12), title_text='')
fig.update_yaxes(tickfont=dict(size=12),title_text='', 
                 categoryarray=y_values, showticklabels=False)
fig.update_layout(showlegend=True)
fig.show()
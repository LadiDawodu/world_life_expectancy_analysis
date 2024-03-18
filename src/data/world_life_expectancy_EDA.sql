#---------------------------------Data Cleaning---------------------------------------

show databases;
use  work_life_expectancy;
select * from worldlifeexpectancy;

#-------------------------------------------------------------------------------------

# Identified 3 duplicates / Now remove
select Country, year, concat(country, year), count(concat(country, year)) 
as "Concat/Year" from worldlifeexpectancy
group by Country, Year, concat(country, year)
Having count(concat(country, year)) > 1;


# Identify with ROW_ID

select *
from (
	select row_id, 
	concat(country, year),
	ROW_NUMBER() over(Partition by concat(country, year) 
	order by concat(country, year)) as row_dupe
	from worldlifeexpectancy
) as row_subquery

where row_dupe > 1;



# Using subquery to delete exact duplicates with using ROW_ID as a uniqueID
delete from worldlifeexpectancy
where row_id in (

select row_id
from (
	select row_id, 
	concat(country, year),
	ROW_NUMBER() over(Partition by concat(country, year) 
	order by concat(country, year)) as row_dupe
	from worldlifeexpectancy
	) 	
	as row_subquery

	where row_dupe > 1
);


# Missing/blank fields NOT NULL fields (in status) Found 7

select * from 
worldlifeexpectancy
where status = '';

select distinct(status)
from worldlifeexpectancy
where status <> ''; 



# Fill the missing fields

select distinct(country)
from worldlifeexpectancy
where status = 'Developing';


# Error Code: 1093. You 
# can't specify target table 'worldlifeexpectancy' for update in FROM clause

#update worldlifeexpectancy
#set status = 'Developing'
#where country in (

#	select distinct(country)
#	from worldlifeexpectancy
#	where status = 'Developing'
#);


# Use self join to update developing

update worldlifeexpectancy table1
join worldlifeexpectancy table2
on table1.country = table2.country 
set table1.status = 'Developing'
where table1.status = ''
and table2.status <> ''
and table2.status = 'Developing';



# Do the same for developed

update worldlifeexpectancy table1
join worldlifeexpectancy table2
on table1.country = table2.country 
set table1.status = 'Developed'
where table1.status = ''
and table2.status <> ''
and table2.status = 'Developed';

# Check any more missing fields:

select * from 
worldlifeexpectancy
where status = '';

#-------------------------------------------------------------------------------------


# Missing/blank fields NOT NULL fields (in life expecyancy) Found 7

select * from 
worldlifeexpectancy
where `Life expectancy` = '';



# Looking at 'Life expectancy' it seems the field is going up by avergaes,
# there isn't an explicit formula for it. BUT looking at it the numbers seem to increase
# by a steady AVG

select country, year, `Life expectancy`  from 
worldlifeexpectancy
where `Life expectancy` = '';

# Using self-joins:

select t1.country, t1.year, t1.`Life expectancy`, t2.country, 
t2.year, t2.`Life expectancy`, t3.country, 
t3.year, t3.`Life expectancy`,
# round the output to one decimal
Round((t2.`Life expectancy` + t3.`Life expectancy`)/2,1)
from 
worldlifeexpectancy t1 
join worldlifeexpectancy t2
	on t1.country = t2.country
	and t1.year = t2.year - 1
join worldlifeexpectancy t3
	on t1.country = t3.country
	and t1.year = t3.year + 1
where t1.`Life expectancy` = '';

#Update inital `Life expectancy` fields

update worldlifeexpectancy t1 
join worldlifeexpectancy t2
	on t1.country = t2.country
	and t1.year = t2.year - 1
join worldlifeexpectancy t3
	on t1.country = t3.country
	and t1.year = t3.year + 1
set t1.`Life expectancy` = Round((t2.`Life expectancy` + t3.`Life expectancy`)/2,1);

# Recheck al empty fields:

select country, year, `Life expectancy`  from 
worldlifeexpectancy
where `Life expectancy` = '';



#-------------------------------Expectancy Exploratory Data------------------------------

select country, min(`Life expectancy`), max(`Life expectancy`)
from worldlifeexpectancy
group by country
order by country desc;

# Find the difference between MAX - MIN

select country, 
min(`Life expectancy`), max(`Life expectancy`),
round(max(`Life expectancy`) - min(`Life expectancy`),1) as Increase_in_Life
from worldlifeexpectancy
group by country
having min(`Life expectancy`) <> 0
and max(`Life expectancy`) <> 0
order by Increase_in_Life desc;



# found Data quality issue multiple counts of 0

select country, year, count(`Life expectancy`) as count from 
worldlifeexpectancy
where `Life expectancy` = 0
group by country, year;


#-------------------------------------------------------------------------------------


# Average life expectancy by Year

select year, round(AVG(`Life expectancy`),1) as AVG_Life_Expectancy
from worldlifeexpectancy
#where (`Life expectancy`) <> 0
#and (`Life expectancy`) <> 0
group by year
order by year asc;

#-------------------------------------------------------------------------------------

# Check GDP correlation and Life expectancy

# ALTER TABLE worldlifeexpectancy MODIFY GDP decimal;

select country, round(AVG(`Life expectancy`),1) as AVG_Life_Expectancy, round(AVG(GDP),2) as Avg_GDP
from worldlifeexpectancy
group by country
having Avg_GDP > 0
and  AVG_Life_Expectancy > 0
order by Avg_GDP asc;


# Check the amount of rows that have an higher GDP than 1500
# 1326 found

select
SUM(case when GDP >= 1500 then 1 else 0 end) High_GDP_Count,
#round out the decimals (too many)
round(AVG(case when GDP >= 1500 then `Life expectancy`  else null end),2) AVG_GDP_Life_expectancy,
SUM(case when GDP <= 1500 then 1 else 0 end) Low_GDP_Count,
#round out the decimals (too many)
round(AVG(case when GDP <= 1500 then `Life expectancy`  else null end),2) Lowest_AVG_GDP_Life_expectancy
from worldlifeexpectancy;


#-------------------------------------------------------------------------------------

# Seeing Correlation between Developed/Developing status and Life expectancy

# This doesnt give a clear insight into how many countries are 'Developed' or 'Developing'
# So results could look skewed one way
select status, round(avg(`Life expectancy`),1) as AVG_Life_Expectancy
from worldlifeexpectancy
group by status;

# Use COUNT to find Countries Developed' or 'Developing'

select status, count(distinct country)
from worldlifeexpectancy
group by status;

# Combined results

select status, count(distinct country), round(avg(`Life expectancy`),1) as AVG_Life_Expectancy
from worldlifeexpectancy
group by status;


#-------------------------------------------------------------------------------------


# BMI comparison on each countries life expectancy

# Intrestingly lower BMI lower life expectnacy
# Higher BMI higher life expectancy
select country, round(AVG(`Life expectancy`),1) as AVG_Life_Expectancy, round(AVG(BMI),2) as Avg_BMI
from worldlifeexpectancy
group by country
having Avg_BMI > 0
and  AVG_Life_Expectancy > 0
order by Avg_BMI asc;


#-------------------------------------------------------------------------------------


# Adult mortality correlation to Life Expectancy (rolling total)


# Some data qaulity issue in Adult Mortality found, 0s not read for example 8 should be 80
# 7 should be 70, so all 10s are not being read
select country, year, `Life expectancy`, `Adult mortality`, 
sum(`Adult mortality`)over(PARTITION by country order by Year) as Rolling_Adult_Life_Mortality
from worldlifeexpectancy;
#where country like '%United Kingdom%';

# Update data qaulity

UPDATE worldlifeexpectancy
SET `Adult mortality` = `Adult mortality` * 10
WHERE `Adult mortality` < 10;


# With Data Quality change and UK specify

select country, year, `Life expectancy`, `Adult mortality`, 
sum(`Adult mortality`)over(PARTITION by country order by Year) as Rolling_Adult_Life_Mortality
from worldlifeexpectancy
where country like '%United Kingdom%';


#-------------------------------------------------------------------------------------

# Nutritional Factors (thinness) / Status ? Life expectancy

select country, `Life expectancy`, `thinness  1-19 years`, `thinness 5-9 years`
from worldlifeexpectancy
where `Life expectancy` > 0
order by`Life expectancy` asc;




# Looking at this There is a disproportionate amount of countries 
# with high avg_life_exp and low thinness both 1-19 and 5-9, who are mostly developed
# Or in the western part of the world.
select
country, status, 
round(avg( `Life expectancy`),2) as avg_life_exp,
ROUND(avg(`thinness  1-19 years`),2) as avg_thinness_1_19,
ROUND(avg(`thinness 5-9 years`),2) as avg_thinness_5_9
from worldlifeexpectancy
where `Life expectancy` > 0
group by country, status
order by avg_life_exp desc;
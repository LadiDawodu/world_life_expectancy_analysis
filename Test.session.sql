SELECT Country, year, concat(country, year), count(concat(country, year)) 
AS "Concat/Year" FROM worldlifeexpectancy
GROUP BY Country, Year, concat(country, year)
HAVING count(concat(country, year)) > 1;


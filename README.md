# NL to SQL.

In the ERA of AI, many customers want to handle their data with natural language. Since DW era, many vendors have suggested their capabilities - easy use like natural language. But all was failed. 

But with modern LLM, we could archieve the proper level of this capability - natural language to SQL. 

I suggest 4 different architectures to handle NL SQL conversion. 


1. Direct Conversion

2. SQL to Natural Language & Search similar SQL

3. BI Dashboard search (with Looker dashboard)

4. NL to SQL conversion via symantic Layer (with Looker symantic layer)

5. Step by Step approach

All architecture has very similar issues and some issues can be solved by symantic layer supported by Looker. 


## Direct Conversion. 

Direct Conversion is very efficient to convert NL to simple SQL - The important point here is that it is SQL that is simple, not a natural language query that is simple.

What's the difference ?

For example, (Case #1)

"I want to see average salary in the 'construction' industry" - It's very simple natural language query. It's matching SQL might be the following. 

"select average(salray) from salary_table where industry = 'construction' and year = '2023'"

But, (Case #2)

"I want to see average salary YoY trends in 3 years." - It's also very simple request. but it's matching SQL is very different. 

"select average_salary / lag(1, average_salary) over (partition by registration_year order by registration_year asc) as salary_yoy from (select registration_year, average(salary) from salary_table where registration_year between '2020' and '2023') limit 3"

It's very complex SQL. 

Direction conversion is very suitable for the case #1. 

With more instructions and guides prompts can help LLM to make more complex SQLs but it's conversion ratio is not sufficient in many cases.

Overall architecture is below. 

![alt Architecture image](resources/1.direct_conversion.png "Title")

[Implementation Example.](nl_to_sql1.ipynb)



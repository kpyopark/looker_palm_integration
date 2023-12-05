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


## 1. Direct Conversion

Direct Conversion is very efficient to convert NL to simple SQL - The important point here is that it is SQL that is simple, not a natural language query that is simple.

What's the difference ?

For example, (Case #1)

"I want to see average salary in the 'construction' industry" - It's very simple natural language query. It's matching SQL might be the following. 

``` SQL
  select average(salray) from salary_table where industry = 'construction' and year = '2023'
```

But, (Case #2)

"I want to see average salary YoY trends in 3 years." - It's also very simple request. but it's matching SQL is very different. 

```SQL
  select average_salary / lag(1, average_salary) over (partition by registration_year order by registration_year asc) as salary_yoy 
    from (select registration_year, average(salary) from salary_table where registration_year between '2020' and '2023') 
  limit 3
```

It's very complex SQL. 

Direction conversion is very suitable for the case #1. 

With more instructions and guides prompts can help LLM to make more complex SQLs but it's conversion ratio is not sufficient in many cases.

Overall architecture is below. 

![alt Architecture image](resources/1.direct_conversion.png "Title")

[Implementation Example.](nl_to_sql1.ipynb)


## 2. SQL to Natural Language & Search similar SQL

Many companies already have a lot of analytic assets, such as pre-configured SQL queries. Even dashboards in BI tools often generate the same SQL queries and store them in the database. Marketing teams often use pre-defined segmentation rules, which can be modified by simply changing filter values. In these cases, SQL to NL & Search is a good approach.

Especially, when the pre-defined SQLs are very complex and static, it's very useful

For example,

Question : "What are the five brands that are positioned as high-end in the swimwear and sportswear category ?"

```SQL
  with average_price_per_category as (
    select category, average(retail_price) as average_price from products
    group by category
  ),
  average_price_per_category_brand as (
    select category, brand, average(retail_prince) as average_price from products
    group by category, brand
  ),
  select a.average_price / b.average_price as price_ratio, brand
    from average_price_per_category_brand a join average_price_per_category b on (a.category = b.cartegory)
  where category in ('Swim', 'Suits & Sport Coats')
  order by 1 desc 
  limit 5

```

it's very difficult to suggest the guideline into LLM on prompt. 

Overall architecture is very similar with direct conversion. But in this architecture crawls the SQL itself includes schema. 

![alt Architecture image](resources/2.sql_to_nl_to_sql.png "Title")

[Implementation Example.](nl_to_sql2.ipynb)



## 3. NL to Looker Dashboard

Looker Dashboard can show business reports in one page. 

Dashboard can describe its own business goal. 

This architecture is very similar with type #2. Sql to NL & search. 



## 4. NL to Looker View

As you know LLM can leverage its capabilities with some hardened framework. (For example, LLMMath chain)

Looker Query Maker is a kind of solution for this. 

Looker can solve the following issues during converting NL to SQL.

1. Business context suggestion
  : Looker 'Explore' can expose the relationships between related tables. 

2. Filter value adjustment
  : Looker 'Filter' can solve various filter values and operators. 

3. Complex Query generation
  : Looker 'Dimension/Measure' attributes can solve complex SQL generation.

If we could choice 'wanted' columns, Looker can make complex SQL via selected dimensions and Measures. 
It's a very great feature for LLM to make SQL easily. 


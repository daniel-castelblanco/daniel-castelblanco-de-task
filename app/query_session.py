


top_rank_book_2022_query = """
with books2022 as (
select  title, "rank", created_date 
from "Books" b
where EXTRACT(YEAR FROM created_date::date) = 2022
and rank <=3
)
select  title, count(title) times_top
from books2022
group by title
order by times_top desc
limit 1"""


top_3_lists_unique_books_query = """
with unique_books as (
select b.list_id,l.list_name, count(distinct title) unique_books
from "Books" b
left join "Lists" l on b.list_id = l.list_id
group by b.list_id, l.list_name 
order by 3 asc
)
select *
from unique_books
order by unique_books asc
limit 3
"""


top_5_publishers_query = """
with quarterly_point_by_rank as (
select
	publisher,
	extract(year from TO_DATE(created_date, 'YYYY-MM-DD')) as year,
	TO_CHAR(TO_DATE(created_date,'YYYY-MM-DD'),'Q') as quarter,
	SUM(case
            when "rank" = 1 then 5
            when "rank" = 2 then 4
            when "rank" = 3 then 3
            when "rank" = 4 then 2
            when "rank" = 5 then 1
            else 0
        end) as points
from
	"Books"
where	TO_DATE(created_date, 'YYYY-MM-DD') >= '2021-01-01'
and TO_DATE(created_date,'YYYY-MM-DD') < '2024-01-01'
group by
	publisher,
	year,
	quarter
order by
	year desc,
	quarter desc,
	4 desc
),
ranked_quarterly as (
select
	year,
	quarter,
	publisher,
	SUM(points) as total_points,
	rank() over (partition by year, quarter order by SUM(points) desc) as quarterly_rank
from
	quarterly_point_by_rank
group by
	year,
	quarter,
	publisher
order by
	year desc,
	quarter desc,
	4 desc
)
select	year,
		quarter,
		publisher,
		total_points,
		quarterly_rank
from ranked_quarterly
where quarterly_rank <= 5
"""


teams_books_review_query = """
with book_teams_2023 as (
    select
        title,
        "rank",
        created_date,
        case
            when "rank" = 1 then 'Jake'
            when "rank" = 3 then 'Pete'
            else null
        end as team
    from
        public."Books"
    where
        extract(year from to_date(created_date, 'YYYY-MM-DD')) = 2023
        and ("rank" = 1 or "rank" = 3)
),
ordered_books as (
    select
        title,
        "rank",
        team,
        created_date,
        row_number() over (partition by title order by created_date) as rn
    from
        book_teams_2023
)
select
    title,
    "rank",
    team,
    created_date
from
    ordered_books
where
    rn = 1
order by
    created_date;
"""
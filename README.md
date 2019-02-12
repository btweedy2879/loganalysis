# News database analytics
This project creates a number of analytical reports on data found 
in the news database.  This project uses python3.

## Required Librarys
[Psycopg2](http://initd.org/psycopg/docs/)

## Instructions.

The following view was created to support this program.  You can run
this query from the psql command prompt.:
```
create view log_stats as 
select E.day, errors, requests, 100*(errors::decimal/requests) as error_percentage
    from
        (
            select date_trunc('day', time) as "day", count(*) as errors from log
            where status not like '%200%'
            group by "day"
        ) as E
    join (
            select date_trunc('day', time) as "day", count(*) as requests from log
            group by "day"
        ) as R on E.day = R.day
    group by e.day, errors, r.requests;
```

Once the view has been created, simply run ```python news_reports.py```


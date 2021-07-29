import os
import psycopg2

def connect_postgres():
    conn = psycopg2.connect(
        host="localhost",
        database="medium",
        user="postgres",
        password=os.environ['Postgres_secret'])

    return conn


published_articles_per_year =   """
                                SELECT date_part('year', published), avg(clap_count), count(clap_count)
                                FROM public.scraper_articles
                                group by date_part('year', published)
                                ORDER BY date_part('year', published)
                                """
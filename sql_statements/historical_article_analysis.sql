SELECT date_part('year', published), avg(clap_count), count(*)
FROM public.scraper_articles
group by date_part('year', published)
ORDER BY date_part('year', published)
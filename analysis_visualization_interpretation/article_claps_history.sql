SELECT date_part('year', published) as year_published, 
		avg(clap_count) as clap_count_avg, 
		count(clap_count) as number_articles, 
		avg(voter_count) as voter_count_avg,
		max(published) as last_date_published
FROM scraper_articles
group by date_part('year', published)
ORDER BY date_part('year', published)
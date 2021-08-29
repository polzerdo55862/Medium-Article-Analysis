SELECT * FROM public.scraper_articles
left join on scraper_articles
(
Select *,
       CASE 
	   		WHEN count<=3 THEN '0 - 3'
            WHEN count >3 AND COUNT <= 6 then '4 - 6'
			ElSE '> 6'
       END 
	   AS count_bin
from
(
SELECT article_id, count(*) FROM public.scraper_figcaptions
group by article_id
) as X
) as y
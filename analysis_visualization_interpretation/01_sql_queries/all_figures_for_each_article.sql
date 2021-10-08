Select *,
       CASE 
	   		WHEN count<=3 THEN '0 - 3'
            WHEN count >3 AND COUNT <= 6 then '4 - 6'
			ElSE '> 6'
       END 
	   AS bin,
	  CASE 
	   		WHEN count<=3 and avg is Null THEN 0
			ElSE count
       END 
	   AS count_real
from
(	
	select avg(id), article_id, count(*) from
	(
		SELECT X.id, Y.id as article_id FROM public.scraper_figcaptions as X
		right join public.scraper_articles as Y
		on X.article_id = Y.id
	) as BN
	group by article_id
	
) as K
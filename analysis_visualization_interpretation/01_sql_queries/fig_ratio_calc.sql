SELECT
    article_id, source_img_rel, clap_count, url, count_images
FROM
	
(	
select article_id, avg(source_img) as source_img_rel, 
	count(caption) as count_images from 
(
SELECT article_id, caption,
       CASE 
		   		WHEN Upper(caption) LIKE '%UNSPLASH%' THEN 0
			WHEN Upper(caption) LIKE '%GIVEY%' THEN 0
	
			WHEN Upper(caption) LIKE '%AUTHOR%' THEN 1
			WHEN Upper(caption) LIKE '% ME%' THEN 1
	
			WHEN caption like '%https%' THEN 0
			WHEN caption like '%http%' THEN 0
			WHEN Upper(caption) like '%FROM%' THEN 0
			WHEN caption like '%[%]%' THEN 0
			WHEN Upper(caption) like '%IMAGE BY%' THEN 0
            ElSE 100
       END 
	   AS source_img
FROM public.scraper_figcaptions
) as X
where source_img < 5
group by article_id
) as figures

LEFT JOIN scraper_articles articles ON figures.article_id = articles.id
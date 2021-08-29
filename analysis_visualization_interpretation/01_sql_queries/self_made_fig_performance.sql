SELECT
    article_id, source_img_rel, clap_count, url, count_images
FROM
	
(	
select article_id, avg(source_img) as source_img_rel, 
	count(caption) as count_images from 
(
SELECT article_id, caption,
       CASE 
	   		WHEN caption LIKE '%unsplash%' THEN 0
			WHEN caption LIKE '%Unsplash%' THEN 0
			WHEN caption LIKE '%Givey%' THEN 0
			WHEN caption LIKE '%givey%' THEN 0
	
			WHEN caption LIKE '%Author%' THEN 1
			WHEN caption LIKE '%author%' THEN 1
			WHEN caption LIKE '%by me%' THEN 1
	
			WHEN caption like '%https%' Then 0
			WHEN caption like '%http%' Then 0
			WHEN caption like '%from%' Then 0
			WHEN caption like '%[%]%' Then 0
			WHEN caption like '%Image by%' Then 0
            ElSE 100
       END 
	   AS source_img
FROM public.scraper_figcaptions
) as X
where source_img < 5
group by article_id
) as figures

LEFT JOIN scraper_articles articles ON figures.article_id = articles.id
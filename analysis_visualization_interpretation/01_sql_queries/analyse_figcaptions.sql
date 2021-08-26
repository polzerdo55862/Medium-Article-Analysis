Select count(*) from
(
SELECT caption,
       CASE 
	   		WHEN caption LIKE '%unsplash%' THEN 'unsplash.com'
			WHEN caption LIKE '%Unsplash%' THEN 'unsplash.com'
			WHEN caption LIKE '%Givey%' THEN 'givey.com' 
			WHEN caption LIKE '%givey%' THEN 'givey.com' 
	
			WHEN caption LIKE '%Author%' THEN 'Author' 
			WHEN caption LIKE '%author%' THEN 'Author'
			WHEN caption LIKE '%by me%' THEN 'Author'
	
			WHEN caption like '%https%' Then 'Other sources'
			WHEN caption like '%http%' Then 'Other sources'
			WHEN caption like '%from%' Then 'Other sources'
			WHEN caption like '%[%]%' Then 'Other sources'
			WHEN caption like '%Image by%' Then 'Other sources'
            ElSE 'Source unclear'
       END 
	   AS Source
FROM public.scraper_figcaptions
Order by Source ASC
) as X
where Source != 'Source unclear'
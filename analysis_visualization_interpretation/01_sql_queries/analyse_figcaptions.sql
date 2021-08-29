Select count(*) from
(
SELECT caption,
       CASE 
	   		WHEN Upper(caption) LIKE '%UNSPLASH%' THEN 'unsplash.com'
			WHEN Upper(caption) LIKE '%GIVEY%' THEN 'givey.com' 
	
			WHEN Upper(caption) LIKE '%AUTHOR%' THEN 'Author' 
			WHEN Upper(caption) LIKE '% ME%' THEN 'Author'
	
			WHEN caption like '%https%' Then 'Other sources'
			WHEN caption like '%http%' Then 'Other sources'
			WHEN Upper(caption) like '%FROM%' Then 'Other sources'
			WHEN caption like '%[%]%' Then 'Other sources'
			WHEN Upper(caption) like '%IMAGE BY%' Then 'Other sources'
            ElSE 'Source unclear'
       END 
	   AS Source
FROM public.scraper_figcaptions
Order by Source ASC
) as X
where Source != 'Source unclear'
Select count(*) from
(
SELECT id,
	clap_count,
	title,
       CASE 
	   		WHEN Upper(title) LIKE '%HOW TO%' THEN 'How To'
			WHEN Upper(title) LIKE '%HOW-TO%' THEN 'How To'
            WHEN Upper(title) LIKE '%GUIDE%' THEN 'Guide'
			WHEN Upper(title) LIKE '%?%' THEN 'Question'
			WHEN Upper(title) LIKE '%CHEAT SHEET%' THEN 'Cheet Sheet'
			WHEN Upper(title) LIKE '%TUTORIAL%' THEN 'Tutorial'
			WHEN Upper(title) LIKE '%HOW %' THEN 'How'
			WHEN Upper(title) LIKE '%WHY %' THEN 'Why'
			ElSE 'Others'
       END 
	   AS headline_type,
	   CASE 
	   		WHEN title ~ '[0-9]' THEN 'Number as Digit'
			WHEN title ~ '[0-9][0-9]' THEN 'Number as Digit'
			WHEN Upper(title) like '%ONE %' THEN 'Number'
			WHEN Upper(title) like '%TWO  %' THEN 'Number'
			WHEN Upper(title) like '%THREE %' THEN 'Number'
			WHEN Upper(title) like '%FOUR  %' THEN 'Number'
			WHEN Upper(title) like '%FIVE %' THEN 'Number'
			WHEN Upper(title) like '%SIX %' THEN 'Number'
			WHEN Upper(title) like '%SEVEN %' THEN 'Number'
			WHEN Upper(title) like '%EIGHT %' THEN 'Number'
			WHEN Upper(title) like '%NINE %' THEN 'Number'
			WHEN Upper(title) like '%TEN %' THEN 'Number'
			ElSE 'No Number'
       END 
	   AS numbers_used,
	
	   CASE 
	   		WHEN title LIKE '%2021%' THEN 'Year'
			WHEN title LIKE '%2020%' THEN 'Year'
			WHEN title LIKE '%2019%' THEN 'Year'
			WHEN title LIKE '%2018%' THEN 'Year'
			WHEN title LIKE '%2017%' THEN 'Year'
			WHEN title LIKE '%2016%' THEN 'Year'
			WHEN title LIKE '%2015%' THEN 'Year'
			WHEN title LIKE '%2014%' THEN 'Year'
			WHEN title LIKE '%2013%' THEN 'Year'
			ElSE 'No Year found'
       END
	   AS year_used,
	
		LENGTH (title) as lenth_of_title
FROM public.scraper_articles
) as X
-- where numbers_used like 'Number as Digit'
-- where headline_type not like 'Others'
where year_used like 'Year'
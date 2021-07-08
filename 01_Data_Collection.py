'''
This script collects the data from different data sources and end points and saves the raw data in a SQLite database.

In the following I search for articles published in a certain time frame in the TowardsDataScience archive (https://towardsdatascience.com/archive/year/month/day)

References:
https://hackernoon.com/how-to-scrape-a-medium-publication-a-python-tutorial-for-beginners-o8u3t69
'''

import helper_functions
from bs4 import BeautifulSoup
import requests

#########################################################################################################################
# Execute the extraction process iteratively
# The HTML request is looking for all articles published on the defined date. By iterating over a list
# with all dates in a certain time frame, we will get all articles published on TowardsDataScience in this time frame.
#########################################################################################################################

from datetime import date, timedelta

# returns a list with a entry for each day between sdate and edate
days = []

sdate = date(2020, 1, 1)   # start date
edate = date(2020, 1, 3)   # end date

delta = edate - sdate       # as timedelta

for i in range(delta.days + 1):
    day = sdate + timedelta(days=i)
    days.append(day)

# iterating over all entries
for k in range(0, 1, 1):
    year = str(days[k].year)
    month = str(days[k].month).zfill(2)
    day = str(days[k].day).zfill(2)

    date_published = f'{month}/{day}/{year}'
    url = f'https://towardsdatascience.com/archive/{year}/{month}/{day}'
    print("Url: " + url)

    df = helper_functions.extract_data(url, date_published)

    # save df to sql
    # df.to_sql('stories', con=conn, if_exists='append')

#########################################################################################################################
# Save the results in a SQLite database
#########################################################################################################################

# connect to SQLite database medium.db
con = helper_functions.create_sqlite_connection("medium.db")
cur = con.cursor()

# define sql statement to create table "stories" if not exist
sql_create_table_stories = """
                                CREATE TABLE IF NOT EXISTS test (

                                    date_published INTEGER PRIMARY KEY,
                                    title TEXT NOT NULL,
                                    subtitle TEXT,
                                    claps TEXT NOT NULL,
                                    responses INTEGER,
                                    author_url TEXT NOT NULL,
                                    reading_time INTEGER

                            );
                            """

# execute sql statement
cur.execute(sql_create_table_stories)

# print all tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cur.fetchall())

# drop table
# helper_functions.print_tables_in_database(cur)
# helper_functions.drop_table(cur, 'test')
# helper_functions.print_tables_in_database(cur)


from bs4 import BeautifulSoup
import requests

url = "https://towardsdatascience.com/making-python-programs-blazingly-fast-c1cd79bd1b32"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

with open("output1.html", "w") as file:
    file.write(str(soup))

#stories = soup.find_all('div', class_='streamItem streamItem--postPreview js-streamItem')

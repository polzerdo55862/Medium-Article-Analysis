"""
This module contains some rep
"""

import sqlite3
import sys
import pandas as pd
from bs4 import BeautifulSoup
import requests
import data_model

######################################################################################################################
# Functions to interact with the SQLite database
######################################################################################################################

class SQLiteConnection:

    def __init__(self, db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        self.conn = None
        self.cur = None

        try:
            self.conn = sqlite3.connect(db_file)
            self.cur = self.conn.cursor()
        except:
            print("Error:", sys.exc_info()[0])

        # # (if not exist) create table stories
        # try:
        #     self.cur.execute(data_model.sql_create_table_stories)
        # except:
        #     print("Error:", sys.exc_info()[0])



    def drop_table(self, table_to_drop):
        """
        drop a table
            :param table_to_drop: String, Name of the table that should be dropped
        """

        sql_drop_table = f"drop table {table_to_drop}"

        try:
            self.cur.execute(sql_drop_table)
        except:
            print("Error:", sys.exc_info()[0])

    def print_tables(self):
        try:
            self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            print(self.cur.fetchall())
        except:
            print("Error:", sys.exc_info()[0])

    def execute(self, statement):
        try:
            self.cur.execute(statement)
            print(self.cur.fetchall())
        except:
            print("Error:", sys.exc_info()[0])


######################################################################################################################
# Functions to interact with the MySQL database
######################################################################################################################

class SQLiteConnection:





######################################################################################################################
# functions for collection data
######################################################################################################################

class Story:
    """
    class to extract all the information to the stories given in the medium archive
        :parameter year, month, day: date
    """

    def __init__(self, conn, year, month, day):

        date_published = f'{month}/{day}/{year}'

        # webpage for scraping
        url = f'https://towardsdatascience.com/archive/{year}/{month}/{day}'

        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        # find all entries to the stories found
        stories = soup.find_all('div', class_='streamItem streamItem--postPreview js-streamItem')
        stories_data = []

        # extract data for attributes author_url, reading_time, reading_time, responses, story_url
        for story in stories:
            each_story = []

            author_box = story.find('div', class_='postMetaInline u-floatLeft u-sm-maxWidthFullWidth')
            author_url = author_box.find('a')['href']

            try:
                reading_time = author_box.find('span', class_='readingTime')['title']
            except:
                continue

            title = story.find('h3').text if story.find('h3') else '-'
            subtitle = story.find('h4').text if story.find('h4') else '-'

            if story.find('button',
                          class_='button button--chromeless u-baseColor--buttonNormal js-multirecommendCountButton u-disablePointerEvents'):

                claps = story.find('button',
                                   class_='button button--chromeless u-baseColor--buttonNormal js-multirecommendCountButton u-disablePointerEvents').text

            else:
                claps = 0

            if story.find('a', class_='button button--chromeless u-baseColor--buttonNormal'):

                responses = story.find('a', class_='button button--chromeless u-baseColor--buttonNormal').text

            else:
                responses = '0 responses'

            story_url = story.find('a', class_='button button--smaller button--chromeless u-baseColor--buttonNormal')[
                'href']

            # data cleaning
            reading_time = reading_time.split()[0]
            responses = responses.split()[0]

            story_page = requests.get(story_url)
            story_soup = BeautifulSoup(story_page.text, 'html.parser')

            sections = story_soup.find_all('section')
            story_paragraphs = []
            section_titles = []

            for section in sections:
                paragraphs = section.find_all('p')
                for paragraph in paragraphs:
                    story_paragraphs.append(paragraph.text)

                subs = section.find_all('h1')
                for sub in subs:
                    section_titles.append(sub.text)

            number_sections = len(section_titles)
            number_paragraphs = len(story_paragraphs)

            each_story.append(date_published)
            each_story.append(title)
            each_story.append(subtitle)
            each_story.append(claps)
            each_story.append(responses)
            each_story.append(author_url)
            each_story.append(story_url)
            each_story.append(reading_time)
            each_story.append(number_sections)
            each_story.append(section_titles)
            each_story.append(number_paragraphs)
            each_story.append(story_paragraphs)

            stories_data.append(each_story)

        # write data to data frame "df" and return df
        columns = ['date_published', 'title', 'subtitle', 'claps', 'responses',
                   'author_url', 'story_url', 'reading_time',
                   'number_sections', 'section_titles',
                   'number_paragraphs', 'paragraphs']

        self.stories = pd.DataFrame(stories_data, columns=columns)
        self.stories.to_sql("stories", conn, if_exists='append')

class StoryContent:
    '''
        Class to collect and store all required data from a specific story
        :parameter
            url: String, e.g. 'https://towardsdatascience.com/principal-coordinates-analysis-cc9a572ce6c'
    '''

    def __init__(self, url):
        self.page = requests.get(url)
        self.soup = BeautifulSoup(self.page.text, 'html.parser')

        ##########################################################################################################
        # Find all figures and figure captures
        ##########################################################################################################
        self.figure_captures = []

        figures = self.soup.find_all('figcaption')

        for figure in figures:
            capture_modified = str(figure).replace('<figcaption class="kl km fy fw fx kn ko bf b bg bh dx">', '')
            capture_modified = capture_modified.replace('</figcaption>', '')
            self.figure_captures.append(capture_modified)

        ##########################################################################################################
        # test
        ##########################################################################################################
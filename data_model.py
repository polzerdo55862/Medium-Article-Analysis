"""
Compilation of SQL statements to create required data model
"""

# create the table with all basic information to the stories
sql_create_table_stories = """
                                CREATE TABLE IF NOT EXISTS stories (

                                    date_published INTEGER PRIMARY KEY,
                                    title TEXT NOT NULL,
                                    subtitle TEXT,
                                    claps TEXT NOT NULL,
                                    responses INTEGER,
                                    author_url TEXT NOT NULL,
                                    reading_time INTEGER

                            );
                            """
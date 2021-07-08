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
# Medium Scraper

Includes some functions for collecting various data from the online publishing platform Medium (medium.com). The database backups contain data from articles of the "Towards Data Science" publication.

1. Create Virtualenv
```bash
python3 -m venv /path/to/new/virtual/environment
```
2. Install requirements
```bash
pip install -r requirements.txt
```
3. Create database "medium" on your Postgres Server
4. Change Database Settings in medium_scraper/settings.py

5. Migrate to apply Django data model to database "medium"
````bash
python3 manage.py migrate
````
This should create the following table structure:

5. Restore Database backup in your postgres database
```bash
pg_restore -U postgres -C -d medium backup_file.tar
```

For creating a backup use:
```bash
pg_dump -U postgres -W -F t medium > database_backup\backup_file.tar
```


## License
[MIT](https://choosealicense.com/licenses/mit/)
Index

- Overview & Features
- Tech Stack brief
- Dependencies
- Configuration
- manage.py options
- userapi and shopyoapi
- modules


## Overview

Maurilearn is a learning management system. It has the following
features:

### Full course

All quizes must be completed before certificate can be requested

- Sections
- Section Quizes
- Chapters
- Assignments
- Assignment correction
- Certificate request
- Certificate issue

### Light course

All quizes must be completed before certificate can be requested.

### Quizes for the whole course

- Chapters
- Assignments
- Assignment correction
- Certificate request (teacher approval request)
- Certificate issue

### Course creation:

- Markdown
- Documents
- Images
- Videos

### Access & subscription

- Students see only courses for their grades (can be customised)
- Users can subscribe to courses they like

## Tech Stack Brief 

- Language: Python
- Database: MySQL
- Web Framework: Flask

## Dependencies

- reportlab: used to generate pdf
- flask_sqlalchemy: wrapper around SQLAlchemy. SQLAlchemy is an ORM (Object Relational Mapper) which is used to execute database operations using Python and also using the records as objects
- flask_migrate: wrapper around Alembic, a migration package in Python
- flask_uploads: used to manage uploads save videos
- pymysql: Python MySQL connector
- faker: generate fake data
- flask_script: used for manage.py to get commandline options
- flask_login: used to manage login
- markdown: render markdown
- werkzeug==0.16.1: no need to specify it but due to flask-uploads conflict, we specify the version. Else installing Flask auto installs werkzeug
- flask_wtf: html form and validation using Python
- email_validator: used in flask-wtf but not installed by default
pandas: used for yet to implement bulk upload
- xlrd: pandas dependency not installed by default

## Configuration

See README

## manage.py options

```
python manage.py rundebug
```

runs on port 5000 by default

```
python manage.py rundebug <port>
```

optional argument allows to specify other port

```
python manage.py runserver
```

same as app.run()

```
python manage.py startapp <app_name>
```

much like Django, creates a folder in module with empty forms.py and view.py so that you instantly get foldername/ url in your app

**After model change**

```
python manage.py db migrate
python manage.py db migrate
```

Used together to apply migrations

migration is when you do changes to models

**apply settings**

```
python manage.py applysettings
```

Sets school name to that set in config.json. Sets logo to None. Sets contact mail to that in config.json

**initialise**

```
python manage.py initialise
```

consists of 

```
- python manage.py db init
- python manage.py db migrate
- python manage.py db upgrade
- Add admins in config.json
- python manage.py apply settings
```

## Userapi and Shopyoapi

Both folders contain helper functions

## modules 

Modules are located in modules/

- admin/ - used for the admin view
- auth/ - login, logout and access
- base/ - templates that repeat on all pages
- bulk/ - bulk upload
- cdn/ - not an actual CDN but serves files
- course/ - course management including homework evaluation and certificate request
- debug/ - not used
- lightcourse - lightcourse management excluding homework evaluation and certificate request done in courses/
- profile/ - profile info and password change
- quiz/ - view.py not really used. More to include Quiz and Answer models for course
- school/ - school info 
- student/ - student management
- teacher/ - teacher management

Normally modules are as follows:

```
module/
	view.py # module logic
	models.py # models i.e your tables in code/object form
	forms.py # forms
```


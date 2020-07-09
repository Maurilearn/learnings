# download python

[download](https://www.python.org/downloads/)

# cloning

```
git clone https://github.com/Abdur-rahmaanJ/learnings.git
```

for push `git push origin master` as only one branch

for update `git pull origin master`

# install packages

try on the commandline

```
python
```

if command not ok, configure path

then install packages

```
python -m pip install -r requirements.txt
```

# Needed environment variables

```
name: AMILEARN_MAIL_PASS
value: value for smtp mail
```


```
name: AMILEARN_MYSQL_PASS
value: value for mysql password
```

# Creating database

```sql
CREATE DATABASE maurilearn;
```

on the mysql console

# Configure connection

In config.py under `class DevelopmentConfig(Config)` set the username, server_name and db name

```
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{server_name}/{db_name}".format(
            username='root',
            password=check_environ('AMILEARN_MYSQL_PASS'),
            server_name='localhost',
            db_name='maurilearn'
        )
```

# Files

create a file named config.py and copy the content of config_demo.py in it

create a file named config.json and copy the content of config_demo.json in it


# Default password and environment

In config.json configure as appropriate, leave development as such

You can add more admins

```
{
    "environment": "development",
    "admins": [
      {
      "email": "arj.python@gmail.com",
      "password": "pass",
      "name": "Abdur-Rahmaan Janhangeer"
      },
      {
      "email": "jdoe@gmail.com",
      "password": "pass",
      "name": "John Doe"
      }
    ]
}
```


# Initialise 

run 

```
python manage.py initialise
```

to run server

```
python manage.py rundebug
```

by default it runs on port 5000 with url `http://127.0.0.1` and
can be accessed via `http://127.0.0.1:5000`
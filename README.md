# download python

[download](https://www.python.org/downloads/)

# cloning

```
git clone https://github.com/Abdur-rahmaanJ/learnings.git
```

for push `git push origin master` as only one branch

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

In config.json replace with correct values for mysql connection:

```
"connect": {
      "username":"root",
      "name":"localhost",
      "db_name":"amilearn"
    }
```

# admin pass

default admin

change before initialising
```
"admin": {
      "email": "arj.python@gmail.com",
      "password": "pass",
      "name": "Abdur-Rahmaan Janhangeer"
    },
```

# initialise


```
python manage.py initialise
```

Add random students and teachers
```
python manage.py populate
```

# Run server

```
python manage.py rundebug
```


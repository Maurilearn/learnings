

# initialise

```
python manage.py clean
```

```
python manage.py initialise
```

Add random students
```
python manage.py populate
```

# Run server

```
python manage.py rundebug
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
# Specialist Certificate in Data Analytics Essentials Assignment

## Chapter 1: Download Database

A repository for the database can be found at: [github.com/lerocha/chinook-database](https://github.com/lerocha/chinook-database)

For this assignment I'll be using the SQLite Chinook Database

## Imports


```python
import requests
```

The `requests` module allows you to send HTTP requests using Python.

## Retrieving the Database


```python
response = requests.get('https://github.com/lerocha/chinook-database/raw/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite')
```

## Saving the Database Locally


```python
with open('../00_Data/Chinook_Sqlite.sqlite', 'wb') as file:
    file.write(response.content)
```

The "wb" mode opens the file in binary format for writing. The `with` statement is for exception handling.

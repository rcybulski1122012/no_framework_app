# no_framework_app

Simple to-do lists application made with Python without any web framework and ORM.
Created for educational purposes.

## Features
* Creating, editing, and deleting to-do lists
* Creating, deleting and marking tasks as done 
* Creating accounts and logging

## Technologies
* Python 3.8
* Bootstrap 4

## Setup
1. Clone the repository
```sh
$ git clone https://github.com/rcybulski1122012/no_framework_app.git
```

2. Create virtual environment, activate it and install dependencies
```sh
$ cd no_framework_app
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

3. Provide environment variables for PostgreSQL connection (DB_HOST, DB_NAME, DB_USER and DB_PASSWORD).

4. Create tables and install required PostgreSQL extensions.
```sh
$ python -m app.scripts.install_extensions
$ python -m app.scripts.create_tables
```

5. That's all. Now you can run the application
```sh
$ python -m app.run
```
The application is available on localhost:8000.

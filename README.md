# Zonar Book API

**Author**: Megan Flood

**Version**: 0.0.0

## Overview
REST API for keeping track of a user's book wish list for Zonar interview

## Architecture
Written in [Python](https://www.python.org/), with [pytest](https://docs.pytest.org/en/latest/). Uses the web framework [Pyramid](https://trypyramid.com/) with a scaffold built with the Cookiecutter [pyramid-cookiecutter-alchemy](https://github.com/Pylons/pyramid-cookiecutter-alchemy). Database run through [SQLite](https://sqlite.org/index.html) using [SQLAlchemy](http://www.sqlalchemy.org/).

## Routes
| Route | Name | Description |
|:--|--|:--|
| `/signup` | signup | POST: create a new user |
| `/books` | book-list | GET: list all the books on the wish list<br/>POST: add a new book to the wish list |
| `/books/{id:\d+}` | book-id | PUT: update a book's details by id<br/>DELETE: remove a book from the wish list by id |

## Getting Started

Clone this repository to your local machine.
```
$ git clone https://github.com/musflood/zonar-book-api.git
```

Once downloaded, change directory into the `book_api` directory.
```
$ cd book_api
```

Begin a new virtual environment with Python 3 and activate it.
```
book_api $ python3 -m venv ENV
book_api $ source ENV/bin/activate
```

Install the application with [`pip`](https://pip.pypa.io/en/stable/installing/).
```
(ENV) book_api $ pip install -e .[testing]
```

Then initialize the database with the `initializedb` command, providing the right `.ini` file for the app's configuration.
```
(ENV) book_api $ initializedb development.ini
```

Once the package is installed and the database is created, start the server with `pserve` and the right `.ini` file.
```
(ENV) book_api $ pserve development.ini --reload
```

Application is served on http://localhost:6543

## Testing
Make sure you have the `testing` set of dependancies installed.

You can test this application by running `pytest` in the same directory as the `setup.py` file.
```
(ENV) book_api $ pytest
```

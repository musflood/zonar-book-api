# Zonar Book API

**Author**: Megan Flood

**Version**: 1.0.0

## Overview
REST API for keeping track of a user's book wish list for Zonar interview

## Architecture
Written in [Python](https://www.python.org/), with [pytest](https://docs.pytest.org/en/latest/). Uses the web framework [Pyramid](https://trypyramid.com/) with a scaffold built with the Cookiecutter [pyramid-cookiecutter-alchemy](https://github.com/Pylons/pyramid-cookiecutter-alchemy). Database run through [SQLite](https://sqlite.org/index.html) using [SQLAlchemy](http://www.sqlalchemy.org/).

More on design and technology choices [here](./design.md).

## Routes

<table>
    <tr>
        <th>Route</th>
        <th>Name</th>
        <th>Method</th>
        <th>Description</th>
        <th>Data Format</th>
    </tr>
    <tr>
        <td><code>/signup</code></td>
        <td>signup</td>
        <td>POST</td>
        <td>create a new user</td>
        <td><pre>
<code>{
    first_name: (String),
    last_name: (String),
    email: (String),
    password: (String)
}</code></pre></td>
    </tr>
    <tr>
        <td rowspan="2"><code>/books</code></td>
        <td rowspan="2">book-list</td>
        <td>GET</td>
        <td>list all the books on the wish list</td>
        <td><pre>
<code>{
    email: (Registered email),
    password: (Registered password)
}</code></pre></td>
    </tr>
    <tr>
        <td>POST</td>
        <td>add a new book to the wish list</td>
        <td><pre>
<code>{
    email: (Registered email),
    password: (Registered password)
    title: (String),
    author: (String),
    isbn: (String),
    pub_date: (String in the form mm/dd/yyyy)
}</code></pre></td>
    </tr>
    <tr>
        <td rowspan="3"><code>/books/{id:\d+}</code></td>
        <td rowspan="3">book-id</td>
        <td>GET</td>
        <td>get details about a book from the wish list by id</td>
        <td><pre>
<code>{
    email: (Registered email),
    password: (Registered password)
}</code></pre></td>
    </tr>
    <tr>
        <td>PUT</td>
        <td>update a book's details by id</td>
        <td><pre>
<code>{
    email: (Registered email),
    password: (Registered password)
    title: (String),
    author: (String),
    isbn: (String),
    pub_date: (String in the form mm/dd/yyyy)
}</code></pre></td>
    </tr>
    <tr>
        <td>DELETE</td>
        <td>remove a book from the wish list by id</td>
        <td><pre>
<code>{
    email: (Registered email),
    password: (Registered password)
}</code></pre></td>
    </tr>

</table>

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

# blog-platform
A small and simple blog platform/CMS. The back end is Python/Flask, and the front is done in both Jinja2 and React (React for the more interactive editor view, and Jinja for the blog itself). Using React for the editor makes allows for a more dynamic experience, while using Jinja for the blog itself ensures better search engine optimization and client performance.

The editor fullfills all CRUD-operations, backed by a RESTful API (GET, POST, PUT and DELETE are all supported for their respective functions)

![The editor](https://i.imgur.com/VduF06e.png)

![The blog](https://i.imgur.com/B6KBD3D.png)

### Python libraries used:
* **SQLAlchemy** (for the object-relational mapping)
* **Flask-Login** (for user authentication)
* **Flask-BCrypt** (for hashing passwords)
* **Flask-Misaka** (for Markdown support)

### To note if you decide to clone this:
* By default it uses MySQL as the database (at this point in time, the app's needs are met well by MySQL)
* The app is tested on Ubuntu LTS 16.04, using Apache2 with [mod_wsgi](https://modwsgi.readthedocs.io/en/develop/). A good guide to using this can be found [here](http://terokarvinen.com/2016/deploy-flask-python3-on-apache2-ubuntu).
* As it is, the app requires a config file (config.py, located in the root directory) that is not included in the repository for obious security reasons. The format is this:
```python
# The top secret login details to the database.
db_config = {
    'user': '[redacted]',
    'pw': '[redacted]',
    'db': '[redacted]',
    'host': 'localhost',
    'port': '3306'
}

# Used for securing sessions
secret_key = "[redacted]"
```

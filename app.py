
# First, we import the packages we need for the project.
from flask import Flask, request, render_template, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from config import db_config
import json, datetime
# This line calls the constructor for the Flask app, issuing the name of the file (app.py) as a parameter
app = Flask(__name__)
# And we set the DEBUG to be 'true' - this allows making changes to the app visible without rebooting the whole server
app.config['DEBUG'] = True
# We'll use BCrypt to crypt the passwords
bcrypt = Bcrypt(app)
# db_config is a struct stored in another file (config.py), 
# so it can easily be aded to .gitignore in order to avoid exposing database connection details
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % db_config
db = SQLAlchemy(app)
# We define a Post class to be used by SQLAlchemy when accessing the database
class Post(db.Model):
    # As per usual, the primary key is an auto incrementing integer called 'id'
    # The other attributes should be pretty self explanatory as well
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=False, nullable=False)
    text = db.Column(db.Text, unique=False, nullable=True)
    # purpose: to save the time a post was first created
    created = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.datetime.now)
    # purpose: to save the time a post was last updated
    last_updated = db.Column(db.DateTime, unique=False, nullable=False)

    # This is needed in order to jsonify the object properly
    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'created': self.created,
            'last_updated': self.last_updated 
        }

    # This serializes the object in a slimmer fashion
    @property
    def slim_serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'last_updated': self.last_updated
        }


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), unique=False, nullable=False)
    role = db.Column(db.String(64), unique=False, nullable=False)

# Just a placeholder, for easy checking if the server is functional
@app.route('/')
def index():
    return 'Hello!'

# TODO replace with a proper saving function
@app.route('/api/save/')
def save_post():
    post_title = request.args.get('title', '')
    post_text = request.args.get('text', '')
    post = Post(title = post_title, text = post_text, last_updated = datetime.datetime.now())
    db.session.add(post)
    db.session.commit()
    return jsonify(post.serialize)

# For getting a specific post
@app.route('/api/posts/<int:post_id>')
def load_post(post_id):
    post = Post.query.filter_by(id = post_id).first()
    return jsonify(post.serialize)

# For getting all posts. This will return all post content
@app.route('/api/posts/')
def load_posts():
    posts = []
    posts_from_db = Post.query.all()
    for post in posts_from_db:
        posts.append(post.serialize)
    return jsonify(posts)

# For getting all posts in a form a bit better suited for lists (not the whole post content)
@app.route('/api/posts/list')
def load_posts_list():
    posts = []
    posts_from_db = Post.query.all()
    for post in posts_from_db:
        posts.append(post.slim_serialize)
    return jsonify(posts)

@app.route('/api/posts/delete/<int:post_id>')
def delete_post(post_id):
    Post.query.filter_by(id = post_id).delete()
    db.session.commit()
    return str(post_id)

@app.route('/admin/login', methods = ['GET'])
def login_screen():
    return render_template('login.html')

@app.route('/admin/login', methods = ['POST'])
def login():
    user = User(username = request.form['username'], password = request.form['password'])
    user_from_db = User.query.filter_by(username = request.form['username']).first()
    if bcrypt.check_password_hash(user_from_db.password, user.password):
        session['logged_in'] = True
        session['user_id'] = user_from_db.id
        return 'Success!'
    else:
        return render_template('login.html', message = "Username and/or Password wrong!")

@app.route('/signup', methods = ['GET'])
def signup_screen():
    return render_template('signup.html')

@app.route('/signup', methods = ['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    password_again = request.form['password_again']
    if password is not password_again:
        return 'Passwords do not match!'
    user = User(username = username, password = bcrypt.generate_password_hash(password), role = 'USER')
    db.session.add(user)
    db.session.commit()
    return render_template('login.html', message = 'Signup succesful!')

@app.route('/admin', methods = ['GET'])
    return 'ADMIN PAGE IS HERE'

# d = request.args.get('id', '') 
# This is only used when using the dev server.
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)


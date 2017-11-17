# First, we import the packages we need for the project.
from flask import Flask, request, render_template, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import db_config
import json, datetime
# This line calls the constructor for the Flask app, issuing the name of the file (app.py) as a parameter
app = Flask(__name__)
# And we set the DEBUG to be 'true' - this allows making changes to the app visible without rebooting the whole server
app.config['DEBUG'] = True
# db = SQLAlchemy(app)

# db_config is a struct stored in another file (config.py), 
# so it can easily be aded to .gitignore in order to avoid exposing database connection details
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % db_config

db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=False, nullable=True)
    text = db.Column(db.Text, unique=False, nullable=True)
    created = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.datetime.now)
    last_updated = db.Column(db.DateTime, unique=False, nullable=False)
    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'created': self.created,
            'last_updated': self.last_updated 
        }

@app.route('/')
def index():
    return 'Jimi on mestari'

@app.route('/api/save/')
def save_post():
    post_title = request.args.get('title', '')
    post_text = request.args.get('text', '')
    post = Post(title = post_title, text = post_text, last_updated = datetime.datetime.now())
    db.session.add(post)
    db.session.commit()
    return jsonify(post.serialize)

@app.route('/api/posts/<int:post_id>')
def load_post(post_id):
    id = request.args.get('id', '') 
    post = Post.query.filter_by(id = post_id).first()
    return jsonify(post.serialize)

@app.route('/api/posts/')
def load_posts():
    posts = []
    posts_from_db = Post.query.all()
    for post in posts_from_db:
        posts.append(post.serialize)
    return jsonify(posts)

# This is only used when using the dev server.
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)


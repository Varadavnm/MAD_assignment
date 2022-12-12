# MAD_assignment
import os.path
import sqlalchemy
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, update

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///articles.sqlite3'
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

class User(db.Model):
    __table__name = "user"
    user_id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True)
    first_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String)
    user_name = db.Column(db.String, unique = True, nullable = False)
    email = db.Column(db.String, unique = True, nullable = False)
    pass_word = db.Column(db.String, unique = True, nullable = False)

class Author(db.Model):
    __table__name = "author"
    author_id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True)
    author_name = db.Column(db.String, unique = True, nullable = False)
    author_user_name = db.Column(db.String, ForeignKey("user.user_name"), unique = True, nullable = False)
    followers = db.Column(db.Integer)

class Post(db.Model):
    __tablename__ = "post"
    post_id = db.Column(db.Integer, primary_key = True, nullable = False, autoincrement = True)
    author_name = db.Column(db.String, nullable = False)
    title = db.Column(db.String, nullable = False, unique=True)
    content = db.Column(db.String)
    # time = db.Column(db.DateTime(timezone=True), nullable=False)
    views = db.String(db.Integer)



@app.route('/user/login', methods = ['GET'])
def get_user_login():
    return render_template("user-login.html")

@app.route('/user/login', methods = ['POST'])
def post_user_login():
    forms = request.form
    user_id = forms.get("username")
    password = forms.get("password")
    
@app.route('/', methods = ['GET'])
def get_posts():
    posts = Post.query.all()
    return render_template("all_posts.html", posts=posts)

@app.route('/article/post', methods = ['GET'])
def get_create_post():
    return render_template("create_post.html")

@app.route('/article/post', methods = ['POST'])
def create_post():
    posts = request.form
    author_name = posts.get("author_name")
    # author_user_id = posts.get("author_user_id")
    title = posts.get("title")
    content = posts.get("content")
    post = Post(author_name = author_name, title = title, content = content)
    db.session.add(post)
    db.session.commit()
    print(title)
    return redirect('/')

@app.route('/user/register', methods = ['GET'])
def get_user_registration():
    return render_template("user_registration.html")

@app.route('/user/register', methods = ['POST'])
def post_user_registration():
    form = request.form
    first_name = form.get("first_name")
    last_name = form.get("last_name")
    email = form.get("email_id")
    user_name = form.get("user_name")
    password1 = form.get("password")
    password2 = form.get("retype_password")
    user = User(first_name=first_name, last_name=last_name, user_name = user_name, email=email, pass_word=password1)
    db.session.add(user)
    db.session.commit()
    return redirect('/')
       

if __name__=="__main__":
    app.run(debug=True)





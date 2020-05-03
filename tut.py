from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json
from datetime import datetime

with open('config.json', 'r') as c:
    params = json.load(c)["params"]
with open('config.json', 'r') as d:
    info = json.load(d)["info"]
local_server = "True"

app = Flask(__name__)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['user'],
    MAIL_PASSWORD = params['pass']
)
mail = Mail(app)
if (local_server):
     app.debug = True
     app.config['SQLALCHEMY_DATABASE_URI'] = params['local_url']
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_url']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Contacts(db.Model):
    __tablename__ = 'contacts'
    sno = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    Phone = db.Column(db.String(13), nullable=False)
    Message = db.Column(db.String(12), nullable=False)
    Date = db.Column(db.String(120), nullable=True)

    def __init__(self, Name, Email, Phone, Message, Date):
        self.Name = Name
        self.Email = Email
        self.Phone = Phone  
        self.Message = Message 
        self.Date = Date


class Form(db.Model):
    __tablename__ = 'form'
    sno = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)

    def __init__(self, first_name, last_name, year, month, day):
        self.first_namefirst_name =first_name
        self.last_name = last_name
        self.year =year  
        self.month = month 
        self.day = day

class Posts(db.Model):
    __tablename__ = 'posts'
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(25), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    img_file = db.Column(db.String(120), nullable=False)

    def __init__(self, title, slug, content, date, img_file):
        self.title = title
        self.slugslug =slug
        self.content =content  
        self.date =date 
        self.img_file =img_file
    




@app.route('/')
def home():
    
    posts = Posts.query.filter_by().all()[0:2]
    return render_template('index.html' ,params = params ,info = info , posts=posts)

@app.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=params, post=post, info=info)


@app.route('/about')
def about():
    return render_template("about.html" ,params = params ,info = info)
@app.route('/login')
def login():
    return render_template("login.html" ,params = params ,info = info)

@app.route('/contact' ,methods = ['GET' , 'POST'])
def contact():
    if (request.method== 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(Name = name , Email = email , Phone = phone , Message = message , Date = datetime.now())
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from Blog' , sender= name  , body = message , recipients = [params['user']]  )
    return render_template("contact.html" ,params = params, info = info)



@app.route('/form' ,methods = ['GET' , 'POST'])
def form():
    if (request.method== 'POST'):
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        year = request.form.get('year')
        month = request.form.get('mth')
        day = request.form.get('day')
        entry = Form(first_name = fname , last_name = lname , year = year , month = month , day = day)
        db.session.add(entry)
        db.session.commit()
    return render_template("navbar.html" ,params = params , info = info )
if __name__ == '__main__':

    app.debug = True
    app.run()
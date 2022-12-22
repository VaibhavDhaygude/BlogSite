from flask import Flask,render_template,request,session,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json



app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1:3307/blogs'
db = SQLAlchemy(app)
app.secret_key = 'super-secret-key'

f = open('config.json')
data=json.load(f)["params"]

class Contacts(db.Model):
    # id ,name , email,phoneno,msg ,date
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(40), unique=False, nullable=False)
    phoneno = db.Column(db.String(12), unique=False, nullable=False)
    msg = db.Column(db.String(120), unique=False, nullable=False)
    date = db.Column(db.String(12), unique=False, nullable=False)


class Posts(db.Model):
    # id, title, slug, content, date.
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    slug = db.Column(db.String(25), unique=False, nullable=False)
    content = db.Column(db.String(120), unique=False, nullable=False)
    by = db.Column(db.String(30), unique=False, nullable=False)
    date = db.Column(db.String(12), unique=False, nullable=False)


@app.route("/")
def hello():
    posts=Posts.query.filter_by().all()
    return render_template("index.html",posts=posts)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/post/<string:post_slug>",methods=['GET'])
def post_route(post_slug):
    post=Posts.query.filter_by(slug=post_slug).first()
    return render_template("post.html",post=post)

@app.route("/contact",methods=['GET','POST'])
def contact():
    if(request.method=='POST'):
        # add enrty to database
        name=request.form.get('name')
        email=request.form.get('email')
        phoneno=request.form.get('phoneno')
        msg=request.form.get('msg')
        entry=Contacts(name=name,email=email,phoneno=phoneno,msg=msg,date=datetime.now())
        db.session.add(entry)
        db.session.commit()


    return render_template("contact.html")

@app.route("/dashboard",methods=['GET','POST'])
def dashboard():

    if "user" in session and session['user']==data['admin_username']:
        posts = Posts.query.all()
        return render_template("Admin_dashboard.html", posts=posts)

    if(request.method=="POST"):
        username=request.form.get('username')
        password=request.form.get('password')
        if(username==data["admin_username"] and password==data['admin_password']):
            session['user']=username
            posts=Posts.query.all()
            return render_template("Admin_dashboard.html",posts=posts)
    return render_template("login.html")




@app.route("/edit/<string:id>",methods=['GET','POST'])
def edit(id):
    
    if "user" in session and session['user']==data['admin_username']:
        if(request.method=='POST'):
            title=request.form.get('title')
            writer=request.form.get('writer')
            slug=request.form.get('slug')
            content=request.form.get('content')
            date=datetime.now()
            if id=='0':
                post=Posts(title=title,by=writer,slug=slug,content=content,date=date)
                db.session.add(post)
                db.session.commit()
                
            else:
                post=Posts.query.filter_by(id=id).first()
                post.title=title
                post.by=writer
                post.slug=slug
                post.content=content
                post.date=post.date
                db.session.commit()
                
        # if request.method=="POST":
    post=Posts.query.filter_by(id=id).first()
    return render_template("edit.html",id=id,post=post)


@app.route("/logout")
def logout():
    session.pop('user')
    return redirect("/dashboard")

@app.route("/delete/<string:id>",methods=['GET','POST'])
def delete(id):
    if 'user' in session and session['user']==data['admin_username']:
        post=Posts.query.filter_by(id=id).first()
        db.session.delete(post)
        db.session.commit()
    return redirect("/dashboard")

app.run(debug=True)
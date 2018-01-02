from flask import Flask, render_template, request, flash, redirect
from createform import CreateForm, NewPost
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc



app = Flask(__name__)
app.config['DEBUG'] = True ##enable debug option
app.secret_key = 'Luanchcode tampabay 2017'   ###CSRF key

#create connection to the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://myblog:launchcode2017@localhost:3306/myblog'

app.config['SQLALCHEMY_ECHO'] = True

#Create alchemy object
db = SQLAlchemy(app)


#create persistent class to be use in database
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(120))
    message = db.Column(db.String(200))
    create_date = db.Column(db.DateTime, default=db.func.now())

    def __init__(self,subject,message):
        self.subject = subject
        self.message = message



"""Rendering home page"""
@app.route('/')
def home():
    return render_template('home.html')


"""Rendering blog page"""
@app.route('/blog', methods=['POST', 'GET'])
def blog():
    posts = Post.query.all() 
    id=request.args.get('id')
    order=request.args.get('order')
    if(id):
        entry = Post.query.filter_by(id=id).first()
        return render_template('entry.html', entry=entry) 

    if(order == "new"):
        posts = Post.query.order_by("id desc")

    return render_template('blog.html',posts=posts)



"""Instantiate signup form and rendering welcome page if successfully validated, else rendering signup page"""
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = CreateForm()
    if(request.method == 'POST' and form.validate_on_submit()):
        status = "signup"
        return render_template('welcome.html',name=form.username.data,status=status) 
	
    return render_template('signup.html',form=form) 


"""Instantiate login form and rendering welcome page if successful, else rendering login page"""
@app.route('/login', methods=['POST', 'GET'])
def login():
    form = CreateForm()
    error = ""
    if(request.method == 'POST'):
        if(request.form['username'] != "admin" or request.form['password1'] != "newsys"):
            error="Invalid credential, Please sign up for an account"
        else:
            status = "login"
            return render_template('welcome.html',name=form.username.data,status=status) 

    return render_template('login.html', form=form, error=error)


"""rendering about page"""
@app.route('/about')
def about():
    return render_template('about.html')


"""rendering new post """
@app.route('/post', methods=['POST','GET'])
def post():
    form = NewPost()
    if(request.method == 'POST' and form.validate_on_submit()):
        subject=request.form['subject']
        message=request.form['message']
        post=Post(subject,message)
        db.session.add(post)
        db.session.commit()
        entry = Post.query.filter_by(id=post.id).first()
        return render_template('entry.html', entry=entry) 
        
    return render_template('post.html', form=form)


if __name__ == "__main__":
    app.run(host='127.0.0.1',port=8000)

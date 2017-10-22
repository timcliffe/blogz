from flask import Flask, request, redirect, request, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from cgi import escape

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://blogz:Angels1234@localhost:3306/blogz"
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'jl4wbgu8ptho'
db = SQLAlchemy(app)


class Blogger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='blogger')

    def __init__(self, username, password):
        self.username = username
        self.password = password



class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    blogger_id = db.Column(db.Integer, db.ForeignKey('blogger.id'))


    def __init__(self, title, body, blogger):
        self.blogger = blogger
        self.title = title
        self.body = body

@app.route('/blog')
def blog():
    if request.args.get("id"):
        blog_id = request.args.get("id")
        blogs = Blog.query.get(blog_id)
        return render_template('blogpost.html', blog=blog)
    else:
        blogs = Blog.query.all()
        return render_template('blog.html', blogs=blogs)





@app.before_request
def validate_login():
    allowed_routes = ['login', 'signup', 'blog', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/')
def index():
    return redirect('/login')



@app.route('/signup', methods=['POST', 'GET'])
def signup():
    
    username = ""
    password = ""
    verify = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        # if username == "" or " " or len(username) < 3 or len(username) > 20:
        #     flash("Invalid Username", 'error')
        # if password == "" or " " or len(password) < 3 or len(password) > 20:
        #     flash("Invalid Password", 'error')
        # if verify == "" or verify != password:
        #     flash("Failed Verification", 'error')

        existing_blogger = Blogger.query.filter_by(username=username).first()
        if True:
            new_blogger = Blogger(username, password)
            db.session.add(new_blogger)
            db.session.commit()
            session['username'] = username
            return redirect('/')
        else:
            flash('User already exists')

    return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']
        blogger = Blogger.query.filter_by(username=username).first()
        if blogger and blogger.password == password:
            session['username'] = username
            flash("Logged In")
            return redirect('/newentry')
        elif blogger and blogger.password != password:
            flash('User password incorrect or user does not exist')
            return redirect('/login')
        elif blogger and blogger.username != username:
            flash('Username incorrect or does not exist')
            return redirect('/login')

    return render_template('login.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')


            





@app.route('/newentry', methods=['GET', 'POST'])
def add_blog():
    if request.method == 'GET':
        return render_template('newentry.html', title="Add A New Entry")

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        title_error= ""
        body_error = ""

    if len(blog_title) < 1:
            title_error = "Invalid Title"

    if not title_error and not body_error:
        username = session['username']
        blogger = Blogger.query.filter_by(username=username).first()
        new_blog = Blog(blog_title, blog_body, blogger)
        db.session.add(new_blog)
        db.session.commit()
        query_param_url = "/blog?id=" + str(new_blog.id)
        return redirect(query_param_url)

    else:
        return render_template('newentry.html', title="Add New Entry", title_error=title_error, body_error=body_error)



@app.route('/blog/newentry', methods=['POST', 'GET'])
def new_entry():
    if request.args:
        blog_id = request.args.get("id")
        blog = Blog.query.get(blog_id)


    
    
if __name__== '__main__':
    app.run()

from flask import Flask, request, redirect, request, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://blogz:Angels1234@localhost:34000/blogz"
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.string(120), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, email, password):
        self.email = bloggers
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
    user = request.args.get("blogger")
    id = request.args.get("id")
    blogs = Blog.query.get(id)
    return render_template('blog.html', blogs=blogs)


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def register():
    return render_template('signup.html')


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
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            query_param_url = "/blog?id=" + str(new_blog.id)
            return redirect(query_param_url)

        else:
            return render_template('newentry.html', title="Add Blog Entry", title_error=title_error, body_error=body_error)



@app.route('/blog', methods=['GET'])
def index():
    if request.args:
        blog_id = request.args.get("id")
        blog = Blog.query.get(blog_id)

        return render_template('blogpost.html', blog=blog)


@app.route('/blog', methods=['POST', 'GET'])
def index():
    bloggers = user.query.all()
    return render_template('index.html', bloggers=bloggers)



    
    
if __name__== '__main__':
    app.run()

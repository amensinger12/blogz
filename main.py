from flask import Flask, request, redirect, session, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz@localhost:3306/blogz'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'ayMv&&sdKius%wds!adfTvsWe'
db = SQLAlchemy(app)

class blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(300))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner
        
class user(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db .Column(db.String(120))
    blog = db.relationship('blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

#@app.before_request
#def require_login():
#    allowed_routes = ['login', 'signup', 'blog', 'index']
#    if request.endpoint not in allowed_routes and 'username' not in session:
#        return redirect('/signup')

@app.route("/login", methods=["POST","GET"])
def login():
    username_error = "This username is incorrect"
    password_error = "This password is incorrect"

    if request.form == "POST":
        username = request.form['username']
        password = request.form ['password']
        User = user.query.filter_by(username=username).first()
        password = user.query.filter_by(password=password).first()

        if User and password:
            session['username'] = username
            return redirect('/newpost')
        else:
            return render_template('login.html', password_error=password_error, username_error=username_error)
    else:
        return render_template('login.html')

@app.route('/')
def index():
    users = user.query.all()
    return render_template("index.html", users=users)

@app.route('/blog', methods=['POST','GET'])
def blogs():
    single_post = request.args.get('id')
    blogs = blog.query.all()
    return render_template("all_blogs.html", blogs=blogs, single_post=single_post)

@app.route('/single_post', methods=['POST','GET'])
def single_post():
    id = request.args.get('id')
    single_post = blog.query.filter_by(id=id).first()
    user_id = request.args.get('userid')
    User = user.query.filter_by(id=user_id).first()
    return render_template("single_post.html", single_post=single_post, user_id=user_id, User=User)

@app.route('/newpost', methods=['POST','GET'])
def new_post():
    if request.method == 'POST':
        title = request.form["title"]
        body = request.form["body"]
        owner = user.query.filter_by(username=session['username']).first()

        empty_field_error = "This field must be filled out!"
        if title == "" and body == "":
            title_error = empty_field_error
            body_error = empty_field_error
            return render_template("newpost.html", body=body, title=title, title_error=title_error, body_error=body_error)
        elif title == "":
            title_error = empty_field_error
            return render_template("newpost.html", title=title, title_error=title_error, body=body)
        elif body == "":
            body_error = empty_field_error
            return render_template("newpost.html", body=body, title=title, body_error=body_error)
        else:
            new_post = blog(title, body, owner)
            db.session.add(new_post)
            db.session.commit()
            
            return redirect ("/single_post?id="+str(new_post.id))
    else:
        return render_template("newpost.html")

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

def char_length(x):
    if len(x) > 3 and len(x) < 20:
        return True
    else:
        return False

def empty(x):
    if x:
        return True
    else:
        return False

def email_symbol(x):
    if x.count('@') == 1:
        return True
    else:
        return False

def email_period(x):
    if x.count('.') == 1:
        return True
    else:
        return False

@app.route("/signup", methods=["POST","GET"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_valid = request.form["password_valid"]

        username_error = ''
        password_error = ''
        password_valid_error = ''

        require_field_error = "Required Field"
        char_count_error = " must be between 3 and 20 characters long"
        spaces_error =  " cannot contain any spaces"

        if not empty(username):
            username_error = require_field_error
            password = ''
            password_valid = ''
        elif not char_length(username):
            username_error = "Username" + char_count_error
            password = ''
            password_valid = ''
        else:
            if " " in username:
                username_error = "Username" + spaces_error
                password = ''
                password_valid = ''

        if not empty(password):
            password_error = require_field_error
            password = ''
            password_valid = ''
        elif not char_length(password):
            password_error = "Password" + char_count_error
            password = ''
            password_valid = ''
        else:
            if " " in password:
                password_error = "Password" + spaces_error
                password = ''
                password_valid = ''

        if password_valid == "":
            password_valid_error = require_field_error
            password = ''
            password_valid = ''
        else:
            if password != password_valid:
                password_valid_error = "Passwords must match"
                password_error = "Passwords must match"
                password = ''
                password_valid = ''

        if not username_error and not password_error and not password_valid_error:
            new_user = user(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            return render_template("signup.html", username_error=username_error, username=username, password_error=password_error, password=password, password_valid_error=password_valid_error, password_valid=password_valid)
    else:
        return render_template("signup.html")


if __name__ == '__main__':
    app.run()
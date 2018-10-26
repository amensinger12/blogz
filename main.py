from flask import Flask, request, redirect, session, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(300))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/blog', methods=['POST','GET'])
def blogs():
    single_post = request.args.get('id')
    blogs = blog.query.all()
    return render_template("homepage.html", blogs=blogs, single_post=single_post)

@app.route('/single_post', methods=['POST','GET'])
def single_post():
    id = request.args.get('id')
    single_post = blog.query.filter_by(id=id).first()
    return render_template("single_post.html", single_post=single_post)

@app.route('/newpost', methods=['POST','GET'])
def new_post():
    if request.method == 'POST':
        title = request.form["title"]
        body = request.form["body"]
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
            new_post = blog(title, body)
            db.session.add(new_post)
            db.session.commit()
            
            return redirect ("/single_post?id="+str(new_post.id))
    else:
        return render_template("newpost.html")


if __name__ == '__main__':
    app.run()
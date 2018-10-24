from flask import Flask, request, redirect, render_template
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
def blog():
    single_post = request.args.get('id')
    blog = Blog.query.all()
    return render_template("homepage.html", blog=blog, single_post=single_post)

@app.route('/new_post', methods=['POST','GET'])
def new_post():

    blog_title = request.form["title"]
    body = request.form["body"]
    empty_field_error = "This field must be filled out!"
    if blog_title == "" and body == "":
        title_error = empty_field_error
        body_error = empty_field_error
        return render_template("newpost.html", title_error=title_error, body_error=body_error)
    elif blog_title == "":
        title_error = empty_field_error
        return render_template("newpost.html", title_error=title_error, body=body)
    elif body == "":
        body_error = empty_field_error
        return render_template("newpost.html", title=blog_title, body_error=body_error)

    else:
        new_post = Blog(blog_title, body)
        db.session.add(new_post)
        db.session.commit()
        url = '/blog?id='+str(new_post.id)
        return redirect (url)    


if __name__ == '__main__':
    app.run()
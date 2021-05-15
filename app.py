from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from decouple import config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config("DATABASE_URL")
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default="N/A")
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    #def __repr__(self):
     #   return "blogpost" + str(self.id)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/posts", methods=["POST", "GET"])
def posts():
    if request.method == "POST":
        form_title = request.form["title"]
        form_content = request.form["content"]
        form_author = request.form["author"]
        new_post = BlogPost(title=form_title, content=form_content, author=form_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect("/posts")
    else:
      all_post = BlogPost.query.order_by(BlogPost.date_posted).all()
      return render_template("posts.html", posts=all_post)

@app.route("/posts/delete/<int:id>")
def delete(id):
    delete_post = db.session.delete(BlogPost.query.get_or_404(id))
    db.session.commit()
    return redirect("/posts")

@app.route("/posts/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    edit_post = BlogPost.query.get_or_404(id)
    if request.method == "POST":
       edit_post.title = request.form["title"]
       edit_post.author = request.form["author"]
       edit_post.content = request.form["content"]
       db.session.commit()
       return redirect("/posts")
    
    else:
        return render_template("edit.html", post=edit_post)

if __name__ == "__main__":
    app.run(debug=True)
from flask import render_template, flash, redirect, url_for
from . import public_bp
from .webforms import PostForm
from app.models import Posts
from ..extensions import db



@public_bp.route("/")
def index():
    publicaciones=Posts.query.order_by(Posts.date_posted)
    return render_template("public/index.html", posts=publicaciones)

@public_bp.route("/addPost", methods=['GET', 'POST'])
def addPost():
    form = PostForm()
    if form.validate_on_submit():
        post = Posts(title=form.title.data, content=form.content.data,slug=form.slug.data)
        form.title.data = ''
        form.content.data = ''
        form.slug.data = ''
        db.session.add(post)
        db.session.commit()
        flash("Blog Post Submitted Successfully!")
        response = redirect(url_for('public.index')) 
        return response
    return render_template("public/addPost.html", form=form)

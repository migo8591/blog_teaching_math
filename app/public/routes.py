from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from . import public_bp
from .webforms import PostForm, SearchForm
from app.models import Posts
from ..extensions import db



@public_bp.route("/")
def index():
    publicaciones=Posts.query.order_by(Posts.date_posted)
    return render_template("public/index.html", posts=publicaciones)

@public_bp.route("/addPost", methods=['GET', 'POST'])
@login_required
def addPost():
    form = PostForm()
    if form.validate_on_submit():
        poster=current_user.id
        post = Posts(title=form.title.data, content=form.content.data,slug=form.slug.data, poster_id=poster)
        form.title.data = ''
        form.content.data = ''
        form.slug.data = ''
        db.session.add(post)
        db.session.commit()
        flash("Blog Post Submitted Successfully!")
        response = redirect(url_for('public.post', id=post.id)) 
        return response
    return render_template("public/addPost.html", form=form)
@public_bp.route("/post<int:id>")
def post(id):
    post=Posts.query.get_or_404(id)
    return render_template('public/post.html', post=post)
@public_bp.route("/editPost<int:id>", methods=['GET','POST'])
def editPost(id):
    form=PostForm()
    post=Posts.query.get_or_404(id)
    if form.validate_on_submit():
        post.title=form.title.data
        post.slug=form.slug.data
        post.content=form.content.data
        db.session.add(post)
        db.session.commit()
        flash("Post ha sido actualizado")
        return redirect(url_for('public.post', id=id))
    else:
        form.title.data=post.title
        form.slug.data=post.slug
        form.content.data=post.content
        return render_template('public/edit.html', form=form)
@public_bp.route("/deletePost<int:id>")
def deletePost(id):
     postDelete=Posts.query.get_or_404(id)
     db.session.delete(postDelete)
     db.session.commit()
     flash("¡Post fue eliminado...!")
@public_bp.route('/search', methods=["POST"])
def search():
    formulario = SearchForm()
    posts = Posts.query
    if formulario.validate_on_submit():
        post.searched = formulario.search.data
        posts = posts.filter(Posts.content.like('%'+post.searched+'%'))
        posts = posts.order_by(Posts.title).all()
        return render_template("public/search.html", form=formulario, searched=post.searched, posts=posts )

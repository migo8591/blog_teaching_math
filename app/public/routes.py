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
    # if current_user.id == post.poster_id:
    else:
        form.title.data=post.title
        # form.author.data=post.author
        form.slug.data=post.slug
        form.content.data=post.content
        return render_template('public/edit.html', form=form)
        # return redirect(url_for('public.post', id=id, form=form))
        # return render_template('public/editPost.html', form=form)
    # else:
    #     flash("You Aren't Authorized to Edit This Post...")
    #     return render_template('public/editPost.html', form=form)
@public_bp.route("/deletePost<int:id>")
def deletePost(id):
     postDelete=Posts.query.get_or_404(id)
     db.session.delete(postDelete)
     db.session.commit()
     flash("¡Post fue eliminado...!")
     return redirect(url_for('public.index'))
# def deletePost(id):
#     postDelete=Posts.query.get_or_404(id)
#     ide=current_user.id
#     if ide== postDelete.poster.id:       
#         try:
#             db.session.delete(postDelete)
#             db.session.commit()
#             flash("¡Post fue eliminado...!")
#             return redirect(url_for('public.index'))
        
#         except:
#                 flash("Whoops! There was a problem deleting post")      
#                 #Grab all the posts from the databases:
#                 posts = Posts.query.order_by(Posts.date_posted)
#                 return render_template("public/posts.html", posts= posts)
#     else:
#         flash("You Aren't Authorized to Delete This Post")
#         return redirect(url_for('public.post', id=id))

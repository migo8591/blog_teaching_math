from flask import render_template, flash, redirect, url_for, session, request, current_app, send_from_directory
from flask_login import login_user, login_required, logout_user
from .webforms import UserForm, LoginForm, UpdateForm
from ..models import Users
from ..extensions import db, bcrypt
from . import auth_bp
from werkzeug.utils import secure_filename
import uuid as uuid
import os


@auth_bp.route("/sign", methods=['GET','POST'])
def sign():
    formulario= UserForm()
    if formulario.validate_on_submit():
        user=Users.query.filter_by(email=formulario.email.data).first()
        if user is None:
            hashed_pw=bcrypt.generate_password_hash(formulario.password_hash.data).decode('utf-8')
            user=Users(username=formulario.username.data,name=formulario.name.data, email=formulario.email.data, about_me=formulario.aboutme.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        formulario.name.data=''    
        formulario.username.data=''    
        formulario.email.data='' 
        formulario.password_hash.data='' 
        flash("Usuario ha sido creado")
        return redirect(url_for('auth.login'))
    return render_template("auth/sign.html", form=formulario)

@auth_bp.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user=Users.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login Successfull!!")
                return redirect(url_for('public.index'))
            else:
                flash("Wrong Password - Try Again!")
        else:
            flash("That User Doesn't Exist! Try Again...")        
    our_users = Users.query.order_by(Users.date_added)
    return render_template("auth/login.html",form =form, usuarios=our_users) 
@auth_bp.route("/dashboard/<int:id>", methods=['GET','POST'])
@login_required
def dashboard(id):
    print(id)
    perfil = Users.query.get_or_404(id)
    return render_template("auth/dashboard.html", profile = perfil )
@auth_bp.route("/editProfile/<int:id>", methods=['GET','POST'])
def editProfile(id):
    form = UpdateForm()
    profile = Users.query.get_or_404(id)
    if form.validate_on_submit():
        profile.email=form.email.data
        profile.about_me=form.aboutme.data
        # Actually pulling in the file
        archivo=request.files['post_image']
        #Grab Image name
        pic_filename = secure_filename(archivo.filename)
        #Set UUID
        pic_name = str(uuid.uuid1())+"_"+pic_filename
        #Se crea el directorio si no existe
        # images_dir = current_app.config['POSTS_IMAGES_DIR']
        # os.makedirs(images_dir, exist_ok=True)
        # file_path = os.path.join(images_dir, pic_name)
        # file.save(file_path)
        #Saving the imagen as bald:
        archivo.save("app/static/pic/"+pic_name)
        # profile.profile_pic.save(os.path.join(current_app.config['UPLOAD_FOLDER'], pic_name))
        profile.profile_pic=pic_name
        try:
            db.session.commit()
            flash("Profile had been updated")
            return  redirect(url_for('auth.dashboard', id=id))
        except:
            flash("Error! Looks like there was an error")
            return render_template("dashboard.html")
    else:
        print("middle testing")
        form.email.data=profile.email
        form.aboutme.data=profile.about_me
        return render_template('auth/profileEdit.html', form=form, id=id)



@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("Closed Session...!")
    return redirect(url_for('auth.login'))

@auth_bp.route('/img/<imagen>')
def imagen_profile(imagen):
    return send_from_directory(os.path.join('static/images/'),imagen)
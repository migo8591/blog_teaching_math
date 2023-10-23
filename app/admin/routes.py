from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from . import admin_bp


@admin_bp.route("/admin")
@login_required
def admin():
   id = current_user.id
   if id == 1:
      return render_template("admin/admin.html")
   else:
      flash("Sorry but you are not a admin")
      return redirect(url_for('auth.dashboard'))
   
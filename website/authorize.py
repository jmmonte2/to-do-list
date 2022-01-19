from flask import Blueprint, render_template, request,redirect,url_for
from werkzeug.utils import redirect

from website.views import home
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

authorize = Blueprint('authorize', __name__)



@authorize.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

    
        if email == "" and password == "":
            return render_template("login.html", empty_email=True, empty_password=True)

        else:
            if user:
                if check_password_hash(user.password, password):
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    return render_template("login.html", user=user)
            else:
                return render_template("login.html")
    
    else: 
        return render_template("login.html")
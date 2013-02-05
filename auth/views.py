# This is where we generate the html data and or json

from flask.views import View, MethodView
from flask.templating import render_template
from flask import redirect, url_for, flash

from lib.flask_login import login_user, current_user, logout_user

from auth import models as auth_models
from auth import forms as auth_forms
from auth import utils as auth_utils


class Register(MethodView):
    def get(self):
        form = auth_forms.RegisterForm()
        return render_template("auth/register.html", form=form)

    def post(self):
        form = auth_forms.RegisterForm()

        # Validate form
        if form.validate_on_submit():

            # Salt password
            password, salt = auth_utils.salt_password(form.password.data)

            # Create new user
            new_user = auth_models.User(username=form.username.data,
                email=form.email.data,
                password=password,
                salt=salt)
            new_user.put()

            # Login as user
            login_user(new_user, remember=form.remember.data)

            # Redirect to User page
            flash('Login Successful', 'success')
            return redirect(url_for('user'))

        else:

            # Show error messages
            for field in form.errors:
                for error in form.errors[field]:
                    flash(error, 'error')

            # Stay on registration page
            return redirect(url_for('register'))


class Login(MethodView):
    def get(self):
        form = auth_forms.LoginForm()
        return render_template("auth/login.html", form=form)

    def post(self):
        form = auth_forms.LoginForm()

        # Validate Form
        if form.validate_on_submit():

            # Authenticate user
            if auth_utils.authenticate(form.email.data, form.password.data):

                # Login as user
                user = auth_models.User.all().filter('email =', form.email.data).fetch(1)[0]
                login_user(user, remember=form.remember.data)

                # Redirect to user page
                flash('Logged In', 'success')
                return redirect(url_for('user'))

            else:
                flash('Invalid Credentials', 'error')

        else:

            # Show error messages
            for field in form.errors:
                for error in form.errors[field]:
                    flash(error, 'error')

            # Stay on login page
            return redirect(url_for('login'))


class Logout(View):
    def dispatch_request(self):
        logout_user()
        flash('You are logged out', 'info')
        return redirect(url_for('home'))


class User(View):
    def dispatch_request(self):
        return render_template('auth/user.html',  user=current_user)
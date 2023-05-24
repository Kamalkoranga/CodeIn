from . import auth
from flask import render_template
from .forms import LoginForm, RegistrationForm
from ..models import User
from flask_login import login_user, login_required, current_user
from flask import request, url_for, redirect, flash
from .. import db
import random


@auth.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, True)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = ''.join(random.choice(form.email.data[:5]) for _ in range(len(form.email.data[:5])))
        user = User(
            email=form.email.data,
            username=username,
            password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/signup.html', form=form)

# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from app import db
from app.forms import RegistrationForm


@app.route('/')
@app.route('/index')
def index():
    #user = {'username': 'DENIS'}
    return render_template('index.html', title='Home') #user=user)

@app.route('/news')
def news ():
    return render_template('news.html')

@app.route('/blog')
def blog ():
    return render_template('blog.html')

@app.route('/shop')
def shop ():
    return render_template('shop.html')

@app.route('/about')
def about ():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login ():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first() # запрос к БД на поиск имени пользователя
        if user is None or not user.check_password(form.password.data):  # запрос к БД на соответствие пароля
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        # asd = str(user)
        # asd = asd.strip('<>').lstrip('User')
        # flash('Welcome, ' + asd)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'},
        {'author': user, 'body': 'Test post #3'},
        {'author': user, 'body': 'Test post #4'},
        {'author': user, 'body': 'Test post #5'}
    ]
    return render_template('user.html', user=user, posts=posts)
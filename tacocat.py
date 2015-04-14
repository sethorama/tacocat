from flask import (Flask, g, render_template, flash, redirect, 
                  url_for, abort)
from flask.ext.bcrypt import generate_password_hash, check_password_hash
from flask.ext.login import (LoginManager, login_user, logout_user,
                            login_required, current_user)

import forms
import models


DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'a;lksj0978()*&0asja07sdashdakh32yD)*Y##&#Yyh'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the database connection after each request"""
    g.db.close()
    return response


@app.route('/')
def index():
    tacos = models.Taco.select()
    return render_template('index.html', tacos=tacos)


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Success, you registered!", "success")
        models.User.create_user(
            email=form.email.data,
            password=form.password.data
        )
        user = models.User.get(models.User.email == form.email.data)
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Email and/or password doesn't match.", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in!", "success")
                return redirect(url_for('index'))
            else:
                flash("Email and/or password doesn't match.", "error")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out.", "success")
    return redirect(url_for('index'))


@app.route('/taco', methods=('POST', 'GET'))
@login_required
def taco():
    form = forms.TacoForm()
    if form.validate_on_submit():
        models.Taco.create_taco(user=g.user._get_current_object(),
                                protein=form.protein.data.strip(),
                                cheese=form.cheese.data.strip(),
                                shell=form.shell.data.strip(),
                                extras=form.extras.data.strip())
        flash("Taco Added!", "success")
        return (redirect(url_for('index')))
    return render_template('taco.html', form=form)


if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            email='sethorama@bassplayer.st',
            password='password'
        )
    except ValueError:
        pass
    app.run(debug=DEBUG)

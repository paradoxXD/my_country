import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from flask import Flask, render_template, url_for, flash, redirect, session, g, request
from forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt
from model import User, Get_password, already_exist



import pymysql.cursors


# from forms import RegistrationForm, LoginForm

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY= os.urandom(24),
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    bcrypt = Bcrypt(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/',methods=['GET', 'POST'])
    @app.route('/portfolio',methods=['GET', 'POST'])
    def hello():
        
        return render_template('portfolio.html',title="portfolio", user_email=session.get("user"), enable=1)
        


    @app.before_request
    def before_request():
        g.user = None
        if 'user' in session:
            g.user = session['user']

    @app.route('/lounge',methods=['GET', 'POST'])
    def lounge():
        return render_template('lounge.html', title="lounge", user_email=session.get("user"), enable=2)

    @app.route('/status')
    def notifications():
        return render_template('status.html', title="status",user_email=session.get("user"), enable=3)

    @app.route('/user')
    def user():
        return render_template('user.html', title='users', user_email=session.get("user"), enable=4)

    @app.route('/tables')
    def tables():
        return render_template('tables.html', user_email=session.get("user"), enable=5)

    @app.route('/typography')
    def typography():
        return render_template('typography.html', user_email=session.get("user"), enable=6)
        

    @app.route('/register', methods=['GET','POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            
            if already_exist(username=form.username.data, email=form.email.data):
                flash('The email or username has been used. Please check username and password', 'danger')
                return render_template('register.html', user_email=session.get("user"), title='register', form=form, enable=7)

            
            # cannot validate whether the email is in the database or not
    
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            
            # create user
            User(username=form.username.data, email=form.email.data, password=hashed_password)
            
            flash('Account created for {}!'.format(form.username.data), 'success')
            return redirect(url_for('login'))
        return render_template('register.html', user_email=session.get("user"), title='Register', form=form, enable=7)

    @app.route('/login', methods=['GET','POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            
            getPass = Get_password(form.email.data)

            if getPass == None:
                flash('Login Unsuccessful. Please check username and password', 'danger')
                return redirect(url_for('login'))

            if bcrypt.check_password_hash(getPass, form.password.data) is True:
                flash('You have been logged in!', 'success')
                session['user'] = form.email.data
                return redirect(url_for('hello'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
        return render_template('login.html', user_email=session.get("user"), title='Login', form=form, enable=8)

    @app.route('/drop')
    def drop():
        session.pop("user",None)
        return redirect(url_for('hello'))




    return app


if __name__ == "__main__":
    
    app = create_app()
    app.run(debug=True)
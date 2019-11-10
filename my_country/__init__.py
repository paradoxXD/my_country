import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from flask import Flask, render_template, url_for, flash, redirect, session, g
from forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt
from model import User, Get_password



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
    @app.route('/portfolio')
    def hello():
        return render_template('portfolio.html',title="portfolio", user_email=session.get("user"))

    @app.before_request
    def before_request():
        g.user = None
        if 'user' in session:
            g.user = session['user']

    @app.route('/icons')
    def icons():
        return render_template('icons.html', title="icons", user_email=session.get("user"))

    @app.route('/notifications')
    def notifications():
        return render_template('notifications.html', user_email=session.get("user"))

    @app.route('/user')
    def user():
        return render_template('user.html', title='users', user_email=session.get("user"))

    @app.route('/tables')
    def tables():
        return render_template('tables.html', user_email=session.get("user"))

    @app.route('/typography')
    def typography():
        return render_template('typography.html', user_email=session.get("user"))
        

    @app.route('/register', methods=['GET','POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
    
            # cannot validate whether the email is in the database or not
    
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            create_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            
            connection = pymysql.connect("112.124.46.178", "root", "rootroot", "my_country")
            
            try:
                with connection.cursor() as cursor:

                    sql = create_user
                    cursor.execute(sql)
                
                    connection.commit()
            finally:
                connection.close()



            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', title='Register', form=form)

    @app.route('/login', methods=['GET','POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            
            connection = pymysql.connect("112.124.46.178", "root", "rootroot", "my_country")
            getPass = Get_password(form.email.data)
            try:
                with connection.cursor() as cursor:

                    sql = getPass
                    cursor.execute(sql)
                    result = cursor.fetchone()
            finally:
                connection.close()


            if bcrypt.check_password_hash(result[0], form.password.data) is True:
                flash('You have been logged in!', 'success')
                session['user'] = form.email.data
                return render_template('portfolio.html', title='portfolio', form=form)
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
        return render_template('login.html', title='Login', form=form)



    return app

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

# from forms import RegistrationForm, LoginForm

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='11267e08ae4320abfe7252612fb97a48',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

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
        return render_template('portfolio.html',title="portfolio")

    @app.route('/icons')
    def icons():
        return render_template('icons.html', title="icons")

    @app.route('/notifications')
    def notifications():
        return render_template('notifications.html')

    @app.route('/user')
    def user():
        return render_template('user.html', title='users')

    @app.route('/tables')
    def tables():
        return render_template('tables.html')

    @app.route('/typography')
    def typography():
        return render_template('typography.html')
        

    @app.route('/register', methods=['GET','POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('hello'))
        return render_template('register.html', title='Register', form=form)

    @app.route('/login', methods=['GET','POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            if form.email.data == 'admin@blog.com' and form.password.data == 'password':
                flash('You have been logged in!', 'success')
                return redirect(url_for('hello'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
        return render_template('login.html', title='Login', form=form)



    return app

import os

from flask import Flask, render_template, url_for


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
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
        return render_template('portfolio.html')

    @app.route('/icons')
    def icons():
        return render_template('icons.html')

    @app.route('/notifications')
    def notifications():
        return render_template('notifications.html')

    @app.route('/user')
    def user():
        return render_template('user.html')

    @app.route('/tables')
    def tables():
        return render_template('tables.html')

    @app.route('/typography')
    def typography():
        return render_template('typography.html')

    


    return app

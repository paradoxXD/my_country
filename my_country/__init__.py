import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from flask import Flask, render_template, url_for, flash, redirect, session, g, request
from forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt
from model import User, Get_password, already_exist, Time, get_stock_lounge_week, get_stock_lounge_month,get_stock_lounge_year,get_All_Stock,get_Recomd,get_buy,get_sell,money_enough,quantity_enough,transac_records, get_balance, get_rank, get_portfolio_list, get_yield
from datetime import datetime



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



    @app.before_request
    def before_request():
        g.user = None
        if 'user' in session:
            g.user = session['user']

    @app.route('/',methods=['GET', 'POST'])
    @app.route('/lounge',methods=['GET', 'POST'])
    def lounge():
        
        All_Stocks = get_All_Stock()

        if request.method == 'POST':
            something = request.form.get('stock')
            print(something)
            # use something to get data
            # please finish this part

        return render_template('lounge.html', title="lounge",time=session.get('time'), user_email=session.get("user"), enable=2,tasks=All_Stocks)

    @app.route('/status')
    def notifications():
        return render_template('status.html', title="status",time=session.get('time'),user_email=session.get("user"), enable=3)

    @app.route('/user')
    def user():
        return render_template('user.html', title='users',time=session.get('time'), user_email=session.get("user"), enable=4)

    @app.route('/tables')
    def tables():
        return render_template('tables.html',title='Buy&Sell',time=session.get('time'), user_email=session.get("user"), enable=5)


    @app.route('/register', methods=['GET','POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            
            if already_exist(username=form.username.data, email=form.email.data):
                flash('The email or username has been used. Please check username and password', 'danger')
                return render_template('register.html',time=session.get('time'), user_email=session.get("user"), title='register', form=form, enable=7)

            
            # cannot validate whether the email is in the database or not
    
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            
            now = datetime.now()
            user_time = now.strftime("%Y-%m-%d %H:%M:%S")

            # create user
            User(username=form.username.data, email=form.email.data, password=hashed_password, datetime=user_time)
            
            flash('Account created for {}!'.format(form.username.data), 'success')
            return redirect(url_for('login'))
        return render_template('register.html', time=session.get('time'),user_email=session.get("user"), title='Register', form=form, enable=7)

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
                session['time'] = Time(form.email.data)
                # print(session.get('time'))
                return redirect(url_for('lounge'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
        return render_template('login.html', time=session.get('time'),user_email=session.get("user"),title='Login', form=form, enable=8)

    @app.route('/drop')
    def drop():
        session.pop("user",None)
        session.pop("time",None)
        return redirect(url_for('lounge'))

    @app.route('/engine',methods=['GET','POST'])
    def engine():
        
        stock = request.args.get('stock')
        time = request.args.get('time')
        
        print(stock)
        print(time)
        result = get_stock_lounge_week(stock,time)


        return result

    @app.route('/engine2',methods=['GET','POST'])
    def engine2():
        
        stock = request.args.get('stock')
        
        time = request.args.get('time')
        
        print(stock)
        print(time)
        result = get_stock_lounge_month(stock,time)


        return result

    @app.route('/engine3',methods=['GET','POST'])
    def engine3():
        
        stock = request.args.get('stock')
        
        time = request.args.get('time')
        
        print(stock)
        print(time)
        result = get_stock_lounge_year(stock,time)


        return result

    
    @app.route('/recomd',methods=['GET','POST'])
    def recomd():  
        time = request.args.get('time')
        result = get_Recomd(time)
        return result


    @app.route('/buy',methods=['GET','POST'])
    def buy():  
        time = request.args.get('time')
        stock = request.args.get('stock')
        quantity=request.args.get('quantity')
        email=session.get("user")

        if money_enough(stock,quantity,email,time)==False:
            flash("You don't have enough money!","danger")
            return "1"
        else:
            get_buy(time,stock,quantity,email)
            flash("Successfully buy! Check them in your asset.","success")
            return "1"

    @app.route('/sell',methods=['GET','POST'])
    def sell():  
        time = request.args.get('time')
        stock = request.args.get('stock')
        quantity=request.args.get('quantity')
        email=session.get("user")
        if quantity_enough(stock,quantity,email)==False:
            flash("You don't have enough stocks!","danger")
            return "1"
        else:
            get_sell(time,stock,quantity,email)
            flash("Successfully sell! Check them in your asset.","success")
            return "1"
        
    @app.route('/record',methods=['GET','POST'])
    def record():  
        email=session.get("user")
        result = transac_records(email)
        return result

    @app.route('/balance',methods=['GET','POST'])
    def balance():  
        email=session.get("user")
        result = get_balance(email)
        return result

    @app.route('/rank',methods=['GET','POST'])
    def rank():  
        email=session.get("user")
        result = get_rank(email)
        return result

    @app.route('/port_list',methods=['GET','POST'])
    def port_list():  
        email=session.get("user")
        time=request.args.get('time')
        result = get_portfolio_list(email,time)
        return result

    @app.route('/yieldrate',methods=['GET','POST'])
    def yieldrate():  
        email=session.get("user")
        time=request.args.get('time')
        result = get_yield(email,time)
        return result


        
    @app.route('/port',methods=['GET','POST'])
    def port():
        return render_template('portfolio.html')

    return app





if __name__ == "__main__":
    
    app = create_app()
    app.run(debug=True)
from flask import Flask, request, redirect, url_for, session
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mail import *
from random import *
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite3'
app.secret_key = b'wserfgthj'
db=SQLAlchemy(app)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USERNAME"] = "tp940648@gmail.com"
app.config["MAIL_PASSWORD"] = "mnkflauljryiyako"
mail = Mail(app)

OTP = randint(1000,9999)

class user(db.Model):
    id = db.Column('user_id', db.Integer, primary_key = True) 
    name = db.Column(db.String(100))
    email_id = db.Column(db.String(100),unique=True)
    password = db.Column(db.String(100))
    mobile_no = db.Column(db.String(10),unique=True)

# <<<<<--------------------Ragister Page---------------------------->>>>>

@app.route('/', methods= ['POST', 'GET'])
def register_page():
    if request.method == 'POST':
        name = request.form['name'] 
        email_id = request.form['email_id'] 
        password = request.form['password']
        mobile_no = request.form['mobile_no']
        users = user(name=name, email_id=email_id, password=password, mobile_no=mobile_no) 
        db.session.add(users)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('ragister.html')

# <<<<<--------------------Login Page---------------------------->>>>>

@app.route('/login', methods= ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email_id = request.form['email_id']
        password = request.form['password']
        login = user.query.filter_by(email_id= email_id, password= password).first()
        if login is not None:
            session['user']=login.email_id
            return redirect(url_for('welcome_page'))
        else:
            return "please enter valid email and password"
    return render_template('login.html')

# <<<<<--------------------Home Page---------------------------->>>>>
    
@app.route('/home', methods= ['POST', 'GET'])
def welcome_page():
    if 'user' not in session.keys():
        return redirect(url_for('login'))
    return render_template('home.html')    

# <<<<<--------------------Forgot Password Page---------------------------->>>>>

# @app.route('/forgotpass', methods= ['POST', 'GET'])
# def forgot_password():
#     if request.method == 'POST':
#         email_id = request.form['email_id']
#         pass1 = request.form['password']
#         repeat_password = request.form['repeat-password'] 
#         newpass = user.query.filter_by(email_id=email_id).first()
#         if newpass!= None:
#             if pass1 == repeat_password:
#                 newpass.password = pass1
#                 db.session.commit()
#                 return redirect(url_for('login'))
#         return render_template('forgotpass.html')    
#     return render_template('forgotpass.html')    
       
# <<<<<--------------------Change Password Page---------------------------->>>>>       

@app.route('/changepass', methods= ['POST', 'GET'])
def change_password():
    if request.method == 'POST':
        email = request.form['email_id']
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        repeat_password = request.form['repeat_password']
        changep = user.query.filter_by(email_id=email, password=old_password).first()
        
        if changep != None:
            if new_password == repeat_password:
                changep.password = new_password
                db.session.commit()
                return redirect(url_for('login'))
        return render_template('changepass.html')    
    return render_template('changepass.html')        
    

# <<<<<--------------------Forgot Password By mail ---------------------------->>>>>    

@app.route('/mail', methods= ['POST', 'GET'])
def send_mail():
    if request.method == 'POST':
        email = request.form['email_id']
        session['gmail']=email
        msg = Message(
                    sender ='tp940648@gmail.com',
                    recipients = [email]
                )
        msg.html = '<a href="http://127.0.0.1:5000/password">click</a>'
        mail.send(msg)
        return 'Sent'
        
    return render_template('mail.html')

# <<<<<--------------------verify password Page---------------------------->>>>>

@app.route('/password', methods= ['POST', 'GET'])
def psw():
    if request.method == 'POST':
        email1 = session['gmail']
        # print(email1)
        pass1 = request.form['password']
        repeat_password = request.form['repeat-password'] 
        obj = user.query.filter_by(email_id=email1).first()
        if pass1 == repeat_password:
            obj.password = pass1
            db.session.commit()
            return redirect(url_for('login'))
        return render_template('password.html')      
    return render_template('password.html')


# <<<<<--------------------Forgot Password By otp ---------------------------->>>>>

@app.route('/mail_otp', methods= ['POST', 'GET'])
def mail_otp():
    if request.method == 'POST':
        email = request.form['email_id']
        session['gmail']=email
        msg = Message(
                    sender ='tp940648@gmail.com',
                    recipients = [email]
                )
        msg.body = str(OTP)
        mail.send(msg)
        session['OTP']= str(OTP)
        return redirect(url_for('verify_otp'))
    else:
        return render_template('mail2.html')
    

# <<<<<--------------------verify otp Page---------------------------->>>>>    

@app.route('/otp', methods= ['POST', 'GET'])
def verify_otp():
    if request.method == 'POST':
        user_otp = request.form['otp']
        # print(session['OTP'])
        # print(user_otp)
        if user_otp == session['OTP']:
            return redirect(url_for('psw'))
    return render_template('otp_validation.html')    
    # return render_template('otp_validation.html')



with app.app_context():
    db.create_all()     









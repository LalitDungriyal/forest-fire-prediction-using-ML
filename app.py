from flask import Flask, render_template, redirect, request, url_for, session
from flaskext.mysql import MySQL
from flask import Flask
from flask_mail import Mail, Message
import bcrypt
import pymysql
import re
import pickle
import numpy as np


app= Flask(__name__)

model=pickle.load(open('model.pkl','rb'))

app.secret_key="124$89afd#*%42*(23("

mysql=MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='projectDB'
mysql.init_app(app)


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'lalitdungriyal4@gmail.com'
app.config['MAIL_PASSWORD'] = 'Mypass123*'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)



@app.route('/')
def home():
    return render_template("home.html")

@app.route('/forest_fire')
def forest_fire():
    if 'loggedin' in session:
        return render_template("predict.html")

    return render_template("login.html") 

@app.route('/predict',methods=['POST','GET'])
def predict():
    conn=mysql.connect()
    cursor=conn.cursor(pymysql.cursors.DictCursor)

    features=[float(x) for x in request.form.values()]
    final=[np.array(features)]
    print(features)
    print(final)
    prediction=model.predict_proba(final)
    output='{0:.{1}f}'.format(prediction[0][1], 2)

    userid=int(session['id'])
    username=session['username']

    

    cursor.execute('insert into activities values(%s,%s,%s,%s,%s,%s)',(int(userid),username,float(features[0]),float(features[1]),float(features[2]),float(output)*100))
    conn.commit()

    if output>str(0.5):
        return render_template('predict.html',pred='Your Forest is in Danger.\nPercentage of fire occuring is {}%'.format(float(output)*100),bhai="danger")
    else:
        return render_template('predict.html',pred='Your Forest is safe.\n Percentage of fire occuring is {}%'.format(float(output)*100),bhai="safe")



@app.route('/profile')
def profile():
    return render_template("profile.html")

@app.route('/login',methods=['GET','POST'])
def login():
    conn=mysql.connect()
    cursor=conn.cursor(pymysql.cursors.DictCursor)
    msg=''

    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        username=request.form['username']
        password=request.form['password']
        cursor.execute('Select * from accounts where username=%s and password=%s',(username,password))
        account=cursor.fetchone()

        if account:
            session['loggedin']=True
            session['id']=account['id']
            session['username']=username

            return redirect(url_for('home'))
        else:
            msg='Invalid Credentials'

    return render_template('login.html',msg=msg)

@app.route('/register',methods=['GET','POST'])
def register():
    conn=mysql.connect()
    cursor=conn.cursor(pymysql.cursors.DictCursor)

    msg=''

    if 'cpass' in request.form and 'fullname' in request.form and 'email' in request.form and 'username' in request.form and 'password' in request.form:

        if(request.form['password']!=request.form['cpass']):
            msg="password doesn't match" 
            return url_for('register')

        username=request.form['username']
        password=request.form['password']
        fullname=request.form['fullname']
        email=request.form['email']

        cursor.execute('select * from accounts where username=%s',(username))

        account=cursor.fetchone()

        if account:
            msg='user already exists'
        elif not re.match(r'[A-Za-z0-9]+',username):
            msg='username not valid'
        else:
            cursor.execute('insert into accounts values(NULL, %s, %s, %s, %s)',(fullname,username,password,email))
            conn.commit()        

            msg='successfully registered'
            return redirect(url_for('login'))
    else:
        msg='please fill out the form'
    return render_template("register.html",msg=msg)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/query",methods=['POST'])
def query():
    email=request.form['email']
    description=request.form['description']
    msg = Message(
                "Feedback from User",
                sender ='lalitdungriyal4@gmail.com',
                recipients = ['lalitdungriyal5@gmail.com']
               )
    msg.body =description
    mail.send(msg)
    return redirect(url_for("/about"))

@app.route("/logout")
def logout():
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('username',None)
    return redirect(url_for('login'))

if(__name__ =='__main__'):
    app.run(debug=true)
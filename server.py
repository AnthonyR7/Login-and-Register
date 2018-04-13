from flask import Flask, request, redirect, render_template, session, flash,url_for
from mysqlconnection import MySQLConnector
import re
import md5
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = "ThisIsSecret!"
mysql = MySQLConnector(app,'log')
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/process', methods=['POST'])
def process():
    if len(request.form['email']) < 1:
        flash("Email cannot be blank!")
        return redirect('/')
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!")
        return redirect('/')
    if len(request.form['f_name']) < 2 :
        flash("First Name be more then 2 characters long")
        return redirect('/')
    elif len(request.form['l_name']) < 2 :
        flash("Last Name be more then 2 characters long")
        return redirect('/')
    elif (request.form['f_name'].isalpha()) != True:
        flash("Fist Name numbers in First name!",'no_num')
        return redirect('/')
    elif (request.form['l_name'].isalpha()) != True:
        flash("Last Name numbers in First name!",'no_num')
        return redirect('/')
    elif (request.form['pass_word']) < 8:
        flash("Pass word must be at least 8 characters in lengh.")
        return redirect('/')
    elif (request.form['pass_word']) != (request.form['confirm_password']):
        flash("Pass word does not match Confirmation input",'issue')
        return redirect('/')
    else:
        pass_word = md5.new(request.form['pass_word']).hexdigest()
        hashed_confirm = md5.new(request.form['confirm_password']).hexdigest()
        query = "INSERT INTO users (id,first_name,last_name,email,pass_word) VALUES (:id,:first_name,:last_name,:email,:pass_word)"
        data = {
                'first_name':request.form['f_name'],
                'last_name':request.form['l_name'],
                'email': request.form['email'],
                'pass_word':pass_word
                }
        mysql.query_db(query, data)
        if session.get('user') == None:
    		for id in data:
                    user_id = session['user']
        if not session.get('user') == None:
            for id in data:
                    session.query(users).get()
        return redirect(url_for('success'))
    return redirect("/")
@app.route('/success', methods = ['GET','POST'])
def success():
    # if session.get('user') == None:
	# 	session['gold'] = 0
    #     session.query(user)
    # return render_template('success.html')
    return render_template('access.html')
app.run(debug=True)

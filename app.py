from datetime import timedelta

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)

app.secret_key = '123'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)


# root of our website
@app.route('/')
def defaultP():
    return redirect('/FirstHW')

@app.route('/FirstHW')
def homePage():
    return render_template('FirstHW.html')

@app.route('/ContactMe')
def contact_page():
    return render_template('ContactMe.html')

users = {1: {"name": "lebron", "email": "lebron@gmail.com"},
         2: {"name": "Kevin", "email": "KD@gmail.com"},
         3: {"name": "Jordan", "email": "jordan@gmail.com"},
         4: {"name": "larry", "email": "larrybird@gmail.com"},
         5: {"name": "magic", "email": "magicj@gmail.com"}}

@app.route('/assignment3_2' ,methods=['GET', 'POST'])
def ass3_2():
    if request.method == 'POST':
        u_name_regis = request.form['uname_r']
        u_email_regis = request.form['email_r']
        for user in users :
            if u_name_regis == users[user]["name"]:
                if u_email_regis == users[user]["email"]:
                    session['username'] = u_name_regis
                    session['loggedIn'] = True
                    return render_template('assignment3_2.html', message="User already signed up")
                else:
                    return render_template('assignment3_2.html', message="Wrong email")
        users.update({list(users.keys())[-1]+1: {"name":u_name_regis,"email":u_email_regis}})
        session['username'] = u_name_regis
        session['loggedIn'] = True
        return render_template('assignment3_2.html', message_new="New user signed up")
    elif 'uname' in request.args:
        uname = request.args['uname']
        for user in users:
            if users[user]["name"] == uname:
                return render_template('assignment3_2.html',user_name=users[user]["name"],user_email=users[user]["email"])
            if uname == "":
                return render_template('assignment3_2.html',users=users)
    else:
        return render_template('assignment3_2.html')

@app.route('/log_out')
def log_out():
    session['loggedIn'] = False
    session.clear()
    return redirect(url_for('ass3_2'))

@app.route('/assignment3_1')
def coffeeUmayLike():
    coffees = {'Espresso' :9 , 'Double Espresso' :10 , 'Cappuchino' : 14, 'latte' : 12, 'Macciato' : 9}
    return render_template('assignment3_1.html',
                           user_coffee=coffees,
                           )


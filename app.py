from datetime import timedelta

from flask import Flask, redirect, render_template, request, session, url_for
from assignment_4.assignment_4 import assignment_4

import mysql.connector

app = Flask(__name__)
app.register_blueprint(assignment_4)

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

# ------------------------------------------------- #
# ------------- DATABASE CONNECTION --------------- #
# ------------------------------------------------- #
# def interact_db(query, query_type: str):
#     return_value = False
#     connection = mysql.connector.connect(host='localhost',
#                                          user='root',
#                                          passwd='root1234',
#                                          database='serverdb')
#     cursor = connection.cursor(named_tuple=True)
#     cursor.execute(query)
#     #
#
#     if query_type == 'commit':
#         # Use for INSERT, UPDATE, DELETE statements.
#         # Returns: The number of rows affected by the query (a non-negative int).
#         connection.commit()
#         return_value = True
#
#     if query_type == 'fetch':
#         # Use for SELECT statement.
#         # Returns: False if the query failed, or the result of the query if it succeeded.
#         query_result = cursor.fetchall()
#         return_value = query_result
#
#     connection.close()
#     cursor.close()
#     return return_value


# query = "INSERT INTO try_table_1(name) VALUES ('try_name_1')"
# interact_db(query=query, query_type='commit')
#
# query = "select * from try_table_1"
# query_result = interact_db(query=query, query_type='fetch')
# print(query_result)
# ------------------------------------------------- #
# ------------------------------------------------- #


# ------------------------------------------------- #
# ------------------- SELECT ---------------------- #
# ------------------------------------------------- #
# @app.route('/users')
# def users():
#     query = 'select * from users'
#     users_list = interact_db(query, query_type='fetch')
#     return render_template('users.html', users=users_list)
# # ------------------------------------------------- #
# # ------------------------------------------------- #
#
#
# # ------------------------------------------------- #
# # -------------------- INSERT --------------------- #
# # ------------------------------------------------- #
# @app.route('/insert_user', methods=['POST'])
# def insert_user():
#     name = request.form['name']
#     email = request.form['email']
#     password = request.form['password']
#     print(f'{name} {email} {password}')
#     query = "INSERT INTO users(name, email, password) VALUES ('%s', '%s', '%s')" % (name, email, password)
#     interact_db(query=query, query_type='commit')
#     return redirect('/users')
#
#
# # ------------------------------------------------- #
# # ------------------------------------------------- #
#
#
# # ------------------------------------------------- #
# # -------------------- DELETE --------------------- #
# # ------------------------------------------------- #
# @app.route('/delete_user', methods=['POST'])
# def delete_user_func():
#     user_id = request.form['user_id']
#     query = "DELETE FROM users WHERE id='%s';" % user_id
#     # print(query)
#     interact_db(query, query_type='commit')
#     return redirect('/users')
#
# # ------------------------------------------------- #
# # ------------------------------------------------- #
#
#
# @app.route('/fetch_fe')
# def fetch_fe_func():
#     return render_template('fetch_frontend.html')
#
#
# def get_users_sync(from_val, until_val):
#     pockemons = []
#     for i in range(from_val, until_val):
#         res = requests.get(f'https://pokeapi.co/api/v2/pokemon/{i}')
#         print(res)
#         pockemons.append(res.json())
#     return pockemons
#
#
# async def fetch_url(client_session, url):
#     """Fetch the specified URL using the aiohttp session specified."""
#     # response = await session.get(url)
#     async with client_session.get(url, ssl=False) as resp:
#         response = await resp.json()
#         return response
#
#
# async def get_all_urls(from_val, until_val):
#     async with aiohttp.ClientSession(trust_env=True) as client_session:
#         tasks = []
#         for i in range(from_val, until_val):
#             url = f'https://pokeapi.co/api/v2/pokemon/{i}'
#             task = asyncio.create_task(fetch_url(client_session, url))
#             tasks.append(task)
#         data = await asyncio.gather(*tasks)
#     return data
#
#
# def save_users_to_session(pockemons):
#     users_list_to_save = []
#     for pockemon in pockemons:
#         pockemons_dict = {
#             'sprites': {
#                 'front_default': pockemon['sprites']['front_default']
#             },
#             'name': pockemon['name'],
#             'height': pockemon['height'],
#             'weight': pockemon['weight'],
#         }
#         users_list_to_save.append(pockemons_dict)
#     session['pockemons'] = users_list_to_save
#
#
# @app.route('/fetch_be')
# def fetch_be_func():
#     if 'type' in request.args:
#         start_time = time.time()
#         # from_val, until_val = int(request.args['from']), int(request.args['until'])
#         num = int(request.args['num'])
#         rand_start = random.randint(1, 30)
#         rand_end = rand_start + num
#         session['num'] = num
#         pockemons = []
#
#         # SYNC
#         if request.args['type'] == 'sync':
#             pockemons = get_users_sync(rand_start, rand_end)
#
#         # ASYNC
#         if request.args['type'] == 'async':
#             pockemons = asyncio.run(get_all_urls(rand_start, rand_end))
#             print('run')
#
#         end_time = time.time()
#         time_to_finish = f'{end_time - start_time: .2f} seconds'
#         session[f'{request.args["type"]}_time'] = time_to_finish
#         session[f'{request.args["type"]}_num'] = session['num']
#
#         save_users_to_session(pockemons)
#     else:
#         session.clear()
#     return render_template('fetch_backend.html')
#
#
if __name__ == '__main__':
     app.run(debug=True)


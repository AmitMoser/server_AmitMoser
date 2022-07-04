from flask import Blueprint, render_template, redirect, request, jsonify
import mysql.connector
import requests

assignment_4 = Blueprint(
    'assignment_4',
    __name__,
    static_folder='static',
    static_url_path='/assignment_4',
    template_folder='templates'
)


@assignment_4.route('/assignment_4')
def assignment4():
    return render_template('assignment_4.html')


def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         passwd='root1234',
                                         database='serverdb')
    cursor = connection.cursor(named_tuple=True)
    cursor.execute(query)
    #

    if query_type == 'commit':
        # Use for INSERT, UPDATE, DELETE statements.
        # Returns: The number of rows affected by the query (a non-negative int).
        connection.commit()
        return_value = True

    if query_type == 'fetch':
        # Use for SELECT statement.
        # Returns: False if the query failed, or the result of the query if it succeeded.
        query_result = cursor.fetchall()
        return_value = query_result

    connection.close()
    cursor.close()
    return return_value


@assignment_4.route('/insert_user', methods=['POST'])
def insert_user():
    name = request.form['name']
    email = request.form['email']
    print(f'{name} {email}')
    query = "INSERT INTO users(name, email) VALUES ('%s', '%s')" % (name, email)
    interact_db(query=query, query_type='commit')
    return render_template('/assignment_4.html', message='inserted Succesfuly')


# ------------------------------------------------- #
# ------------------- SELECT ---------------------- #
# ------------------------------------------------- #
@assignment_4.route('/get_users')
def users():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    return render_template('assignment_4.html', users=users_list)


# ------------------------------------------------- #
# ------------------- Delete ---------------------- #
# ------------------------------------------------- #
@assignment_4.route('/delete_user', methods=['POST'])
def delete_user_func():
    user_id = request.form['user_id']
    query = "DELETE FROM users WHERE id='%s';" % user_id
    interact_db(query, query_type='commit')
    return render_template('/assignment_4.html', message="Deleted Succesfuly")


@assignment_4.route('/update_user', methods=['POST'])
def update_user():
    user_id = request.form['user_id']
    name = request.form['name']
    email = request.form['email']
    old_name = request.form['old_name']
    old_email = request.form['old_email']
    if name == "":
        name = old_name
    if email == "":
        email = old_email
    query = "UPDATE users SET name = '%s',email = '%s' where id='%s';" % (name, email, user_id)
    interact_db(query, query_type='commit')
    return render_template('/assignment_4.html', message='Update Succesfully')


@assignment_4.route('/users/')
def json_print():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    return jsonify(users_list)


@assignment_4.route('/outer_source')
def extract_user():
    user_id = request.args.get('back_id')
    res = requests.get(f'https://reqres.in/api/users/{user_id}')
    result_json = res.json()
    return render_template('assignment_4.html' , users_back = result_json)



@assignment_4.route('/restapi_users')
def usersApi():
    user_id = request.args['id']
    if user_id =="":
        return jsonify ("[1],labron,lebraon@james.com")
    return redirect(f'/restapi_users/{user_id}')


@assignment_4.route('/restapi_users/<user_id>')
def printuserjson(user_id):
    query = "select * from users"
    users_list = interact_db(query, query_type='fetch')
    for user in users_list:
        if user_id == str(user.id):
            return jsonify(user)
    return jsonify("User not found")

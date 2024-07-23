from flask import Flask, jsonify
from flask_mysqldb import MySQL
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'damia_user_login'
# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_abc'

mysql = MySQL(app)
login_manager = LoginManager()
login_manager.init_app(app)
# Initialize Flask-JWT-Extended
jwt = JWTManager(app)
@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({
        'message': 'Missing Authorization Header',
        'status':401
    }), 401

# Route that requires JWT authentication
@app.route('/protected')
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

class User(UserMixin):
    def __init__(self, id, username, employee_id, first_name, last_name, nik):
        self.id = id
        self.username = username
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.nik = nik

@app.route('/login2', methods=['POST'])
def login2():
    try:
        # Get employee_id from the POST request
        data = request.json  # Assuming you are sending JSON data
        nik = data.get('nik')

        # Query database with employee_id
        cur = mysql.connection.cursor()
        cur.execute('SELECT users.*, employee.first_name, employee.last_name, employee.nik '
                    'FROM users INNER JOIN employee ON users.employee_id = employee.id '
                    'WHERE employee.nik = %s', (nik,))
        result = cur.fetchone()
        cur.close()

        if result:
            # Create a User object
            user = User(id=result[0], username=result[1], employee_id=result[2],
                        first_name=result[3], last_name=result[4], nik=result[5])

            # Login user (start user session)
            login_user(user)

            # Generate JWT token
            expires = timedelta(days=1)
            access_token = create_access_token(identity=user.id, expires_delta=expires)
            # access_token = create_access_token(identity=user.id)

            cur2 = mysql.connection.cursor()
            cur2.execute('UPDATE employee SET access_token=%s WHERE id=%s', (access_token, user.employee_id))
            mysql.connection.commit()  # Commit the transaction
            cur2.close()
            return jsonify({'data':{'access':access_token, 'id':user.employee_id}, 'status':200})
            # Return user data and token
            # return jsonify({
            #     'id': user.id,
            #     'username': user.username,
            #     'employee_id': user.employee_id,
            #     'first_name': user.first_name,
            #     'last_name': user.last_name,
            #     'nik': user.nik,
            #     'access_token': access_token
            # })

        else:
            return jsonify({'message': 'Employee not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users')
    results = cur.fetchall()
    cur.close()
    return jsonify(results)

@app.route('/test')
@jwt_required()
def test():
    cur = mysql.connection.cursor()
    cur.execute('SELECT name FROM users')
    results = cur.fetchall()
    cur.close()
    return jsonify(results)

@app.route('/employee')
@jwt_required()
def employee():
    cur = mysql.connection.cursor()
    cur.execute('SELECT users.*, employee.first_name, employee.last_name, employee.nik FROM users INNER JOIN employee ON users.employee_id = employee.id')
    results = cur.fetchall()
    cur.close()
    return jsonify({'data':results, 'status':200})

@app.route('/employee-by-id', methods=['POST'])
@jwt_required()
def employee_by_id():
    try:
        # Get employee_id from the POST request
        data = request.json  # Assuming you are sending JSON data
        employee_id = data.get('employee_id')

        # Query database with employee_id
        cur = mysql.connection.cursor()
        cur.execute('SELECT users.*, employee.first_name, employee.last_name, employee.nik '
                    'FROM users INNER JOIN employee ON users.employee_id = employee.id '
                    'WHERE employee.id = %s', (employee_id,))
        result = cur.fetchone()
        cur.close()

        if result:
            # Convert result to JSON format
            employee_data = {
                'id': result[0],
                'username': result[1],
                'employee_id': result[2],
                'first_name': result[3],
                'last_name': result[4],
                'nik': result[5]
            }
            return jsonify(employee_data)
        else:
            return jsonify({'message': 'Employee not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        # Get employee_id from the POST request
        data = request.json  # Assuming you are sending JSON data
        nik = data.get('nik')

        # Query database with employee_id
        cur = mysql.connection.cursor()
        cur.execute('SELECT users.*, employee.first_name, employee.last_name, employee.nik '
                    'FROM users INNER JOIN employee ON users.employee_id = employee.id '
                    'WHERE employee.nik = %s', (nik,))
        result = cur.fetchone()
        cur.close()

        if result:
            # Convert result to JSON format
            employee_data = {
                'id': result[0],
                'username': result[1],
                'employee_id': result[2],
                'first_name': result[3],
                'last_name': result[4],
                'nik': result[5]
            }
            return jsonify(employee_data)
        else:
            return jsonify({'message': 'Employee not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

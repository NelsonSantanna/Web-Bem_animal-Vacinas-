
import mysql.connector
from flask import Flask, render_template, request, redirect, send_from_directory, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

def create_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='0208',
        database="bem_animal2",
        auth_plugin="mysql_native_password"
    )
    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def read_responsavel():
    connection = create_connection()
    query = "SELECT * FROM responsavel"
    responsavel = execute_query(connection, query)
    connection.close()
    return responsavel

def write_responsavel(responsavel):
    print(responsavel)
    connection = create_connection()
    query = "INSERT INTO responsavel (nome, pet, telefone, email, password) VALUES (%s, %s, %s, %s, %s)"
    cursor = connection.cursor()
    try:
        cursor.execute(query, responsavel)
        connection.commit()
    except:
        print(cursor.statement)
        raise
    connection.close()



@app.route('/')
def index():
    message = 'usuário'
    error = request.args.get('error')
    return render_template('index.html', message=message, error=error)

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        pet = request.form['pet']
        telefone = request.form['telefone']
        email = request.form['email']
        password = request.form['password']

        # responsavel = read_responsavel()
        # responsavel.append({'nome': nome, 'pet': int(pet), 'telefone': telefone,'email': email})
        responsavel = (nome, pet, telefone, email, password)
        write_responsavel(responsavel)

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login')
def login():
         
    return render_template('login.html')
  

if __name__ == '__main__':
    app.run(debug=True)

 
 
 

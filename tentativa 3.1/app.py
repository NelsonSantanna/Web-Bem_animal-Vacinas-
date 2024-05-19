
import mysql.connector
from flask import Flask, render_template, request, redirect, send_from_directory, url_for, flash, session
from functools import wraps

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

def execute_query(connection, query, params=None):
    cursor = connection.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    if query.strip().upper().startswith('SELECT'):
        result = cursor.fetchall()
        return result
    connection.commit()
    return cursor.rowcount

def read_responsavel():
    connection = create_connection()
    query = "SELECT * FROM responsavel"
    responsavel = execute_query(connection, query)
    connection.close()
    return responsavel

def write_responsavel(responsavel):
    print(responsavel)
    connection = create_connection()
    query = "INSERT INTO responsavel (nome, pet, telefone, email) VALUES (%s, %s, %s, %s)" #removi password (%s)
    cursor = connection.cursor()
    try:
        cursor.execute(query, responsavel)
        connection.commit()
    except:
        print(cursor.statement)
        flash('Cadastro realizado com sucesso!')
        raise
    connection.close()

def get_responsavel_by_id(id):
    connection = create_connection()
    query = "SELECT * FROM responsavel WHERE id = %s"
    responsavel = execute_query(connection, query, (id,))
    connection.close()
    return responsavel[0]

def update_responsavel(responsavel):
    connection = create_connection()
    query = """
    UPDATE responsavel
    SET nome = %s, pet = %s, telefone = %s, email = %s
    WHERE id = %s
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query, responsavel)
        connection.commit()
    except:
        print(cursor.statement)
        raise
    connection.close()

def delete_responsavel(id):
    connection = create_connection()
    query = "DELETE FROM responsavel WHERE id = %s"
    cursor = connection.cursor()
    try:
        cursor.execute(query, (id,))
        connection.commit()
    except:
        print(cursor.statement)
        raise
    connection.close()

def check_user(email, password):
    connection = create_connection()
    query = "SELECT * FROM users WHERE email = %s AND password = %s"
    user = execute_query(connection, query, (email, password))
    connection.close()
    return user

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
   




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
        email = request.form['email'] #removi password = request.form['password]
        
        # responsavel = read_responsavel()
        # responsavel.append({'nome': nome, 'pet': int(pet), 'telefone': telefone,'email': email})
        responsavel = (nome, pet, telefone, email)  #removi , password
        write_responsavel(responsavel)
        
        return redirect(url_for('index'))
    flash('Cadastro realizado com sucesso!')
    
    return render_template('register.html')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = check_user(email, password)
        if user:
            session['logged_in'] = True
            return redirect(url_for('consulta'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/consulta')
@login_required
def consulta():
    responsaveis = read_responsavel()
    return render_template('consulta.html', responsaveis=responsaveis)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if request.method == 'POST':
        nome = request.form['nome']
        pet = request.form['pet']
        telefone = request.form['telefone']
        email = request.form['email']
        
        responsavel = (nome, pet, telefone, email, id)
        update_responsavel(responsavel)
        return redirect(url_for('consulta'))

    responsavel = get_responsavel_by_id(id)
    return render_template('edit.html', responsavel=responsavel)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    delete_responsavel(id)
    return redirect(url_for('consulta'))


  

if __name__ == '__main__':
    app.run(debug=True)

 
 
 

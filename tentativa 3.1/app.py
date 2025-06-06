import json
from mysql.connector.errors import IntegrityError
from flask import Flask, render_template, request, redirect, send_from_directory, url_for, flash, session
from functools import wraps
import mysql.connector
import smtplib
from email.mime.text import MIMEText
import uuid
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

def create_connection():
    connection = mysql.connector.connect(
        host='bemanimal2.cb2sykgqiecd.us-east-2.rds.amazonaws.com',
        user='PINGranada',
        password='Univesp2024',
        database='bem_animal2a',
        auth_plugin='mysql_native_password'
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
    connection = create_connection()
    query = "INSERT INTO responsavel (nome, pet, telefone, email, email_verified, token) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor = connection.cursor()
    try:
        cursor.execute(query, responsavel)
        flash("Cadastro efetuado com sucesso", "success")
        connection.commit()
    except mysql.connector.errors.IntegrityError as e:
        connection.rollback()
        duplicate_email = extract_duplicate_email_from_error(str(e))
        if duplicate_email:
            flash(f"O email {duplicate_email} já está cadastrado. Por favor, use outro email.", "warning")
    except Exception as e:
        flash("Ocorreu um erro inesperado. Por favor, tente novamente.", "danger")
        raise
    finally:
        cursor.close()
        connection.close()

def extract_duplicate_email_from_error(error_message):
    match = re.search(r"Duplicate entry '([^']+)' for key 'responsavel.email'", str(error_message))
    if match:
        return match.group(1)
    return None

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
    SET nome = %s, pet = %s, telefone = %s, email = %s, email_verified = %s, token = %s
    WHERE id = %s
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query, responsavel)  # Passa a tupla completa
        connection.commit()
    except:
        print(cursor.statement)
        raise
    finally:
        cursor.close()
        connection.close()

def delete_responsavel(id):
    connection = create_connection()
    query = "DELETE FROM responsavel WHERE id = %s"
    cursor = connection.cursor()
    cursor.execute(query, (id,))
    connection.commit()
    cursor.close()
    connection.close()

def check_user(email, password):
    connection = create_connection()
    query = "SELECT * FROM user WHERE email = %s AND password = %s"
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

def send_verification_email(email, token):
    msg = MIMEText("Cadastro realizado com sucesso!")
    msg['Subject'] = 'Cadastro Confirmado'
    msg['From'] = 'projetopingranada@gmail.com'
    msg['To'] = email 

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('projetopingranada@gmail.com', 'v a k o u l d t y k i d m p q r')
        server.sendmail('projetopingranada@gmail.com', email, msg.as_string())
        server.quit()
        print("Email enviado com sucesso")
    except Exception as e:
        print(f"Falha ao enviar email: {e}")

def generate_token():
    return str(uuid.uuid4())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        pet = request.form['pet']
        telefone = request.form['telefone']
        email = request.form['email']
        
        token = generate_token()
        responsavel = (nome, pet, telefone, email, False, token)
        write_responsavel(responsavel)
        send_verification_email(email, token)
        return render_template('register.html', success=True)
    return render_template('register.html', success=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = check_user(email, password)
        if user and user[0][4]:
            session['logged_in'] = True
            return redirect(url_for('consulta'))
        else:
            error = 'Você precisa verificar seu email antes de acessar o site.'
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
        
        email_verified = False
        token = ''
        
        # Incluindo o ID e valores necessários na tupla
        responsavel = (nome, pet, telefone, email, email_verified, token, id)

        # Chama o método com a tupla completa
        update_responsavel(responsavel)
        return redirect(url_for('consulta'))

    responsavel = get_responsavel_by_id(id)
    return render_template('edit.html', responsavel=responsavel)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    delete_responsavel(id)
    return redirect(url_for('consulta'))

@app.route('/verify_email/<token>')
def verify_email(token):
    connection = create_connection()
    query = "SELECT * FROM responsavel WHERE token = %s AND email_verified = %s"
    responsavel = execute_query(connection, query, (token, False))
    connection.close()
    if responsavel:
        user = responsavel[0]
        update_responsavel((user[1], user[2], user[3], user[4], True, None, user[0]))
        flash("Email verificado com sucesso!", "success")
    else:
        flash("Token inválido ou email já verificado.", "danger")
    return render_template('verify_email.html')

if __name__ == '__main__':
    app.run(debug=True)

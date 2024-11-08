import json 
from MySQLdb import IntegrityError
from flask.json import jsonify
import mysql.connector
from flask import Flask, render_template, request, redirect, send_from_directory, url_for, flash, session, get_flashed_messages
from functools import wraps
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
        port= 3306,
        database='bem_animal2a',
        auth_plugin='mysql_native_password' 
       


        


    
#        host= 'localhost',
 #       user= 'root',        
  #      password= '0208', # se conectar BD pela (porta 3306 Password = '0208'  )   (porta 3307 Password = ''  )
   #     database='bem_animal2a',
    #    auth_plugin='mysql_native_password'

    
       
        
                 
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
        flash(f"Cadastro efetuado com sucesso", "success")
        connection.commit()
    except mysql.connector.errors.IntegrityError as e:
        connection.rollback()
        duplicate_email = extract_duplicate_email_from_error(str(e))
        if duplicate_email:
            flash(f"O email {duplicate_email} já está cadastrado. Por favor, use outro email.", "warning" )
        else:
            flash(f"Cadastro efetuado com sucesso", "success")
    except Exception as e:
            flash("Ocorreu um erro inesperado. Por favor, tente novamente.", "danger")
            raise
    finally:
            cursor.close()
            connection.close()  # Certifica de que a conexão está sendo fechada

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
    SET nome = %s, pet = %s, telefone = %s, email = %s
    WHERE id = %s
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query, responsavel + (responsavel[4],))
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
    msg = MIMEText("Verifique seu email clicando em <a href='{}'>este link</a>".format(url_for('verify_email', token=token, _external=True)))
    msg['Subject'] = 'Verifique seu email'
    msg['From'] = 'projetopingranada@gmail.com'
    msg['To'] = email 

    try:
        server = smtplib.SMTP('smtp.gmail.com' , 587)
        server.starttls()  # Habilitar TLS
        server.login('projetopingranada@gmail.com', 'v a k o u l d t y k i d m p q r')  # Email e senha de aplicativo
        server.sendmail('projetopingranada@gmail.com', email, msg.as_string())
        server.quit()
        print("Email enviado com sucesso")
    except Exception as e:
        print(f"Falha ao enviar email: {e}")

def generate_token():
    return str(uuid.uuid4())

def execute_query_with_retry(connection, query, params=None, retry_count=3):
    attempt = 0
    while attempt < retry_count:
        try:
            return execute_query(connection, query, params)
        except mysql.connector.errors.DatabaseError as e:
            if e.errno == 1205:  # Código do erro para lock timeout
                attempt += 1
                print(f"Lock wait timeout, tentativa {attempt}/{retry_count}...")
                if attempt >= retry_count:
                    raise
            else:
                raise    

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
        
        token = generate_token()  # Gerar o token
        responsavel = (nome, pet, telefone, email, False, token)
        write_responsavel(responsavel)

        send_verification_email(email, token)

         # Renderiza a página com o modal de sucesso
        return render_template('register.html', success=True)

    return render_template('register.html', success=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = check_user(email, password)
        if user and user[0][4]:  # Verificar se o usuário está verificado
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

@app.route('/verify_email/<token>')
def verify_email(token):
    connection = create_connection()
    query = "SELECT * FROM responsavel WHERE email_verified = %s"
    responsavel = execute_query(connection, query, (False,))
    connection.close()
    if responsavel:
        for user in responsavel:
            # Vamos supor que o token está vinculado a um campo específico no banco de dados (precisa garantir isso no banco de dados).
            if user[4] == token:  # Certifique-se de que o campo de token seja o correto
                user = (user[1], user[2], user[3], user[4], user[0], True)  # Atualiza para verificado
                update_responsavel(user)
                return render_template('verify_email.html', message="Email verificado com sucesso!")
    
    return render_template('verify_email.html', message="Token inválido ou email já verificado")



if __name__ == '__main__':
    app.run(debug=True)

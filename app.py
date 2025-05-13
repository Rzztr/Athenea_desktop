from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta'

# Configuración de la base de datos SQLite
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Ruta base del proyecto
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')  # Ruta de la carpeta instance
DB_PATH = os.path.join(INSTANCE_DIR, 'ubicaciones.db')  # Ruta completa a la base de datos

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db = SQLAlchemy(app)

# Modelo para almacenar usuarios
class Usuario(db.Model):
    __tablename__ = 'usuarios'  # Nombre explícito de la tabla existente
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)

# Modelo para almacenar ubicaciones
class Ubicacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitud = db.Column(db.Float, nullable=False)
    longitud = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.String(100), nullable=False)

# Crear las tablas en la base de datos si no existen
with app.app_context():
    if not os.path.exists(INSTANCE_DIR):
        os.makedirs(INSTANCE_DIR)  # Crear carpeta instance si no existe
    db.create_all()  # Crear tablas en la base de datos

# Ruta de inicio
@app.route('/')
def index():
    if 'usuario' in session:
        if session['tipo'] == 'operador':
            return redirect(url_for('consulta'))
        elif session['tipo'] == 'ciudadano':
            return redirect(url_for('enviar'))
    return redirect(url_for('login'))

# Ruta de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return "Faltan datos de inicio de sesión", 400

        # Consultar la base de datos para encontrar el usuario
        user = Usuario.query.filter_by(usuario=username).first()

        # Verificar si se encontró el usuario y si la contraseña coincide
        if user and user.password == password:
            session['usuario'] = username
            session['tipo'] = user.tipo  # Guardar el tipo de usuario en la sesión

            # Redirigir según el tipo de usuario
            if user.tipo == 'operador':
                return redirect(url_for('consulta'))  # Redirigir a consulta para operadores
            elif user.tipo == 'ciudadano':
                return redirect(url_for('enviar'))  # Redirigir a enviar ubicación para ciudadanos
        else:
            return "Credenciales incorrectas", 401

    return render_template('login.html')

# Ruta para enviar ubicación
@app.route('/enviar', methods=['GET'])
def enviar():
    if 'usuario' not in session or session['tipo'] != 'ciudadano':
        return redirect(url_for('login'))
    return render_template('enviar_ubicacion.html')

# Ruta para recibir la ubicación enviada (POST)
@app.route('/enviar_ubicacion', methods=['POST'])
def enviar_ubicacion():
    if 'usuario' not in session or session['tipo'] != 'ciudadano':
        return redirect(url_for('login'))

    data = request.get_json()
    latitud = data.get('latitud')
    longitud = data.get('longitud')

    if latitud is None or longitud is None:
        return jsonify({"error": "Faltan datos de ubicación"}), 400

    nueva_ubicacion = Ubicacion(
        latitud=latitud,
        longitud=longitud,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    db.session.add(nueva_ubicacion)
    db.session.commit()

    return jsonify({"mensaje": "Ubicación guardada con éxito"})

# Ruta para mostrar las ubicaciones (solo para operadores)
@app.route('/consulta', methods=['GET'])
def consulta():
    if 'usuario' not in session or session['tipo'] != 'operador':
        return redirect(url_for('login'))

    ubicaciones = Ubicacion.query.all()
    return render_template('consulta.html', ubicaciones=ubicaciones)

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    session.pop('tipo', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

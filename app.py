from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta'

# Configuración de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ubicaciones.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo para almacenar ubicaciones
class Ubicacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitud = db.Column(db.Float, nullable=False)
    longitud = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.String(100), nullable=False)

# Crear las tablas en la base de datos si no existen
with app.app_context():
    db.create_all()

# Ruta de inicio
@app.route('/')
def index():
    if 'usuario' in session:
        return redirect(url_for('enviar'))
    return redirect(url_for('login'))

# Ruta de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']

        if usuario == 'admin' and password == '1234':
            session['usuario'] = usuario
            return redirect(url_for('enviar'))
        return "Credenciales incorrectas", 401

    return render_template('login.html')

# Ruta para enviar ubicación
@app.route('/enviar', methods=['GET'])
def enviar():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('enviar_ubicacion.html')

# Ruta para recibir la ubicación enviada (POST)
@app.route('/enviar_ubicacion', methods=['POST'])
def enviar_ubicacion():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    data = request.get_json()
    latitud = data.get('latitud')
    longitud = data.get('longitud')

    nueva_ubicacion = Ubicacion(
        latitud=latitud,
        longitud=longitud,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    db.session.add(nueva_ubicacion)
    db.session.commit()

    return jsonify({"mensaje": "Ubicación guardada con éxito"})

# Ruta para mostrar las ubicaciones
@app.route('/consulta', methods=['GET'])
def consulta():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    ubicaciones = Ubicacion.query.all()
    return render_template('consulta.html', ubicaciones=ubicaciones)

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

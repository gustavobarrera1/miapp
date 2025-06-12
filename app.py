# app.py
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Inicializar la aplicación Flask
app = Flask(__name__)

# Configurar la base de datos
# Usando SQLite, el archivo de la base de datos estará en la carpeta 'instance',
# la cual se monta como un volumen de Docker para persistencia.
# Para producción, considera usar PostgreSQL o MySQL con un servicio separado.
database_path = os.path.join(os.getcwd(), 'instance', 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la extensión de base de datos SQLAlchemy
db = SQLAlchemy(app)

# Definir el modelo de la base de datos para un usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        # Este método define cómo se representa un objeto de la clase User
        return f'<User {self.id}: {self.name} ({self.email})>'

# Crear las tablas de la base de datos si no existen
# Esto se ejecutará cuando la aplicación se inicie
with app.app_context():
    db.create_all()

# Ruta para la página de inicio, muestra todos los usuarios
@app.route('/', methods=['GET'])
def index():
    # Consultar todos los usuarios de la base de datos
    users = User.query.all()
    # Renderizar la plantilla index.html, pasando los usuarios
    return render_template('index.html', users=users)

# Ruta para añadir un nuevo usuario
@app.route('/add_user', methods=['POST'])
def add_user():
    # Obtener el nombre y el email del formulario
    user_name = request.form['name']
    user_email = request.form['email']

    # Verificar si se proporcionan el nombre y el email
    if not user_name or not user_email:
        # Si falta información, redirigir a la página principal
        return redirect(url_for('index'))

    # Crear un nuevo objeto User
    new_user = User(name=user_name, email=user_email)
    try:
        # Añadir el nuevo usuario a la sesión de la base de datos
        db.session.add(new_user)
        # Confirmar la sesión para guardar el usuario en la base de datos
        db.session.commit()
        # Redirigir a la página principal para mostrar la lista actualizada
        return redirect(url_for('index'))
    except Exception as e:
        # Imprimir cualquier error que ocurra durante las operaciones de la base de datos
        print(f"Error al añadir usuario: {e}")
        # Opcionalmente, mostrar un mensaje de error al usuario
        # Por simplicidad, solo redirigimos
        return redirect(url_for('index'))

# Ruta para eliminar un usuario por su ID
@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    # Consultar el usuario a eliminar por su ID, o devolver 404 si no se encuentra
    user_to_delete = User.query.get_or_404(id)
    try:
        # Eliminar el usuario de la sesión de la base de datos
        db.session.delete(user_to_delete)
        # Confirmar la sesión para eliminar el usuario de la base de datos
        db.session.commit()
        # Redirigir a la página principal
        return redirect(url_for('index'))
    except Exception as e:
        # Imprimir cualquier error que ocurra
        print(f"Error al eliminar usuario: {e}")
        return redirect(url_for('index'))

# Punto de entrada para ejecutar la aplicación Flask
if __name__ == '__main__':
    # Ejecutar la aplicación en modo depuración (útil para desarrollo)
    app.run(debug=True, host='0.0.0.0', port=5000)

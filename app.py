import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

database_path = os.path.join(os.getcwd(), 'instance', 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.id}: {self.name} ({self.email})>'

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/add_user', methods=['POST'])
def add_user():
    user_name = request.form['name']
    user_email = request.form['email']

    if not user_name or not user_email:
        return redirect(url_for('index'))

    new_user = User(name=user_name, email=user_email)
    try:
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error al añadir usuario: {e}")
        return redirect(url_for('index'))

@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    user_to_delete = User.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error al eliminar usuario: {e}")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

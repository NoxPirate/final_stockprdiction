from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Create the database
with app.app_context():
    db.create_all()

# Home Route
@app.route('/')
def home():
    return render_template('core/home.html', user=session.get('user'))

# Login Route
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user'] = user.username  # Store user in session
            return redirect(url_for('dashboard'))
    return render_template('./registration/login.html')

# Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        email = request.form['email']
        new_user = User(username=username, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registration/register.html')

# Dashboard Route
@app.route('/dashboard')
def dashboard():
    return render_template('core/dashboard.html', user=session.get('user'))

# Logout Route
@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove user from session
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

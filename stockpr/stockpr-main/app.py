import os
from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()  # load .env if present

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key')
# Prefer SQLite for this project. Ignore non-sqlite DATABASE_URL values.
env_db = os.environ.get('DATABASE_URL')
# Build an absolute path to instance/users.db so DB works regardless of current working directory
project_dir = os.path.abspath(os.path.dirname(__file__))
instance_db_file = os.path.join(project_dir, 'instance', 'users.db')
os.makedirs(os.path.dirname(instance_db_file), exist_ok=True)
abs_db_uri = 'sqlite:///' + instance_db_file.replace('\\', '/')
if env_db and env_db.startswith('sqlite'):
    db_path = env_db
else:
    if env_db and not env_db.startswith('sqlite'):
        print('WARNING: DATABASE_URL set to non-sqlite; forcing SQLite for local dev')
    db_path = abs_db_uri
app.config['SQLALCHEMY_DATABASE_URI'] = db_path
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    # password hashes can be long; use Text to avoid truncation errors
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)

# Create the database
with app.app_context():
    db.create_all()
    # Debug/info: print configured DB URI and dialect
    try:
        print('Configured DB URI:', app.config.get('SQLALCHEMY_DATABASE_URI'))
        engine = db.engine
        print('DB dialect:', getattr(engine.dialect, 'name', None))
        # Run a simple schema adjustment for Postgres to ensure password column can hold long hashes
        if engine.dialect.name == 'postgresql':
            with engine.connect() as conn:
                try:
                    # Use USING to be explicit about casting if needed
                    conn.execute(text('ALTER TABLE "user" ALTER COLUMN password TYPE text USING password::text;'))
                    print('Migration: password column altered to text')
                except Exception as e:
                    print('DB migration warning:', e)
    except Exception as e:
        print('DB startup warning:', e)

# Home Route
@app.route('/')
def home():
    return render_template('core/home.html', user=session.get('user'))

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user'] = user.username  # Store user in session
            return redirect(url_for('dashboard'))
    return render_template('registration/login.html')

# Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        email = request.form['email']
        # basic uniqueness checks
        if User.query.filter_by(username=username).first():
            return render_template('registration/register.html', error='Username already exists')
        if User.query.filter_by(email=email).first():
            return render_template('registration/register.html', error='Email already registered')
        new_user = User(username=username, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registration/register.html')


@app.route('/db_status')
def db_status():
    try:
        user_count = User.query.count()
        return {'status': 'ok', 'user_count': user_count}
    except Exception as e:
        return {'status': 'error', 'error': str(e)}

# Dashboard Route
@app.route('/dashboard')
def dashboard():
    return render_template('core/dashboard.html', user=session.get('user'))

# Logout Route
@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove user from session
    return redirect(url_for('home'))

# Additional pages (render templates in templates/core)
@app.route('/cryptocurrency')
def cryptocurrency():
    return render_template('core/cryptocurrency.html', user=session.get('user'))


@app.route('/academy')
def academy():
    return render_template('core/academy.html', user=session.get('user'))


@app.route('/calculator')
def calculator():
    return render_template('core/calculator.html', user=session.get('user'))


@app.route('/faq')
def faq():
    return render_template('core/faq.html', user=session.get('user'))

if __name__ == '__main__':
    app.run(debug=True)

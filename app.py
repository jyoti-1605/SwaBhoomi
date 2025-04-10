from flask import Flask, render_template, redirect, url_for, session, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, ValidationError
import bcrypt
import MySQLdb
import MySQLdb.cursors

app = Flask(__name__)

# Configure MySQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'admin',
    'db': 'swabhoomi',
    'cursorclass': MySQLdb.cursors.DictCursor
}

app.secret_key = 'your_secret_key_here'

def get_db():
    """Get database connection"""
    try:
        connection = MySQLdb.connect(**DB_CONFIG)
        return connection
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# Initialize database
def init_db():
    try:
        # First connect without database
        conn = MySQLdb.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS swabhoomi")
        cursor.execute("USE swabhoomi")
        
        # Create tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS addresses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                address_type VARCHAR(50) NOT NULL,
                street_address TEXT NOT NULL,
                city VARCHAR(100) NOT NULL,
                state VARCHAR(100) NOT NULL,
                postal_code VARCHAR(20) NOT NULL,
                country VARCHAR(100) NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized successfully!")
        return True
    except Exception as e:
        print(f"Database initialization error: {e}")
        return False

# Initialize database on startup
init_db()

class RegisterForm(FlaskForm):
    name=StringField("Name", validators=[DataRequired()])
    email=StringField("Email", validators=[DataRequired(), Email()])
    password=PasswordField("Password", validators=[DataRequired()])
    address=TextAreaField("Address", validators=[DataRequired()])
    city=StringField("City", validators=[DataRequired()])
    state=StringField("State", validators=[DataRequired()])
    postal_code=StringField("Postal Code", validators=[DataRequired()])
    country=StringField("Country", validators=[DataRequired()])
    submit=SubmitField("Register")

    def validate_email(self, field):
        try:
            conn = get_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE email=%s", (field.data,))
                user = cursor.fetchone()
                cursor.close()
                conn.close()
                if user:
                    raise ValidationError('Email already registered. Please choose a different one.')
        except Exception as e:
            print(f"Database error in validate_email: {e}")
            raise ValidationError('Unable to validate email. Please try again.')

class LoginForm(FlaskForm):
    email=StringField("Email", validators=[DataRequired(), Email()])
    password=PasswordField("Password", validators=[DataRequired()])
    submit=SubmitField("Login")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            conn = get_db()
            if not conn:
                flash('Database connection error. Please try again later.', 'error')
                return render_template('register.html', form=form)

            cursor = conn.cursor()

            name = form.name.data
            email = form.email.data
            password = form.password.data
            address = form.address.data
            city = form.city.data
            state = form.state.data
            postal_code = form.postal_code.data
            country = form.country.data

            # Check if email already exists
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            existing_user = cursor.fetchone()
            if existing_user:
                cursor.close()
                conn.close()
                flash('Email already registered. Please choose a different one.', 'error')
                return render_template('register.html', form=form)

            # Hash password
            hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Store user data
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", 
                         (name, email, hash_password))
            conn.commit()
            user_id = cursor.lastrowid

            # Store address data
            cursor.execute("""
                INSERT INTO addresses (user_id, address_type, street_address, city, state, postal_code, country) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (user_id, 'PRIMARY', address, city, state, postal_code, country))
            conn.commit()
            
            cursor.close()
            conn.close()
            flash('Registration successful! Please login.', 'success')
            return redirect('/login')

        except Exception as e:
            print(f"Registration error: {e}")
            flash('An error occurred during registration. Please try again.', 'error')
            return render_template('register.html', form=form)
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            email = form.email.data
            password = form.password.data

            conn = get_db()
            if not conn:
                flash('Database connection error. Please try again later.', 'error')
                return render_template('login.html', form=form)

            cursor = conn.cursor()
            
            # Query for user
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                stored_password = user['password']
                if isinstance(stored_password, str):
                    stored_password = stored_password.encode('utf-8')
                
                if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                    session['user_id'] = user['id']
                    session['user_name'] = user['name']
                    flash('Login successful!', 'success')
                    return redirect('/dashboard')
            
            flash('Invalid email or password', 'error')
            return render_template('login.html', form=form)

        except Exception as e:
            print(f"Login error: {e}")
            flash('An error occurred during login. Please try again.', 'error')
            return render_template('login.html', form=form)
    
    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login first.')
        return redirect('/login')

    try:
        conn = get_db()
        if not conn:
            flash('Database connection error. Please try again later.')
            return redirect('/login')

        user_id = session.get('user_id')
        
        # Get user data
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        user = cursor.fetchone()
        
        # Get user addresses
        cursor.execute("SELECT * FROM addresses WHERE user_id=%s", (user_id,))
        addresses = cursor.fetchall()
        cursor.close()
        conn.close()

        if user:   
            return render_template('dashboard.html', user=user, addresses=addresses)
        
        session.pop('user_id', None)
        flash('User not found. Please login again.')
        return redirect('/login')
    except Exception as e:
        print(f"Dashboard error: {e}")
        flash('An error occurred. Please try again.')
        return redirect('/login')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('Please login first.')
        return redirect('/login')

    try:
        conn = get_db()
        if not conn:
            flash('Database connection error. Please try again later.')
            return redirect('/login')

        user_id = session.get('user_id')
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.*, a.* 
            FROM users u 
            LEFT JOIN addresses a ON u.id = a.user_id 
            WHERE u.id=%s
        """, (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()

        if user_data:
            return render_template('profile.html', user_data=user_data)
        
        session.pop('user_id', None)
        flash('User not found. Please login again.')
        return redirect('/login')
    except Exception as e:
        print(f"Profile error: {e}")
        flash('An error occurred. Please try again.')
        return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out')
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from dotenv import load_dotenv
import os

load_dotenv()  # loads variables from .env into environment

SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database Setup
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

# Routes
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid Credentials')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            flash('Registration Successful! Please log in.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists.')
        finally:
            conn.close()

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/projectile', methods=['GET', 'POST'])
def projectile():
    result = None
    if request.method == 'POST':
        try:
            u = float(request.form['velocity'])
            angle = float(request.form['angle'])
            import math
            R = (u**2 * math.sin(math.radians(2*angle))) / 9.8
            H = (u**2 * (math.sin(math.radians(angle))**2)) / (2*9.8)
            T = (2*u*math.sin(math.radians(angle))) / 9.8
            result = {'range': R, 'height': H, 'time': T}
        except:
            result = {'error': 'Invalid input'}
    return render_template('projectile.html', result=result)

@app.route('/time_conversion')
def time_conversion():
    return render_template('time_conversion.html')

@app.route('/speed_conversion')
def speed_conversion():
    return render_template('speed_conversion.html')

@app.route('/kinetic_energy', methods=['GET', 'POST'])
def kinetic_energy():
    result = None
    if request.method == 'POST':
        try:
            mass = float(request.form['mass'])
            velocity = float(request.form['velocity'])
            ke = 0.5 * mass * velocity ** 2
            result = {'ke': ke}
        except:
            result = {'error': 'Invalid input'}
    return render_template('kinetic_energy.html', result=result)

@app.route('/litre_conversion')
def litre_conversion():
    return render_template('litre_conversion.html')

@app.route('/specific_heat_capacity', methods=['GET', 'POST'])
def specific_heat_capacity():
    result = None
    if request.method == 'POST':
        try:
            m = float(request.form['mass'])
            c = float(request.form['specific_heat'])
            dT = float(request.form['change_temp'])
            q = m * c * dT
            result = {'heat': q}
        except:
            result = {'error': 'Invalid input'}
    return render_template('specific_heat_capacity.html', result=result)

@app.route('/basic_physics_conversion')
def basic_physics_conversion():
    return render_template('basic_physics_conversion.html')

@app.route('/frequency_wavelength', methods=['GET', 'POST'])
def frequency_wavelength():
    result = None
    if request.method == 'POST':
        try:
            speed = float(request.form['speed'])
            frequency = float(request.form['frequency'])
            wavelength = speed / frequency
            result = {'wavelength': wavelength}
        except:
            result = {'error': 'Invalid input'}
    return render_template('frequency_wavelength.html', result=result)

@app.route('/currency_conversion', methods=['GET', 'POST'])
def currency_conversion():
    result = None
    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
            from_currency = request.form['from_currency']
            to_currency = request.form['to_currency']
            url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
            response = requests.get(url)
            data = response.json()
            converted = amount * data['rates'][to_currency]
            result = {'converted': converted}
        except:
            result = {'error': 'Conversion failed'}
    return render_template('currency_conversion.html', result=result)

@app.route('/energy_conversion', methods=['GET', 'POST'])
def energy_conversion():
    result = None
    if request.method == 'POST':
        try:
            joules = float(request.form['joules'])
            ev = joules / 1.602e-19
            result = {'ev': ev}
        except:
            result = {'error': 'Invalid input'}
    return render_template('energy_conversion.html', result=result)

@app.route('/temperature_conversion')
def temperature_conversion():
    return render_template('temperature_conversion.html')

@app.route('/ohms_law', methods=['GET', 'POST'])
def ohms_law():
    result = None
    if request.method == 'POST':
        try:
            voltage = float(request.form['voltage'])
            current = float(request.form['current'])
            resistance = voltage / current
            result = {'resistance': resistance}
        except:
            result = {'error': 'Invalid input'}
    return render_template('ohms_law.html', result=result)

@app.route('/volume_conversion')
def volume_conversion():
    return render_template('volume_conversion.html')

if __name__ == '__main__':
    app.run(debug=True)

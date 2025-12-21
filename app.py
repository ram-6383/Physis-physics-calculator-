from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from dotenv import load_dotenv
import os
import math

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
@app.route('/shm', methods=['GET', 'POST'])
def shm():
    result = None

    if request.method == 'POST':
        try:
            # Input values
            mass = float(request.form['mass'])
            k = float(request.form['k'])
            A = float(request.form['amplitude'])

            if mass <= 0 or k <= 0 or A <= 0:
                raise ValueError("Values must be positive")

            import math

            # SHM calculations
            omega = math.sqrt(k / mass)          # Angular frequency
            T = 2 * math.pi / omega              # Time period
            f = 1 / T                            # Frequency
            vmax = A * omega                     # Maximum velocity

            # Send everything to HTML
            result = {
                'mass': mass,
                'k': k,
                'amplitude': A,
                'omega': round(omega, 4),
                'time_period': round(T, 4),
                'frequency': round(f, 4),
                'vmax': round(vmax, 4)
            }

        except:
            result = {'error': 'Invalid input. Please enter valid positive numbers.'}

    return render_template('shm.html', result=result)

@app.route('/doppler', methods=['GET', 'POST'])
def doppler():
    result = None
    if request.method == 'POST':
        try:
            f = float(request.form['source_freq'])        # Source frequency
            vo = float(request.form['observer_velocity']) # Observer velocity
            vs = float(request.form['source_velocity'])   # Source velocity
            direction = request.form['direction']

            v = 343  # Speed of sound in air (m/s)

            # Doppler Effect formula
            if direction == 'approaching':
                f_observed = f * ((v + vo) / (v - vs))
            else:
                f_observed = f * ((v - vo) / (v + vs))

            # Send ALL required values to template
            result = {
                'observed_freq': round(f_observed, 2),
                'source_freq': round(f, 2),
                'observer_velocity': round(vo, 2),
                'source_velocity': round(vs, 2)
            }

        except Exception as e:
            result = {'error': 'Invalid input values'}

    return render_template('doppler.html', result=result)

@app.route('/heat_transfer', methods=['GET', 'POST'])
def heat_transfer():
    result = None
    if request.method == 'POST':
        try:
            m = float(request.form['mass'])
            c = float(request.form['specific_heat'])
            t1 = float(request.form['initial_temp'])
            t2 = float(request.form['final_temp'])

            deltaT = t2 - t1
            q = m * c * deltaT

            # Time simulation (5 steps)
            time = list(range(0, 6))  # 0 to 5 seconds
            temp = [t1 + (deltaT / 5) * i for i in time]

            result = {
                'heat': q,
                'time': time,
                'temp': temp,
                'initial_temp': t1,
                'final_temp': t2
            }
        except:
            result = {'error': 'Invalid input.'}
    return render_template('heat_transfer.html', result=result)
@app.route('/circular_motion', methods=['GET', 'POST'])
def circular_motion():
    result = None
    if request.method == 'POST':
        try:
            r = float(request.form['radius'])
            omega = float(request.form['angular_velocity'])

            t = [i * 0.1 for i in range(100)]
            x = [r * math.cos(omega * ti) for ti in t]
            y = [r * math.sin(omega * ti) for ti in t]
            v = [r * omega for _ in t]
            a = [r * omega ** 2 for _ in t]

            result = {
                'x': x,
                'y': y,
                'v': v[0],
                'a': a[0],
                'radius': r,
                'omega': omega
            }
        except:
            result = {'error': 'Invalid input.'}
    return render_template('circular_motion.html', result=result)

@app.route('/physics-constants')
def physics_constants():
    return render_template('physics_constants.html')

@app.route('/thermodynamics')
def thermo_dashboard():
    return render_template('thermo/thermo_dashboard.html')

@app.route('/thermodynamics/first-law', methods=['GET', 'POST'])
def first_law():
    result = None
    if request.method == 'POST':
        try:
            Q = float(request.form['heat'])
            W = float(request.form['work'])
            deltaU = Q - W
            result = {
                'Q': Q,
                'W': W,
                'deltaU': round(deltaU, 2)
            }
        except:
            result = {'error': 'Invalid input'}
    return render_template('thermo/first_law.html', result=result)

@app.route('/thermodynamics/ideal-gas', methods=['GET', 'POST'])
def ideal_gas():
    result = None
    if request.method == 'POST':
        try:
            n = float(request.form['moles'])
            T = float(request.form['temperature'])
            V = float(request.form['volume'])

            R = 8.314  # J/mol·K
            P = (n * R * T) / V

            result = {
                'n': n,
                'T': T,
                'V': V,
                'P': round(P, 2)
            }
        except:
            result = {'error': 'Invalid input'}
    return render_template('thermo/ideal_gas.html', result=result)
@app.route('/thermodynamics/work-done', methods=['GET', 'POST'])
def work_done():
    result = None
    if request.method == 'POST':
        try:
            P = float(request.form['pressure'])
            V1 = float(request.form['v1'])
            V2 = float(request.form['v2'])

            deltaV = V2 - V1
            W = P * deltaV

            result = {
                'P': P,
                'V1': V1,
                'V2': V2,
                'deltaV': round(deltaV, 4),
                'W': round(W, 2)
            }
        except:
            result = {'error': 'Invalid input'}
    return render_template('thermo/work_done.html', result=result)
@app.route('/thermodynamics/cp-cv', methods=['GET', 'POST'])
def cp_cv():
    result = None
    if request.method == 'POST':
        try:
            R = float(request.form['R'])
            gamma = float(request.form['gamma'])

            Cv = R / (gamma - 1)
            Cp = gamma * Cv

            result = {
                'R': round(R, 4),
                'gamma': round(gamma, 4),
                'Cv': round(Cv, 4),
                'Cp': round(Cp, 4)
            }
        except:
            result = {'error': 'Invalid input'}
    return render_template('thermo/cp_cv.html', result=result)
@app.route('/thermodynamics/heat-engine', methods=['GET', 'POST'])
def heat_engine():
    result = None
    if request.method == 'POST':
        try:
            Q1 = float(request.form['Q1'])
            Q2 = float(request.form['Q2'])

            if Q2 >= Q1:
                raise ValueError

            work = Q1 - Q2
            efficiency = (work / Q1) * 100

            result = {
                'Q1': round(Q1, 3),
                'Q2': round(Q2, 3),
                'work': round(work, 3),
                'efficiency': round(efficiency, 2)
            }
        except:
            result = {'error': 'Invalid input or Q₂ must be less than Q₁'}
    return render_template('thermo/heat_engine.html', result=result)
@app.route('/thermodynamics/carnot-engine', methods=['GET', 'POST'])
def carnot_engine():
    result = None
    if request.method == 'POST':
        try:
            Th = float(request.form['Th'])
            Tc = float(request.form['Tc'])

            if Th <= 0 or Tc <= 0 or Tc >= Th:
                raise ValueError

            efficiency = (1 - (Tc / Th)) * 100

            result = {
                'Th': round(Th, 2),
                'Tc': round(Tc, 2),
                'efficiency': round(efficiency, 2)
            }
        except:
            result = {'error': 'Invalid input (Ensure Th > Tc and both in Kelvin)'}
    return render_template('thermo/carnot_engine.html', result=result)
@app.route('/thermodynamics/entropy', methods=['GET', 'POST'])
def entropy():
    result = None
    if request.method == 'POST':
        try:
            Q = float(request.form['heat'])
            T = float(request.form['temperature'])

            if T <= 0:
                raise ValueError

            entropy = Q / T

            result = {
                'heat': round(Q, 2),
                'temperature': round(T, 2),
                'entropy': round(entropy, 4)
            }
        except:
            result = {'error': 'Invalid input (Temperature must be > 0 Kelvin)'}
    return render_template('thermo/entropy.html', result=result)

@app.route('/thermodynamics/refrigerator', methods=['GET', 'POST'])
def refrigerator():
    result = None
    if request.method == 'POST':
        try:
            qc = float(request.form['qc'])
            work = float(request.form['work'])

            if work <= 0:
                raise ValueError

            cop = qc / work

            result = {
                'qc': round(qc, 2),
                'work': round(work, 2),
                'cop': round(cop, 4)
            }
        except:
            result = {'error': 'Invalid input (Work must be > 0)'}
    return render_template('thermo/refrigerator.html', result=result)
import numpy as np
import math

@app.route('/thermo/process', methods=['GET', 'POST'])
def thermo_process():
    result = None

    if request.method == 'POST':
        try:
            process = request.form['process']
            P1 = float(request.form.get('P1', 0) or 0)
            V1 = float(request.form.get('V1', 0) or 0)
            V2 = float(request.form.get('V2', 0) or 0)
            gamma = float(request.form.get('gamma', 1.4) or 1.4)
            P_const = float(request.form.get('P', 0) or 0)

            steps = []
            V_plot = []
            P_plot = []
            W = None
            P2 = None

            # ---------------- ISOTHERMAL ----------------
            if process == 'isothermal':
                C = P1 * V1
                V_plot = np.linspace(V1, V2, 50).tolist()
                P_plot = [(C / v) for v in V_plot]
                W = round(C * math.log(V2 / V1), 3)

                steps = [
                    f"P₁V₁ = constant = {C}",
                    "Isothermal work formula: W = P₁V₁ ln(V₂/V₁)",
                    f"W = {W} J"
                ]

            # ---------------- ADIABATIC ----------------
            elif process == 'adiabatic':
                C = P1 * (V1 ** gamma)
                V_plot = np.linspace(V1, V2, 50).tolist()
                P_plot = [(C / (v ** gamma)) for v in V_plot]
                P2 = round(C / (V2 ** gamma), 3)
                W = round((P1 * V1 - P2 * V2) / (gamma - 1), 3)

                steps = [
                    "Adiabatic relation: PV^γ = constant",
                    f"Final pressure P₂ = {P2} Pa",
                    f"Work done W = {W} J"
                ]

            # ---------------- ISOBARIC ----------------
            elif process == 'isobaric':
                P_plot = [P_const, P_const]
                V_plot = [V1, V2]
                W = round(P_const * (V2 - V1), 3)

                steps = [
                    "Pressure is constant",
                    f"W = P(V₂ − V₁)",
                    f"W = {W} J"
                ]

            # ---------------- ISOCHORIC ----------------
            elif process == 'isochoric':
                V_plot = [V1, V1]
                P_plot = [P1, P1 * 1.5]
                W = 0

                steps = [
                    "Volume is constant",
                    "No work done",
                    "W = 0 J"
                ]

            result = {
                "steps": steps,
                "W": W,
                "P2": P2,
                "V_plot": V_plot,
                "P_plot": P_plot
            }

        except Exception as e:
            result = {"error": str(e)}

    return render_template('thermo/process.html', result=result)

@app.route('/thermodynamics/zeroth-law', methods=['GET', 'POST'])
def zeroth_law():
    result = None

    if request.method == 'POST':
        try:
            T1 = float(request.form['T1'])
            T2 = float(request.form['T2'])

            equilibrium = "YES" if T1 == T2 else "NO"

            result = {
                'T1': T1,
                'T2': T2,
                'equilibrium': equilibrium
            }

        except:
            result = {'error': 'Invalid temperature values'}

    return render_template('thermo/zeroth_law.html', result=result)
@app.route('/thermodynamics/internal-energy', methods=['GET', 'POST'])
def internal_energy():
    result = None

    if request.method == 'POST':
        try:
            f = float(request.form['f'])   # degrees of freedom
            n = float(request.form['n'])   # moles
            T = float(request.form['T'])   # temperature (K)

            R = 8.314  # J/mol·K
            U = (f / 2) * n * R * T

            result = {
                'f': f,
                'n': n,
                'T': T,
                'U': round(U, 3)
            }

        except:
            result = {'error': 'Invalid input values'}

    return render_template('thermo/internal_energy.html', result=result)
@app.route('/thermodynamics/gibbs-free-energy', methods=['GET', 'POST'])
def gibbs_free_energy():
    result = None

    if request.method == 'POST':
        try:
            # Read inputs from form
            H = float(request.form['H'])   # ΔH (J)
            T = float(request.form['T'])   # Temperature (K)
            S = float(request.form['S'])   # ΔS (J/K)

            # Gibbs Free Energy calculation
            G = H - (T * S)

            result = {
                'H': H,
                'T': T,
                'S': S,
                'G': round(G, 3)
            }

        except:
            result = {'error': 'Invalid input values'}

    return render_template('thermo/gibbs_free_energy.html', result=result)
@app.route('/thermodynamics/enthalpy', methods=['GET', 'POST'])
def enthalpy():
    result = None

    if request.method == 'POST':
        try:
            # Read inputs
            m = float(request.form['mass'])          # mass (kg)
            cp = float(request.form['cp'])           # specific heat capacity (J/kg·K)
            dT = float(request.form['deltaT'])       # temperature change (K)

            # Enthalpy change calculation
            deltaH = m * cp * dT

            result = {
                'mass': m,
                'cp': cp,
                'deltaT': dT,
                'deltaH': round(deltaH, 3)
            }

        except:
            result = {'error': 'Invalid input values'}

    return render_template('thermo/enthalpy_change.html', result=result)
@app.route('/thermodynamics/hess', methods=['GET', 'POST'])
def hess():
    result = None

    if request.method == 'POST':
        try:
            # Input enthalpy changes of individual steps
            H1 = float(request.form['H1'])
            H2 = float(request.form['H2'])
            H3 = float(request.form.get('H3', 0))  # optional third step

            # Hess's Law: total enthalpy change
            deltaH = H1 + H2 + H3

            result = {
                'H1': H1,
                'H2': H2,
                'H3': H3,
                'deltaH': round(deltaH, 3)
            }

        except:
            result = {'error': 'Invalid input values'}

    return render_template('thermo/hess_law.html', result=result)
@app.route('/thermodynamics/helmholtz', methods=['GET', 'POST'])
def helmholtz():
    result = None

    if request.method == 'POST':
        try:
            # Input values
            U = float(request.form['U'])   # Internal Energy (J)
            T = float(request.form['T'])   # Temperature (K)
            S = float(request.form['S'])   # Entropy (J/K)

            # Helmholtz free energy formula
            A = U - (T * S)

            result = {
                'U': U,
                'T': T,
                'S': S,
                'A': round(A, 3)
            }

        except:
            result = {'error': 'Invalid input values'}

    return render_template('thermo/helmholtz_free_energy.html', result=result)
@app.route('/thermodynamics/phase', methods=['GET', 'POST'])
def phase():
    result = None

    if request.method == 'POST':
        try:
            # Inputs
            m = float(request.form['mass'])          # mass (kg)
            L = float(request.form['latent_heat'])  # latent heat (J/kg)
            T1 = float(request.form['T1'])           # initial temperature (K)
            T2 = float(request.form['T2'])           # final temperature (K)
            H_vap = float(request.form['H_vap'])     # enthalpy of vaporization (J/mol)

            R = 8.314  # J/mol·K

            # Latent heat calculation
            Q = m * L

            # Clausius–Clapeyron (integrated form)
            lnP_ratio = (H_vap / R) * ((1 / T1) - (1 / T2))

            result = {
                'mass': m,
                'latent_heat': L,
                'Q': round(Q, 3),
                'T1': T1,
                'T2': T2,
                'H_vap': H_vap,
                'lnP_ratio': round(lnP_ratio, 5)
            }

        except:
            result = {'error': 'Invalid input values'}

    return render_template('thermo/phase_transition.html', result=result)
@app.route('/thermodynamics/maxwell', methods=['GET', 'POST'])
def maxwell():
    result = None

    relations = {
        "1": {
            "equation": "(∂T/∂V)ₛ = −(∂P/∂S)ᵥ",
            "explanation": [
                "This Maxwell relation is derived from internal energy U(S, V).",
                "It relates temperature change with volume at constant entropy.",
                "It also connects pressure change with entropy at constant volume."
            ]
        },
        "2": {
            "equation": "(∂T/∂P)ₛ = (∂V/∂S)ₚ",
            "explanation": [
                "This relation comes from enthalpy H(S, P).",
                "It links temperature change with pressure at constant entropy.",
                "It also relates volume change with entropy at constant pressure."
            ]
        },
        "3": {
            "equation": "(∂S/∂V)ₜ = (∂P/∂T)ᵥ",
            "explanation": [
                "This relation is obtained from Helmholtz free energy A(T, V).",
                "It connects entropy variation with volume at constant temperature.",
                "It is widely used in entropy calculations."
            ]
        },
        "4": {
            "equation": "(∂S/∂P)ₜ = −(∂V/∂T)ₚ",
            "explanation": [
                "This relation comes from Gibbs free energy G(T, P).",
                "It relates entropy change with pressure at constant temperature.",
                "Useful for phase transition analysis."
            ]
        }
    }

    if request.method == 'POST':
        try:
            key = request.form['relation']
            result = relations[key]
        except:
            result = {'error': 'Invalid selection'}

    return render_template('thermo/maxwell_relation.html', result=result)

@app.route('/thermodynamics/real-gas', methods=['GET', 'POST'])
def real_gas():
    result = None

    if request.method == 'POST':
        try:
            # Inputs
            P = float(request.form['P'])   # Pressure (Pa)
            V = float(request.form['V'])   # Volume (m^3)
            n = float(request.form['n'])   # Number of moles
            a = float(request.form['a'])   # van der Waals constant a
            b = float(request.form['b'])   # van der Waals constant b

            R = 8.314  # Gas constant (J/mol·K)

            # Van der Waals equation solved for temperature
            T = ((P + (a * n * n) / (V * V)) * (V - n * b)) / (n * R)

            result = {
                'P': P,
                'V': V,
                'n': n,
                'a': a,
                'b': b,
                'T': round(T, 3)
            }

        except:
            result = {'error': 'Invalid input values'}

    return render_template('thermo/real_gas.html', result=result)
@app.route('/thermodynamics/statistical', methods=['GET', 'POST'])
def statistical():
    result = None

    if request.method == 'POST':
        try:
            # Inputs
            omega = float(request.form['omega'])   # number of microstates
            f = float(request.form['f'])           # degrees of freedom
            n = float(request.form['n'])           # moles
            T = float(request.form['T'])           # temperature (K)

            k = 1.38e-23    # Boltzmann constant (J/K)
            R = 8.314       # Gas constant (J/mol·K)

            # Calculations
            entropy = k * math.log(omega)
            internal_energy = (f / 2) * n * R * T

            result = {
                'omega': omega,
                'f': f,
                'n': n,
                'T': T,
                'entropy': round(entropy, 6),
                'internal_energy': round(internal_energy, 3)
            }

        except:
            result = {'error': 'Invalid input values'}

    return render_template(
        'thermo/statistical_mechanics.html',
        result=result
    )
@app.route('/thermodynamics/heat-transfer-advanced', methods=['GET', 'POST'])
def heat_transfer_adv():
    result = None

    if request.method == 'POST':
        try:
            # Inputs
            k = float(request.form['k'])          # thermal conductivity (W/m·K)
            A = float(request.form['A'])          # area (m^2)
            dT = float(request.form['dT'])        # temperature difference (K)
            dx = float(request.form['dx'])        # thickness (m)

            L0 = float(request.form['L0'])        # original length (m)
            alpha = float(request.form['alpha']) # coefficient of expansion (1/K)

            T = float(request.form['T'])          # temperature (K)

            # Constants
            b = 2.898e-3  # Wien's constant (m·K)

            # Calculations
            heat_rate = (k * A * dT) / dx                     # Fourier's Law
            expanded_length = L0 * (1 + alpha * dT)           # Linear expansion
            lambda_max = b / T                                 # Wien's law

            result = {
                'k': k,
                'A': A,
                'dT': dT,
                'dx': dx,
                'heat_rate': round(heat_rate, 3),
                'L0': L0,
                'alpha': alpha,
                'expanded_length': round(expanded_length, 6),
                'T': T,
                'lambda_max': round(lambda_max, 9)
            }

        except:
            result = {'error': 'Invalid input values'}

    return render_template(
        'thermo/heat_transfer_advanced.html',
        result=result
    )
@app.route('/thermodynamics/stability', methods=['GET', 'POST'])
def stability():
    result = None

    if request.method == 'POST':
        try:
            # Inputs
            T = float(request.form['T'])          # Temperature (K)
            dSdT = float(request.form['dSdT'])    # (∂S/∂T)V
            V = float(request.form['V'])          # Volume (m^3)
            dVdP = float(request.form['dVdP'])    # (∂V/∂P)T
            dmu = float(request.form['dmu'])      # (∂μi/∂ni)

            # Calculations
            Cv = T * dSdT
            kappa_T = -(1 / V) * dVdP

            thermal = "Stable" if Cv > 0 else "Unstable"
            mechanical = "Stable" if kappa_T > 0 else "Unstable"
            diffusional = "Stable" if dmu > 0 else "Unstable"

            result = {
                'T': T,
                'Cv': round(Cv, 4),
                'kappa_T': round(kappa_T, 6),
                'dmu': dmu,
                'thermal': thermal,
                'mechanical': mechanical,
                'diffusional': diffusional
            }

        except:
            result = {'error': 'Invalid input values'}

    return render_template(
        'thermo/thermodynamic_stability.html',
        result=result
    )
@app.route('/thermodynamics/advanced-cycles', methods=['GET', 'POST'])
def advanced_cycles():
    result = None

    if request.method == 'POST':
        try:
            cycle = request.form['cycle']
            gamma = float(request.form['gamma'])

            # ------------------------
            # Brayton Cycle
            # ------------------------
            if cycle == 'brayton':
                rp = float(request.form['rp'])
                eta = 1 - (rp ** ((1 - gamma) / gamma))

                result = {
                    'cycle': 'Brayton Cycle',
                    'eta': round(eta, 4)
                }

            # ------------------------
            # Rankine Cycle
            # ------------------------
            elif cycle == 'rankine':
                h1 = float(request.form['h1'])
                h2 = float(request.form['h2'])
                h3 = float(request.form['h3'])
                h4 = float(request.form['h4'])

                W_net = (h1 - h2) - (h4 - h3)

                result = {
                    'cycle': 'Rankine Cycle',
                    'W_net': round(W_net, 3)
                }

            # ------------------------
            # Otto / Diesel Cycle
            # ------------------------
            elif cycle == 'otto':
                r = float(request.form['r'])
                eta = 1 - (r ** (1 - gamma))

                result = {
                    'cycle': 'Otto / Diesel Cycle',
                    'eta': round(eta, 4)
                }

        except:
            result = {'error': 'Invalid input values'}

    return render_template(
        'thermo/advanced_thermodynamic_cycles.html',
        result=result
    )

@app.route('/thermodynamics/chemical-phase-equilibrium', methods=['GET', 'POST'])
def chem_phase_eq():
    result = None

    if request.method == 'POST':
        try:
            law = request.form['law']

            # ---------------------------------
            # Chemical Potential
            # ---------------------------------
            if law == 'chemical_potential':
                G = float(request.form['G'])
                n = float(request.form['n'])
                mu = G / n

                result = {
                    'law': 'Chemical Potential',
                    'mu': round(mu, 4)
                }

            # ---------------------------------
            # Gibbs Phase Rule
            # ---------------------------------
            elif law == 'gibbs_phase':
                C = int(request.form['C'])
                P = int(request.form['P'])
                F = C - P + 2

                result = {
                    'law': 'Gibbs Phase Rule',
                    'F': F
                }

            # ---------------------------------
            # Van der Waals Differential
            # ---------------------------------
            elif law == 'vdw':
                dv = float(request.form['dv'])
                ds = float(request.form['ds'])
                dP = float(request.form['dP'])
                dT = float(request.form['dT'])
                d2gdx2 = float(request.form['d2gdx2'])
                dx = float(request.form['dx'])

                lhs = dv * dP
                rhs = (ds * dT) + (d2gdx2 * dx)

                result = {
                    'law': 'Van der Waals Differential',
                    'lhs': round(lhs, 5),
                    'rhs': round(rhs, 5),
                    'equilibrium': "Satisfied" if abs(lhs - rhs) < 1e-3 else "Not satisfied"
                }

        except:
            result = {'error': 'Invalid input values'}

    return render_template(
        'thermo/chemical_phase_equilibrium.html',
        result=result
    )

@app.route('/thermodynamics/thermochemistry', methods=['GET', 'POST'])
def thermochemistry():
    result = None

    if request.method == 'POST':
        try:
            law = request.form['law']

            # -------------------------------
            # Kirchhoff’s Law
            # -------------------------------
            if law == 'kirchhoff':
                H1 = float(request.form['H1'])      # ΔH at T1
                Cp = float(request.form['Cp'])      # ΔCp (assumed constant)
                T1 = float(request.form['T1'])
                T2 = float(request.form['T2'])

                H2 = H1 + Cp * (T2 - T1)

                result = {
                    'law': 'Kirchhoff’s Law',
                    'H2': round(H2, 4),
                    'details': f"ΔH(T₂) = ΔH(T₁) + ΔCp(T₂ − T₁)"
                }

            # -------------------------------
            # Partial Molar Properties
            # -------------------------------
            elif law == 'partial_molar':
                n1 = float(request.form['n1'])
                n2 = float(request.form['n2'])
                V1 = float(request.form['V1'])
                V2 = float(request.form['V2'])

                V_total = (n1 * V1) + (n2 * V2)

                result = {
                    'law': 'Partial Molar Properties',
                    'V_total': round(V_total, 4),
                    'details': "V = Σ nᵢ V̄ᵢ"
                }

        except:
            result = {'error': 'Invalid input values'}

    return render_template(
        'thermo/thermochemistry_solution_laws.html',
        result=result
    )

@app.route('/thermodynamics/fugacity-activity', methods=['GET', 'POST'])
def fugacity_activity():
    result = None

    if request.method == 'POST':
        try:
            law = request.form['law']

            # ---------------------------------
            # Fugacity
            # ---------------------------------
            if law == 'fugacity':
                phi = float(request.form['phi'])
                P = float(request.form['P'])

                f = phi * P

                result = {
                    'law': 'Fugacity',
                    'phi': phi,
                    'P': P,
                    'f': round(f, 4)
                }

            # ---------------------------------
            # Fugacity Coefficient (Conceptual)
            # ---------------------------------
            elif law == 'fugacity_coeff':
                GR = float(request.form['GR'])   # Residual Gibbs free energy
                T = float(request.form['T'])

                R = 8.314
                ln_phi = GR / (R * T)
                phi = round(pow(2.71828, ln_phi), 5)

                result = {
                    'law': 'Fugacity Coefficient',
                    'ln_phi': round(ln_phi, 5),
                    'phi': phi
                }

            # ---------------------------------
            # Activity
            # ---------------------------------
            elif law == 'activity':
                gamma = float(request.form['gamma'])
                x = float(request.form['x'])

                a = gamma * x

                result = {
                    'law': 'Activity',
                    'gamma': gamma,
                    'x': x,
                    'a': round(a, 5)
                }

        except:
            result = {'error': 'Invalid input values'}

    return render_template(
        'thermo/fugacity_activity.html',
        result=result
    )
@app.route('/thermodynamics/legendre', methods=['GET', 'POST'])
def legendre():
    result = None

    if request.method == 'POST':
        try:
            transform = request.form['transform']

            # ---------------------------------
            # U → Helmholtz Free Energy
            # F = U − TS
            # ---------------------------------
            if transform == 'helmholtz':
                U = float(request.form['U'])
                T = float(request.form['T'])
                S = float(request.form['S'])

                F = U - T * S

                result = {
                    'transform': 'Internal Energy → Helmholtz Free Energy',
                    'formula': 'F = U − TS',
                    'value': round(F, 4)
                }

            # ---------------------------------
            # U → Enthalpy
            # H = U + PV
            # ---------------------------------
            elif transform == 'enthalpy':
                U = float(request.form['U'])
                P = float(request.form['P'])
                V = float(request.form['V'])

                H = U + P * V

                result = {
                    'transform': 'Internal Energy → Enthalpy',
                    'formula': 'H = U + PV',
                    'value': round(H, 4)
                }

            # ---------------------------------
            # U → Gibbs Free Energy
            # G = U − TS + PV
            # ---------------------------------
            elif transform == 'gibbs':
                U = float(request.form['U'])
                T = float(request.form['T'])
                S = float(request.form['S'])
                P = float(request.form['P'])
                V = float(request.form['V'])

                G = U - T * S + P * V

                result = {
                    'transform': 'Internal Energy → Gibbs Free Energy',
                    'formula': 'G = U − TS + PV',
                    'value': round(G, 4)
                }

        except:
            result = {'error': 'Invalid input values'}

    return render_template(
        'thermo/legendre_transformations.html',
        result=result
    )
@app.route('/thermodynamics/non-equilibrium', methods=['GET', 'POST'])
def non_equilibrium():
    result = None

    if request.method == 'POST':
        try:
            law = request.form['law']

            # ---------------------------------
            # Entropy Production Rate
            # σ = Σ Ji Xi
            # ---------------------------------
            if law == 'entropy_prod':
                J = float(request.form['J'])   # flux
                X = float(request.form['X'])   # thermodynamic force

                sigma = J * X

                result = {
                    'law': 'Entropy Production Rate',
                    'sigma': round(sigma, 6),
                    'validity': 'Irreversible (σ ≥ 0)' if sigma >= 0 else 'Violates Second Law'
                }

            # ---------------------------------
            # Onsager Reciprocal Relations
            # ---------------------------------
            elif law == 'onsager':
                L12 = float(request.form['L12'])
                L21 = float(request.form['L21'])

                result = {
                    'law': 'Onsager Reciprocal Relations',
                    'L12': L12,
                    'L21': L21,
                    'relation': 'Satisfied (L₁₂ = L₂₁)' if abs(L12 - L21) < 1e-3 else 'Not Satisfied'
                }

            # ---------------------------------
            # Thermal Diffusion (Coupled Transport)
            # ---------------------------------
            elif law == 'thermal_diffusion':
                kT = float(request.form['kT'])     # thermal diffusion coefficient
                gradT = float(request.form['gradT'])  # temperature gradient

                Jq = -kT * gradT

                result = {
                    'law': 'Thermal Diffusion',
                    'Jq': round(Jq, 6),
                    'meaning': 'Heat & mass transport are coupled'
                }

        except:
            result = {'error': 'Invalid input values'}

    return render_template(
        'thermo/non_equilibrium_transport.html',
        result=result
    )
@app.route('/thermodynamics/molecular-simulation', methods=['GET', 'POST'])
def molecular_simulation():
    result = None

    if request.method == 'POST':
        try:
            method = request.form['method']
            R = 8.314

            # ---------------------------------
            # Thermodynamic Integration
            # ΔF = ∫ ⟨∂U/∂λ⟩ dλ  (simplified numeric)
            # ---------------------------------
            if method == 'thermo_integration':
                avg_dU = float(request.form['avg_dU'])   # ⟨∂U/∂λ⟩
                delta_lambda = float(request.form['delta_lambda'])

                deltaF = avg_dU * delta_lambda

                result = {
                    'method': 'Thermodynamic Integration',
                    'deltaF': round(deltaF, 5),
                    'explain': 'Free energy difference obtained by integrating along a path'
                }

            # ---------------------------------
            # Widom Particle Insertion
            # μ = -RT ln⟨exp(-ΔU/RT)⟩
            # ---------------------------------
            elif method == 'widom':
                deltaU = float(request.form['deltaU'])
                T = float(request.form['T'])

                mu = -R * T * (deltaU / (R * T))

                result = {
                    'method': 'Widom Particle Insertion',
                    'mu': round(mu, 5),
                    'explain': 'Chemical potential estimated via particle insertion'
                }

            # ---------------------------------
            # Langevin Equation (1D steady state)
            # m dv/dt = -γv + ξ(t)
            # ---------------------------------
            elif method == 'langevin':
                gamma = float(request.form['gamma'])
                v = float(request.form['v'])

                friction = -gamma * v

                result = {
                    'method': 'Langevin Dynamics',
                    'force': round(friction, 5),
                    'explain': 'Motion under friction and thermal noise'
                }

        except:
            result = {'error': 'Invalid input values'}

    return render_template(
        'thermo/molecular_simulation_methods.html',
        result=result
    )
@app.route('/thermodynamics/exergy', methods=['GET', 'POST'])
def exergy():
    result = None

    if request.method == 'POST':
        try:
            # System state
            U1 = float(request.form['U1'])
            V1 = float(request.form['V1'])
            S1 = float(request.form['S1'])

            # Dead state (environment)
            U0 = float(request.form['U0'])
            V0 = float(request.form['V0'])
            S0 = float(request.form['S0'])

            P0 = float(request.form['P0'])
            T0 = float(request.form['T0'])

            # Exergy change calculation
            delta_psi = (U1 - U0) + P0 * (V1 - V0) - T0 * (S1 - S0)

            result = {
                'U1': U1, 'U0': U0,
                'V1': V1, 'V0': V0,
                'S1': S1, 'S0': S0,
                'P0': P0, 'T0': T0,
                'delta_psi': round(delta_psi, 4)
            }

        except:
            result = {'error': 'Invalid input values'}

    return render_template(
        'thermo/exergy_analysis.html',
        result=result
    )
@app.route('/thermodynamics/surface-interface', methods=['GET', 'POST'])
def surface_interface():
    result = None

    if request.method == 'POST':
        try:
            law = request.form['law']
            R = 8.314

            # ---------------------------------
            # Surface Tension
            # γ = ∂G / ∂A
            # ---------------------------------
            if law == 'surface_tension':
                dG = float(request.form['dG'])
                dA = float(request.form['dA'])

                gamma = dG / dA

                result = {
                    'law': 'Surface Tension',
                    'gamma': round(gamma, 6)
                }

            # ---------------------------------
            # Gibbs Adsorption Isotherm
            # dγ = − Γ dμ
            # ---------------------------------
            elif law == 'gibbs_adsorption':
                Gamma = float(request.form['Gamma'])
                dmu = float(request.form['dmu'])

                dgamma = -Gamma * dmu

                result = {
                    'law': 'Gibbs Adsorption Isotherm',
                    'dgamma': round(dgamma, 6)
                }

            # ---------------------------------
            # Laplace Equation
            # ΔP = γ (1/R1 + 1/R2)
            # ---------------------------------
            elif law == 'laplace':
                gamma = float(request.form['gamma'])
                R1 = float(request.form['R1'])
                R2 = float(request.form['R2'])

                deltaP = gamma * ((1 / R1) + (1 / R2))

                result = {
                    'law': 'Laplace Equation',
                    'deltaP': round(deltaP, 6)
                }

            # ---------------------------------
            # Kelvin Equation
            # ln(P/P0) = 2γVm / rRT
            # ---------------------------------
            elif law == 'kelvin':
                gamma = float(request.form['gamma'])
                Vm = float(request.form['Vm'])
                r = float(request.form['r'])
                T = float(request.form['T'])

                ln_ratio = (2 * gamma * Vm) / (r * R * T)

                result = {
                    'law': 'Kelvin Equation',
                    'ln_ratio': round(ln_ratio, 6)
                }

            # ---------------------------------
            # Young Equation
            # cosθ = (γsv − γsl) / γlv
            # ---------------------------------
            elif law == 'young':
                gamma_sv = float(request.form['gamma_sv'])
                gamma_sl = float(request.form['gamma_sl'])
                gamma_lv = float(request.form['gamma_lv'])

                cos_theta = (gamma_sv - gamma_sl) / gamma_lv

                result = {
                    'law': 'Young Equation',
                    'cos_theta': round(cos_theta, 6)
                }

        except:
            result = {'error': 'Invalid input values'}

    return render_template(
        'thermo/surface_interface_thermodynamics.html',
        result=result
    )
@app.route('/thermodynamics/advanced-efficiency', methods=['GET', 'POST'])
def advanced_efficiency():
    result = None

    if request.method == 'POST':
        try:
            calc = request.form['calc']
            gamma = float(request.form['gamma'])

            # -------------------------------
            # Diesel Cycle Efficiency
            # -------------------------------
            if calc == 'diesel':
                r = float(request.form['r'])         # compression ratio
                beta = float(request.form['beta'])   # cut-off ratio

                eta_diesel = 1 - (1/gamma) * ((beta**gamma - 1) / (r**(gamma - 1) * (beta - 1)))

                result = {
                    'calc': 'Diesel Cycle Efficiency',
                    'eta': round(eta_diesel, 5)
                }

            # -------------------------------
            # Refrigerator COP
            # -------------------------------
            elif calc == 'cop_r':
                QL = float(request.form['QL'])
                W = float(request.form['W'])

                COP_R = QL / W

                result = {
                    'calc': 'Refrigerator COP',
                    'cop': round(COP_R, 5)
                }

            # -------------------------------
            # Heat Pump COP
            # -------------------------------
            elif calc == 'cop_hp':
                QH = float(request.form['QH'])
                W = float(request.form['W'])

                COP_HP = QH / W

                result = {
                    'calc': 'Heat Pump COP',
                    'cop': round(COP_HP, 5)
                }

        except:
            result = {'error': 'Invalid input values'}

    return render_template(
        'thermo/advanced_efficiencies.html',
        result=result
    )
@app.route('/thermodynamics/non-ideal-mixture', methods=['GET', 'POST'])
def non_ideal_mixture():
    result = None

    if request.method == 'POST':
        try:
            law = request.form['law']

            # ---------------------------------
            # Residual Property
            # Gᴿ = G_real − G_ideal
            # ---------------------------------
            if law == 'residual':
                G_real = float(request.form['G_real'])
                G_ideal = float(request.form['G_ideal'])

                GR = G_real - G_ideal

                result = {
                    'law': 'Residual Property',
                    'GR': round(GR, 5)
                }

            # ---------------------------------
            # Activity Coefficient
            # aᵢ = γᵢ xᵢ
            # ---------------------------------
            elif law == 'activity_coeff':
                gamma = float(request.form['gamma'])
                x = float(request.form['x'])

                a = gamma * x

                result = {
                    'law': 'Activity Coefficient',
                    'a': round(a, 5)
                }

            # ---------------------------------
            # Poynting Correction (Simplified)
            # f = f⁰ exp[V(P−P⁰)/RT]
            # ---------------------------------
            elif law == 'poynting':
                V = float(request.form['V'])
                P = float(request.form['P'])
                P0 = float(request.form['P0'])
                T = float(request.form['T'])

                R = 8.314
                correction = (V * (P - P0)) / (R * T)

                result = {
                    'law': 'Poynting Correction',
                    'correction': round(correction, 6)
                }

            # ---------------------------------
            # Dalton’s Law
            # P_total = Σ Pi
            # ---------------------------------
            elif law == 'dalton':
                P1 = float(request.form['P1'])
                P2 = float(request.form['P2'])
                P3 = float(request.form['P3'])

                P_total = P1 + P2 + P3

                result = {
                    'law': 'Dalton’s Law',
                    'P_total': round(P_total, 5),
                    'partials': [P1, P2, P3]
                }

        except:
            result = {'error': 'Invalid input values'}

    return render_template(
        'thermo/non_ideal_mixture.html',
        result=result
    )
@app.route('/thermodynamics/relativistic-quantum', methods=['GET', 'POST'])
def relativistic_quantum():
    result = None

    if request.method == 'POST':
        try:
            law = request.form['law']

            # ---------------------------------
            # Relativistic First Law (Scalar Form)
            # dξ = dΘ − P dV
            # ---------------------------------
            if law == 'relativistic_first':
                dTheta = float(request.form['dTheta'])
                P = float(request.form['P'])
                dV = float(request.form['dV'])

                dXi = dTheta - P * dV

                result = {
                    'law': 'Relativistic First Law',
                    'dXi': round(dXi, 6)
                }

            # ---------------------------------
            # Black Hole Entropy (Bekenstein–Hawking)
            # S = kB A / (4 lP²)
            # ---------------------------------
            elif law == 'black_hole':
                A = float(request.form['A'])

                kB = 1.380649e-23      # Boltzmann constant
                lP = 1.616255e-35      # Planck length

                S = (kB * A) / (4 * lP**2)

                result = {
                    'law': 'Black Hole Entropy',
                    'S': S
                }

            # ---------------------------------
            # Quantum Master Equation (Relaxation)
            # dρ/dt = −γ(ρ − ρ_eq)
            # ---------------------------------
            elif law == 'quantum_master':
                gamma = float(request.form['gamma'])
                rho = float(request.form['rho'])
                rho_eq = float(request.form['rho_eq'])

                drho_dt = -gamma * (rho - rho_eq)

                result = {
                    'law': 'Quantum Master Equation',
                    'drho_dt': round(drho_dt, 6)
                }

        except:
            result = {'error': 'Invalid input values'}

    return render_template(
        'thermo/relativistic_quantum_thermodynamics.html',
        result=result
    )
@app.route('/thermodynamics/information-thermodynamics', methods=['GET', 'POST'])
def info_thermo():
    result = None

    if request.method == 'POST':
        try:
            law = request.form['law']
            kB = 1.380649e-23   # Boltzmann constant

            # ---------------------------------
            # Landauer’s Principle
            # Q ≥ kB T ln 2
            # ---------------------------------
            if law == 'landauer':
                T = float(request.form['T'])

                Qmin = kB * T * 0.693147  # ln(2)

                result = {
                    'law': "Landauer’s Principle",
                    'Qmin': Qmin
                }

            # ---------------------------------
            # Shannon Entropy
            # H = − Σ pi ln(pi)
            # ---------------------------------
            elif law == 'shannon':
                p1 = float(request.form['p1'])
                p2 = float(request.form['p2'])
                p3 = float(request.form['p3'])

                probs = [p1, p2, p3]
                H = -sum(p * __import__('math').log(p) for p in probs if p > 0)

                result = {
                    'law': "Shannon Entropy",
                    'H': round(H, 6),
                    'probs': probs
                }

            # ---------------------------------
            # Jarzynski Equality
            # ⟨e^(−βW)⟩ = e^(−βΔG)
            # ---------------------------------
            elif law == 'jarzynski':
                W = float(request.form['W'])
                T = float(request.form['T'])
                deltaG = float(request.form['deltaG'])

                beta = 1 / (kB * T)
                lhs = __import__('math').exp(-beta * W)
                rhs = __import__('math').exp(-beta * deltaG)

                result = {
                    'law': "Jarzynski Equality",
                    'lhs': lhs,
                    'rhs': rhs,
                    'validity': "Satisfied" if abs(lhs - rhs) / rhs < 0.05 else "Not satisfied"
                }

        except:
            result = {'error': 'Invalid input values'}

    return render_template(
        'thermo/information_theoretic_thermodynamics.html',
        result=result
    )
@app.route('/thermodynamics/fluctuation-noise', methods=['GET', 'POST'])
def fluctuation_noise():
    result = None

    if request.method == 'POST':
        try:
            law = request.form['law']
            kB = 1.380649e-23  # Boltzmann constant

            # ---------------------------------
            # Einstein Relation
            # D = μ kB T
            # ---------------------------------
            if law == 'einstein':
                mu = float(request.form['mu'])   # mobility
                T = float(request.form['T'])     # temperature

                D = mu * kB * T

                result = {
                    'law': 'Einstein Relation (Diffusion)',
                    'D': D
                }

            # ---------------------------------
            # Johnson–Nyquist Noise
            # <V^2> = 4 kB T R Δf
            # ---------------------------------
            elif law == 'johnson':
                T = float(request.form['T'])
                R = float(request.form['R'])
                df = float(request.form['df'])

                V2 = 4 * kB * T * R * df

                result = {
                    'law': 'Johnson–Nyquist Noise',
                    'V2': V2
                }

            # ---------------------------------
            # Fluctuation–Dissipation (Simplified)
            # <x^2> = kB T χ
            # ---------------------------------
            elif law == 'fdt':
                chi = float(request.form['chi'])
                T = float(request.form['T'])

                fluct = kB * T * chi

                result = {
                    'law': 'Fluctuation–Dissipation Theorem',
                    'fluct': fluct
                }

        except:
            result = {'error': 'Invalid input values'}

    return render_template(
        'thermo/fluctuation_noise_calculations.html',
        result=result
    )
@app.route('/thermodynamics/turbulence-flow', methods=['GET', 'POST'])
def turbulence_thermo():
    result = None

    if request.method == 'POST':
        try:
            law = request.form['law']

            # ---------------------------------
            # Spectral Energy Balance
            # ∂E/∂t = P − ε − ∂J/∂k
            # ---------------------------------
            if law == 'spectral':
                P = float(request.form['P'])          # production
                eps = float(request.form['eps'])      # dissipation
                dJdk = float(request.form['dJdk'])    # flux gradient

                dEdt = P - eps - dJdk

                result = {
                    'law': 'Spectral Energy Balance',
                    'P': P,
                    'eps': eps,
                    'dJdk': dJdk,
                    'dEdt': round(dEdt, 6)
                }

            # ---------------------------------
            # Turbulent Entropy Production
            # Σ = ε / T
            # ---------------------------------
            elif law == 'entropy_prod':
                eps = float(request.form['eps'])      # dissipation
                T = float(request.form['T'])          # temperature

                Sigma = eps / T

                result = {
                    'law': 'Turbulent Entropy Production',
                    'Sigma': round(Sigma, 6)
                }

        except:
            result = {'error': 'Invalid input values'}

    return render_template(
        'thermo/turbulence_flow_thermodynamics.html',
        result=result
    )
@app.route('/thermodynamics/advanced-properties', methods=['GET', 'POST'])
def advanced_properties():
    result = None

    if request.method == 'POST':
        try:
            law = request.form['law']

            # ---------------------------------
            # Isothermal Compressibility
            # κT = − (1/V) (∂V/∂P)
            # ---------------------------------
            if law == 'compressibility':
                V = float(request.form['V'])
                dVdP = float(request.form['dVdP'])

                kT = -(1 / V) * dVdP

                result = {
                    'law': 'Isothermal Compressibility',
                    'kT': round(kT, 6)
                }

            # ---------------------------------
            # Thermal Expansion Coefficient
            # α = (1/V) (∂V/∂T)
            # ---------------------------------
            elif law == 'expansion':
                V = float(request.form['V'])
                dVdT = float(request.form['dVdT'])

                alpha = (1 / V) * dVdT

                result = {
                    'law': 'Thermal Expansion Coefficient',
                    'alpha': round(alpha, 6)
                }

            # ---------------------------------
            # Joule–Thomson Coefficient
            # μJT = (∂T/∂P)H
            # ---------------------------------
            elif law == 'joule_thomson':
                dTdP = float(request.form['dTdP'])

                result = {
                    'law': 'Joule–Thomson Coefficient',
                    'muJT': round(dTdP, 6)
                }

        except:
            result = {'error': 'Invalid input values'}

    return render_template(
        'thermo/advanced_property_relations.html',
        result=result
    )
@app.route('/thermodynamics/multi-component-equilibrium', methods=['GET', 'POST'])
def multi_component_eq():
    result = None

    if request.method == 'POST':
        try:
            law = request.form['law']

            # ---------------------------------
            # Raoult's Law
            # Pi = xi * Pi*
            # ---------------------------------
            if law == 'raoult':
                xi = float(request.form['xi'])
                P_star = float(request.form['P_star'])

                Pi = xi * P_star

                result = {
                    'law': "Raoult's Law",
                    'Pi': round(Pi, 5),
                    'xi': xi,
                    'P_star': P_star
                }

            # ---------------------------------
            # Nernst / Electrochemical Relation
            # ΔG = −n F E
            # ---------------------------------
            elif law == 'nernst':
                n = float(request.form['n'])
                E = float(request.form['E'])
                F = 96485  # Faraday constant (C/mol)

                deltaG = -n * F * E

                result = {
                    'law': "Nernst / Electrochemical Relation",
                    'deltaG': round(deltaG, 3),
                    'n': n,
                    'E': E
                }

            # ---------------------------------
            # Duhem–Margules (Simplified Form)
            # x1 d(ln P1) + x2 d(ln P2) = 0
            # ---------------------------------
            elif law == 'duhem':
                x1 = float(request.form['x1'])
                dlnP1 = float(request.form['dlnP1'])
                x2 = 1 - x1

                dlnP2 = -(x1 / x2) * dlnP1

                result = {
                    'law': "Duhem–Margules Equation",
                    'x1': x1,
                    'x2': round(x2, 4),
                    'dlnP1': dlnP1,
                    'dlnP2': round(dlnP2, 6)
                }

        except:
            result = {'error': 'Invalid input values'}

    return render_template(
        'thermo/multi_component_equilibrium.html',
        result=result
    )
@app.route('/thermodynamics/superconductivity', methods=['GET', 'POST'])
def superconductivity():
    result = None

    if request.method == 'POST':
        try:
            law = request.form['law']

            # ---------------------------------
            # Critical Magnetic Field
            # Hc = H0 [1 − (T/Tc)^2]
            # ---------------------------------
            if law == 'critical_field':
                H0 = float(request.form['H0'])
                T = float(request.form['T'])
                Tc = float(request.form['Tc'])

                Hc = H0 * (1 - (T / Tc) ** 2)

                result = {
                    'law': 'Critical Magnetic Field',
                    'Hc': round(Hc, 6),
                    'H0': H0,
                    'T': T,
                    'Tc': Tc
                }

            # ---------------------------------
            # London Penetration Depth
            # H(x) = H(0) e^(−x/λ)
            # ---------------------------------
            elif law == 'london':
                H0 = float(request.form['H0'])
                x = float(request.form['x'])
                lam = float(request.form['lam'])

                Hx = H0 * __import__('math').exp(-x / lam)

                result = {
                    'law': 'London Penetration Depth',
                    'Hx': round(Hx, 6),
                    'H0': H0,
                    'x': x,
                    'lam': lam
                }

            # ---------------------------------
            # Gibbs Free Energy Difference
            # ΔG = Gn − Gs
            # ---------------------------------
            elif law == 'gibbs_transition':
                Gn = float(request.form['Gn'])
                Gs = float(request.form['Gs'])

                deltaG = Gn - Gs

                result = {
                    'law': 'Gibbs Free Energy of Transition',
                    'deltaG': round(deltaG, 6)
                }

        except:
            result = {'error': 'Invalid input values'}

    return render_template(
        'thermo/superconductivity_phase_transition.html',
        result=result
    )
@app.route('/thermodynamics/plasma-astrophysical', methods=['GET', 'POST'])
def plasma_astro():
    result = None

    if request.method == 'POST':
        try:
            law = request.form['law']

            kB = 1.380649e-23     # Boltzmann constant (J/K)
            h = 6.62607015e-34    # Planck constant (J·s)
            me = 9.10938356e-31   # Electron mass (kg)

            # ---------------------------------
            # Saha Ionization Equation (Simplified)
            # ni+1 ne / ni = (2πme kT / h²)^(3/2) e^(−χ / kT)
            # ---------------------------------
            if law == 'saha':
                T = float(request.form['T'])          # temperature
                chi = float(request.form['chi'])      # ionization energy (J)

                saha_ratio = ((2 * 3.14159 * me * kB * T) / h**2) ** 1.5 \
                              * __import__('math').exp(-chi / (kB * T))

                result = {
                    'law': 'Saha Ionization Equation',
                    'ratio': saha_ratio
                }

            # ---------------------------------
            # Internal Partition Function (Simplified)
            # Z = Σ gi e^(−Ei / kT)
            # ---------------------------------
            elif law == 'partition':
                g1 = float(request.form['g1'])
                E1 = float(request.form['E1'])
                g2 = float(request.form['g2'])
                E2 = float(request.form['E2'])
                T = float(request.form['T'])

                Z = g1 * __import__('math').exp(-E1 / (kB * T)) + \
                    g2 * __import__('math').exp(-E2 / (kB * T))

                result = {
                    'law': 'Internal Partition Function',
                    'Z': round(Z, 6)
                }

            # ---------------------------------
            # Hydrostatic Equilibrium (Barometric Law)
            # P(z) = P0 e^(−mgz / kT)
            # ---------------------------------
            elif law == 'hydrostatic':
                P0 = float(request.form['P0'])
                m = float(request.form['m'])
                g = float(request.form['g'])
                z = float(request.form['z'])
                T = float(request.form['T'])

                Pz = P0 * __import__('math').exp(-(m * g * z) / (kB * T))

                result = {
                    'law': 'Hydrostatic Equilibrium',
                    'Pz': round(Pz, 6)
                }

        except:
            result = {'error': 'Invalid input values'}

    return render_template(
        'thermo/plasma_astrophysical_thermodynamics.html',
        result=result
    )
@app.route('/thermodynamics/biological-chemical', methods=['GET', 'POST'])
def bio_chem_thermo():
    result = None

    if request.method == 'POST':
        try:
            law = request.form['law']

            R = 8.314      # J/mol·K
            F = 96485     # C/mol

            # ---------------------------------
            # Nernst Equation (Membrane Potential)
            # E = (RT / zF) ln(Co / Ci)
            # ---------------------------------
            if law == 'nernst_membrane':
                T = float(request.form['T'])
                z = float(request.form['z'])
                Cout = float(request.form['Cout'])
                Cin = float(request.form['Cin'])

                E = (R * T) / (z * F) * __import__('math').log(Cout / Cin)

                result = {
                    'law': 'Nernst Equation (Membrane Potential)',
                    'E': round(E, 6)
                }

            # ---------------------------------
            # Coupled Reactions
            # ΔGtotal = ΔG1 + ΔG2
            # ---------------------------------
            elif law == 'coupled':
                dG1 = float(request.form['dG1'])
                dG2 = float(request.form['dG2'])

                dG_total = dG1 + dG2

                result = {
                    'law': 'Coupled Biochemical Reactions',
                    'dG_total': round(dG_total, 4),
                    'feasible': 'Spontaneous' if dG_total < 0 else 'Non-spontaneous'
                }

            # ---------------------------------
            # Chemical Potential (Biological Mixture)
            # μ = μ0 + RT ln a
            # ---------------------------------
            elif law == 'chemical_potential':
                mu0 = float(request.form['mu0'])
                a = float(request.form['a'])
                T = float(request.form['T'])

                mu = mu0 + R * T * __import__('math').log(a)

                result = {
                    'law': 'Chemical Potential (Biological Systems)',
                    'mu': round(mu, 4)
                }

        except:
            result = {'error': 'Invalid input values'}

    return render_template(
        'thermo/biological_chemical_thermodynamics.html',
        result=result
    )
@app.route('/thermodynamics/advanced-materials', methods=['GET', 'POST'])
def advanced_materials():
    result = None

    if request.method == 'POST':
        try:
            law = request.form['law']

            # ---------------------------------
            # Roeser–Huber Formalism (Simplified)
            # Tc = K * (a / d)^2
            # ---------------------------------
            if law == 'roeser_huber':
                K = float(request.form['K'])      # material constant
                a = float(request.form['a'])      # lattice parameter
                d = float(request.form['d'])      # interatomic spacing

                Tc = K * (a / d) ** 2

                result = {
                    'law': 'Roeser–Huber Formalism',
                    'Tc': round(Tc, 4)
                }

            # ---------------------------------
            # Low-Temperature Specific Heat
            # Cv = γT + A T^3
            # ---------------------------------
            elif law == 'specific_heat':
                gamma = float(request.form['gamma'])   # electronic coefficient
                A = float(request.form['A'])           # lattice coefficient
                T = float(request.form['T'])           # temperature

                Cv = gamma * T + A * T**3

                result = {
                    'law': 'Low-Temperature Specific Heat of Metals',
                    'Cv': round(Cv, 6),
                    'T': T,
                    'Ce': round(gamma * T, 6),
                    'Cl': round(A * T**3, 6)
                }

        except:
            result = {'error': 'Invalid input values'}

    return render_template(
        'thermo/advanced_material_calculations.html',
        result=result
    )

if __name__ == '__main__':
    app.run(debug=True)

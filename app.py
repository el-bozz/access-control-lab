from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import check_password_hash

app = Flask(__name__)
# Secret key is needed to use sessions (keeping users logged in)
app.secret_key = 'super_secret_demo_key_123'

# Helper function to connect to the database
def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row # This lets us access columns by name
    return conn

# --- ROUTES ---

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            # Login successful! Save user info in the session
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid credentials. Try again.'
            
    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    # Get only the orders that belong to the logged-in user
    orders = conn.execute('SELECT * FROM orders WHERE user_id = ?', (session['user_id'],)).fetchall()
    conn.close()
    
    return render_template('dashboard.html', orders=orders)

# 🚨 VULNERABILITY 1: IDOR (Insecure Direct Object Reference)
@app.route('/order/<int:order_id>')
def view_order(order_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    # FLAW: We are fetching the order by ID, but we are NOT checking if this order belongs to the logged-in user!
    order = conn.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
    conn.close()
    
    if order:
        return render_template('order.html', order=order)
    return "Order not found", 404

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db()
    if request.method == 'POST':
        # 🚨 VULNERABILITY 2: Mass Assignment / Parameter Tampering
        # FLAW: We are blindly trusting the 'role' parameter sent by the user's browser!
        new_role = request.form.get('role')
        
        if new_role:
            conn.execute('UPDATE users SET role = ? WHERE id = ?', (new_role, session['user_id']))
            conn.commit()
            session['role'] = new_role # Update the session too
            
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    conn.close()
    return render_template('profile.html', user=user)

@app.route('/admin')
def admin():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    # 🚨 VULNERABILITY 3: Broken Access Control
    # FLAW: We check if the user is logged in, but we FORGOT to check if session['role'] == 'admin'!
    conn = get_db()
    users = conn.execute('SELECT id, username, role, email FROM users').fetchall()
    conn.close()
    
    return render_template('admin.html', users=users)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Run the app on port 5000, accessible from the phone's browser
    app.run(host='0.0.0.0', port=5000, debug=True)

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from tinydb import TinyDB, Query
from datetime import datetime
from tinydb.operations import delete
import os

app = Flask(__name__)
app.secret_key = "kila_dreka"

db = TinyDB('klepet.json')
users = db.table('uporabniki')
messages = db.table('sporocila')
User = Query()

@app.route('/')
def index():
    if 'username' in session:
        return render_template('chat.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            user = users.get(User.username == username)
            
            if user:
                if user['password'] == password:
                    session['username'] = username
                    return jsonify({'success': True})
                else:
                    return jsonify({'success': False, 'error': 'Napačno geslo'})
            else:
                users.insert({'username': username, 'password': password})
                session['username'] = username
                return jsonify({'success': True})
        except Exception as e:
            print(f"Napaka pri prijavi: {str(e)}")
            return jsonify({'success': False, 'error': 'Prišlo je do napake'})
    
    return render_template('login.html')

@app.route('/kviz')
def goToHomePage():
    return render_template('kviz.html')
    
@app.route('/logout')
def logout():
     session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
 if not os.path.exists('templates'):
        os.makedirs('templates')
    
    app.run(debug=True)

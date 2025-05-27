from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from tinydb import TinyDB, Query
import os

app = Flask(__name__)
app.secret_key = "kila_dreka"

db = TinyDB('spg.json')
users = db.table('uporabniki')
User = Query()

pesniki = [
    {"id": 1, "pesnik_ime": "France", "pesnik_priimek": "Prešeren", "pesnik_slika": "https://www.ekoper.si/wp-content/uploads/2017/02/france.jpg", "pesnik_rojen": "1800", "pesnik_umrl": "1849"},
    {"id": 2, "pesnik_ime": "Matija", "pesnik_priimek": "Čop", "pesnik_slika": "https://javnost.si/wp-content/uploads/2022/07/Matija-Cop-1200x630.jpg", "pesnik_rojen": "1797", "pesnik_umrl": "1835"},
    {"id": 3, "pesnik_ime": "Anton", "pesnik_priimek": "Aškerc", "pesnik_slika": "https://n1info.si/wp-content/uploads/2022/06/09/1654776210-askerc3-1024x768.jpg", "pesnik_rojen": "1856", "pesnik_umrl": "1912"},
    {"id": 4, "pesnik_ime": "Simon", "pesnik_priimek": "Gregorčič", "pesnik_slika": "https://www.miszalozba.com/cache/img/author/420a48-83c00ece4a02019531ec7305ba2b5bbf@w1200.jpg", "pesnik_rojen": "1844", "pesnik_umrl": "1906"},
    {"id": 5, "pesnik_ime": "Fran", "pesnik_priimek": "Levstik", "pesnik_slika": "https://www.travel-slovenia.si/wp-content/uploads/2018/09/travel-slovenia-fran-levstik.jpg", "pesnik_rojen": "1831", "pesnik_umrl": "1887"},
    {"id": 6, "pesnik_ime": "Josip", "pesnik_priimek": "Jurčič", "pesnik_slika": "https://www.slovenska-biografija.si/static/osebe/sbi260454_Jurcic_Josip.jpg", "pesnik_rojen": "1844", "pesnik_umrl": "1881"},
    {"id": 7, "pesnik_ime": "Ivan", "pesnik_priimek": "Tavčar", "pesnik_slika": "https://www.obrazislovenskihpokrajin.si/slir/w800-h1057-c800x1057/wp-content/uploads/2020/01/gorenjci-Img_00000590.gif", "pesnik_rojen": "1851", "pesnik_umrl": "1923"},
    {"id": 8, "pesnik_ime": "Oton", "pesnik_priimek": "Župančič", "pesnik_slika": "https://www.slovenska-biografija.si/static/osebe/sbi913178_Zupancic_Oton.jpg", "pesnik_rojen": "1878", "pesnik_umrl": "1949"},
    {"id": 9, "pesnik_ime": "Dragotin", "pesnik_priimek": "Kette", "pesnik_slika": "https://www.obrazislovenskihpokrajin.si/slir/w800-h1057-c800x1057/wp-content/uploads/2019/12/Kette-Dragotin.jpg", "pesnik_rojen": "1876", "pesnik_umrl": "1899"},
    {"id": 10, "pesnik_ime": "Josip", "pesnik_priimek": "Murn Aleksandrov", "pesnik_slika": "https://i0.wp.com/kd-severinsali.si/wp-content/uploads/2019/03/FOTOGRAFIJA-JOSIPA-MURNA.jpg", "pesnik_rojen": "1879", "pesnik_umrl": "1901"},
    {"id": 11, "pesnik_ime": "Ivan", "pesnik_priimek": "Cankar", "pesnik_slika": "https://www.vrhnika.si/wp-content/uploads/2021/07/Ivan-Cankar-1.png", "pesnik_rojen": "1876", "pesnik_umrl": "1918"},
    {"id": 12, "pesnik_ime": "Srečko", "pesnik_priimek": "Kosovel", "pesnik_slika": "https://www.miszalozba.com/cache/img/author/b7f4d8-8d538538fbfae4b77429f7d6457fc2e2@w1200.jpg", "pesnik_rojen": "1904", "pesnik_umrl": "1926"},
    {"id": 13, "pesnik_ime": "Lovro", "pesnik_priimek": "Kuhar (Prežihov Voranc)", "pesnik_slika": "https://www.obrazislovenskihpokrajin.si/slir/w800-h1057-c800x1057/wp-content/uploads/2019/09/Pre%C5%BEihov-Voranc_Portret_2_osp-1024x728.jpg", "pesnik_rojen": "1893", "pesnik_umrl": "1950"}
]

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('kviz'))  
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
                    # Inicializiramo seznam uporabljenih pesnikov ob prijavi
                    session['uporabljeni_pesniki'] = []
                    return jsonify({'success': True, 'redirect': url_for('kviz')}) 
                else:
                    return jsonify({'success': False, 'error': 'Napačno geslo'})
            else:
                users.insert({'username': username, 'password': password})
                session['username'] = username
                # Inicializiramo seznam uporabljenih pesnikov ob registraciji
                session['uporabljeni_pesniki'] = []
                return jsonify({'success': True, 'redirect': url_for('kviz')})  
        except Exception as e:
            print(f"Napaka pri prijavi: {str(e)}")
            return jsonify({'success': False, 'error': 'Prišlo je do napake'})
    
    return render_template('login.html')

@app.route('/kviz')
def kviz():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Preverimo, če so vsi pesniki že bili uporabljeni
    if 'uporabljeni_pesniki' in session and len(session['uporabljeni_pesniki']) >= len(pesniki):
        return redirect(url_for('konec'))
    
    return render_template('kviz.html')
    
@app.route('/logout')
def logout():
    # Clear all data from the JSON file
    db.truncate()
    # Clear session data
    session.pop('username', None)
    session.pop('tocke', None)
    session.pop('runda', None)
    session.pop('uporabljeni_pesniki', None)
    return redirect(url_for('login'))

@app.route('/pesniki', methods=['GET'])
def get_pesniki():
    # Vrnemo samo pesnike, ki še niso bili uporabljeni
    if 'uporabljeni_pesniki' not in session:
        session['uporabljeni_pesniki'] = []
    
    neuporabljeni_pesniki = []
    for p in pesniki:
        if p['id'] not in session['uporabljeni_pesniki']:
            neuporabljeni_pesniki.append(p)
    return jsonify(neuporabljeni_pesniki)

@app.route("/pesniki/<int:pesnik_id>", methods=["GET"])
def get_pesnik(pesnik_id):
    pesnik = None
    for pesnik in pesniki:
        if pesnik["id"] == pesnik_id:
            pesnik = pesnik
            break

    if pesnik:
        return jsonify(pesnik)
    return jsonify({"error": "pesnik ne obstaja"}), 404

@app.route("/dodaj_pesnika", methods=["POST"])
def dodaj_pesnika():
    podatki = request.get_json()
    return jsonify(podatki), 201

@app.route("/get_score", methods=["GET"])
def get_score():
    return jsonify({
        "tocke": session.get('tocke', 0),
        "runda": session.get('runda', 1)
    })

@app.route("/preveri_pesnika", methods=["POST"])
def check_poet():
    data = request.get_json()
    pesnik_id = data['pesnik_id']
    vnos = data['vnos']

    if 'tocke' not in session:
        session['tocke'] = 0
    if 'runda' not in session:
        session['runda'] = 1
    if 'uporabljeni_pesniki' not in session:
        session['uporabljeni_pesniki'] = []

    poet = None
    for p in pesniki:
        if p['id'] == pesnik_id:
            poet = p
            break
    
    if not poet:
        session['runda'] += 1
        session.modified = True
        return jsonify({
            "correct": False,
            "partial": 0,
            "tocke": session['tocke'],
            "runda": session['runda'],
            "tocke_dodatek": 0
        })
    
    # Dodamo pesnika v seznam uporabljenih
    if pesnik_id not in session['uporabljeni_pesniki']:
        session['uporabljeni_pesniki'].append(pesnik_id)
        session.modified = True
    
    tocke_dodatek = 0
    pravilni_deli = 0
    
    if vnos['ime'].lower() == poet['pesnik_ime'].lower():
        pravilni_deli += 1
    if vnos['priimek'].lower() == poet['pesnik_priimek'].lower():
        pravilni_deli += 1
    if vnos['rojen'] == poet['pesnik_rojen']:
        pravilni_deli += 1
    if vnos['umrl'] == poet['pesnik_umrl']:
        pravilni_deli += 1
    
    tocke_dodatek = pravilni_deli * 25
    
    session['tocke'] += tocke_dodatek
    session['runda'] += 1
    session.modified = True
    
    correct = (pravilni_deli == 4)
    
    # Preverimo, če so vsi pesniki uporabljeni
    if session["runda"] >= len(pesniki):
        return jsonify({
            "correct": correct,
            "partial": pravilni_deli,
            "tocke": session.get('tocke', 0), 
            "runda": session.get('runda', 1),
            "tocke_dodatek": tocke_dodatek,
            "redirect": url_for('konec')
        })
    
    return jsonify({
        "correct": correct,
        "partial": pravilni_deli,
        "tocke": session.get('tocke', 0), 
        "runda": session.get('runda', 1),
        "tocke_dodatek": tocke_dodatek
    })


@app.route('/konec')
def konec():
    # Izračunajmo odstotek pravilnih odgovorov
    max_tocke = len(pesniki) * 100 
    dosezene_tocke = session.get('tocke', 0)
    odstotek = (dosezene_tocke / max_tocke) * 100 
    
    # Določimo oceno
    if odstotek < 50:
        ocena = 1
    elif odstotek < 63:
        ocena = 2
    elif odstotek < 75:
        ocena = 3
    elif odstotek < 90:
        ocena = 4
    else:
        ocena = 5
    
    return render_template(
        'konec.html', 
        tocke=dosezene_tocke,
        max_tocke=max_tocke,
        odstotek=round(odstotek, 2),
        ocena=ocena)

@app.route("/konec", methods=["POST"])
def reset_igre():
    session['tocke'] = 0
    session['runda'] = 1
    session['uporabljeni_pesniki'] = []
    session.modified = True
    return jsonify({"success": True})

if __name__ == "__main__":
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    app.run(debug=True)

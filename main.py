from flask import Flask, request, jsonify, render_template
import requests
app = Flask(__name__)

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

@app.route('/pesniki', methods=['GET'])
def get_pesniki():
    return jsonify(pesniki)

@app.route("/pesniki/<int:pesnik_id>", methods = ["GET"])
def get_pesnik(pesnik_id):
    pesnik = next((pesnik for pesnik in pesniki if pesnik["id"] == pesnik_id), None)
    if pesnik:
        return jsonify(pesnik)
    return jsonify({"error": "pesnik ne obstaja"}), 404

@app.route("/dodaj_pesnika", methods=["POST"])
def dodaj_pesnika():
    podatki = podatki.get_json()

    return jsonify(podatki), 201
    
@app.route("/check_poet", methods=["POST"])
def check_poet():
    data = request.get_json()
    poet_id = data['poet_id']
    user_input = data['user_input']
    
    poet = next((p for p in pesniki if p['id'] == poet_id), None)
    
    if not poet:
        return jsonify({"correct": False})
    
    correct = (
        user_input['ime'].lower() == poet['pesnik_ime'].lower() and
        user_input['priimek'].lower() == poet['pesnik_priimek'].lower() and
        user_input['rojen'] == poet['pesnik_rojen'] and
        user_input['umrl'] == poet['pesnik_umrl']
    )
    
    return jsonify({"correct": correct})

if __name__ == ("__main__"):
    app.run(debug=True)

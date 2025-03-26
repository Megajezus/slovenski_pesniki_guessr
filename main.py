from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/get_pesnik/<pesnik_id>")
def get_pesnik(pesnik_id):
    pesnik_data = {
        "pesnik_id" : pesnik_id,
        "pesnik_ime" : "France",
        "pesnik_priimek" : "Preseren",
        "pesnik_slika" : "/",
        "pesnik_rojen" : "1800",
        "pesnik_umrl" : "1849"
    }

    extra = request.args.get("extra")
    if extra :
        pesnik_data["extra"] = extra

    return jsonify(pesnik_data), 200

@app.route("/dodaj_pesnika", methods=["POST"])
def dodaj_pesnika():
    podatki = podatki.get_json()

    return jsonify(podatki), 201

if __name__ == ("__main__"):
    app.run(debug=True)
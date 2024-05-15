from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
import requests

# Setter opp applikasjon
app = Flask(__name__)
CORS(app)


# Rute for hjemmeside
@app.route('/', methods = ["GET"])
def index():
  restauranter = requests.get('http://127.0.0.1:5010/get_restauranter').json()
  return render_template('index.html', restauranter=restauranter)

# Rute for siden for valgt restaurant
@app.route('/get_restaurant/<rid>', methods = ["GET"]) # rid er Restaurant id
def get_restaurant(rid):
  restaurant_meny = requests.get('http://127.0.0.1:5010/get_restaurant_meny', json={"rid": rid}).json()
  restaurant = requests.get('http://127.0.0.1:5010/get_restaurant', json={"rid": rid}).json()
  return render_template('restaurant.html', restaurant=restaurant, meny=restaurant_meny)



# Rute som håndterer eier som logger inn
@app.route('/logg_inn', methods=["GET","POST"])
def logg_inn():
  if request.method == "GET":
    return render_template('logg_inn.html')

  if request.method == "POST":
    navn = request.form.get('navn')
    passord = request.form.get('passord')
    bruker = requests.get('http://127.0.0.1:5010/logg_inn', json={"navn": navn, "passord": passord}).json()
    if bruker["status"] == "finnes":
      return redirect(url_for('eier_sin_side', rid=bruker["rid"], navn=bruker["navn"]))
    print(bruker["status"])
    return render_template('logg_inn.html', status=bruker["status"])

# rute som sender bruker til eier_sin_side.html
@app.route('/eier_sin_side/<rid>/<navn>', methods = ["GET"])
def eier_sin_side(rid, navn):
  restaurant_meny = requests.get('http://127.0.0.1:5010/get_restaurant_meny', json={"rid": rid}).json()
  restaurant = requests.get('http://127.0.0.1:5010/get_restaurant', json={"rid": rid}).json()
  return render_template('eier_sin_side.html', navn=navn, meny=restaurant_meny, restaurant=restaurant, rid=restaurant[0])

# Rute som sender request til serveren for å fjerne valgt rett
@app.route('/fjern_rett/<rett_id>/<rid>/<navn>', methods=["POST"])
def fjern_rett(rett_id, rid, navn):
  requests.delete('http://127.0.0.1:5010/fjern_rett', json={"rett_id": rett_id, "rid": rid})
  return redirect(url_for('eier_sin_side', rid=rid, navn=navn))

# Rute som sender bruker til rediger side
@app.route('/rediger_rett/<rett_id>/<rid>/<navn>', methods=["get"])
def rediger_rett(rett_id, rid, navn):
  rett = requests.get('http://127.0.0.1:5010/get_rett', json={"rett_id": rett_id, "rid": rid}).json()
  return render_template('rediger.html', rett=rett, rett_id=rett_id, rid=rid, navn=navn)



@app.route('/rediger/rett/<rett_id>/<rid>/<navn>', methods=["POST"])
def rediger_rett_tekst(rett_id, rid, navn):
  rett_tekst = request.form.get('tekst')
  requests.put('http://127.0.0.1:5010/rediger_tekst', json={"rett_id": rett_id, "rid": rid, "content": rett_tekst})
  return redirect(url_for('eier_sin_side', rid=rid, navn=navn))

@app.route('/rediger/beskrivelse/<rett_id>/<rid>/<navn>', methods=["POST"])
def rediger_rett_beskrivelse(rett_id, rid, navn):
  rett_beskrivelse = request.form.get('beskrivelse')
  requests.put('http://127.0.0.1:5010/rediger_beskrivelse', json={"rett_id": rett_id, "rid": rid, "content": rett_beskrivelse})
  return redirect(url_for('eier_sin_side', rid=rid, navn=navn))

@app.route('/rediger/pris/<rett_id>/<rid>/<navn>', methods=["POST"])
def rediger_rett_pris(rett_id, rid, navn):
  rett_pris = request.form.get('pris')
  requests.put('http://127.0.0.1:5010/rediger_pris', json={"rett_id": rett_id, "rid": rid, "content": rett_pris})
  return redirect(url_for('eier_sin_side', rid=rid, navn=navn))

# Starter applikasjonen på port 5000
if __name__ == "__main__":
  app.run(debug=True, port=5020)
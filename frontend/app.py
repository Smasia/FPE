from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS
import requests
import secrets

# Setter opp applikasjon
app = Flask(__name__)
CORS(app)

app.secret_key = secrets.token_hex()

# Rute for hjemmeside
@app.route('/', methods = ["GET"])
def index():
  if "user" in session:
    restauranter = requests.get('http://127.0.0.1:5010/get_restauranter').json()
    return render_template('index.html', restauranter=restauranter, navn = session["user"])
  else:
    restauranter = requests.get('http://127.0.0.1:5010/get_restauranter').json()
    return render_template('index.html', restauranter=restauranter)



# Rute som sender bruker til restaurant.html side
@app.route('/get_restaurant/<rid>', methods = ["GET"])
def get_restaurant(rid):
  if "user" in session:
    restaurant_meny = requests.get('http://127.0.0.1:5010/get_restaurant_meny', json={"rid": rid}).json()
    restaurant = requests.get('http://127.0.0.1:5010/get_restaurant', json={"rid": rid}).json()
    return render_template('restaurant.html', restaurant=restaurant, meny=restaurant_meny, navn = session["user"])
  else:
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

    # Sjekker om bruker er eier
    if bruker["status"] == "finnes" and bruker["rid"] != None:
      session["user"] = navn
      session["rid"] = bruker["rid"]
      return redirect(url_for('eier_sin_side', rid=session["rid"], navn=session["user"]))
    # Sjekker om bruker er kunde
    if bruker["status"] == "finnes" and bruker["rid"] == None:
      session["user"] = navn
      return redirect('index')
    return render_template('logg_inn.html', status=bruker["status"])



# Rute for å registrere bruker
@app.route('/registrer', methods=["GET", "POST"])
def registrer():
  if request.method == "GET":
    return render_template('registrer.html')
  
  if request.method == "POST":
    navn = request.form.get('navn')
    passord = request.form.get('passord')
    requests.post('http://127.0.0.1:5010/registrer', json={"navn": navn, "passord": passord})
    session["user"] = navn
    return redirect(url_for('index'))



# rute som sender bruker til eier_sin_side.html
@app.route('/eier_sin_side/<rid>/<navn>', methods = ["GET"])
def eier_sin_side(rid, navn):
  if "user" in session and "rid" in session:
    restaurant_meny = requests.get('http://127.0.0.1:5010/get_restaurant_meny', json={"rid": rid}).json()
    restaurant = requests.get('http://127.0.0.1:5010/get_restaurant', json={"rid": rid}).json()
    return render_template('eier_sin_side.html', navn=session["user"], meny=restaurant_meny, restaurant=restaurant, rid=restaurant[0])
  else:
    return redirect('/logg_inn')



# Rute som sender bruker til legg_til.html side
@app.route('/legg_til_ny_rett/<rid>/<navn>', methods=["GET"])
def legg_til_ny_rett(rid, navn):
  if "user" in session and "rid" in session:
    return render_template('legg_til.html', rid=session["rid"], navn=session["user"])
  else:
    return redirect('/logg_inn')



# Rute som sender request til serveren for å fjerne valgt rett
@app.route('/fjern_rett/<rett_id>/<rid>/<navn>', methods=["POST"])
def fjern_rett(rett_id, rid, navn):
  if "user" in session and "rid" in session:
    requests.delete('http://127.0.0.1:5010/fjern_rett', json={"rett_id": rett_id, "rid": rid})
    return redirect(url_for('eier_sin_side', rid=session["rid"], navn=session["user"]))
  else:
    return redirect('/logg_inn')



# Rute som sender bruker til rediger.html side
@app.route('/rediger_rett/<rett_id>/<rid>/<navn>', methods=["get"])
def rediger_rett(rett_id, rid, navn):
  if "user" in session and "rid" in session:
    rett = requests.get('http://127.0.0.1:5010/get_rett', json={"rett_id": rett_id, "rid": rid}).json()
    return render_template('rediger.html', rett=rett, rett_id=rett_id, rid=session["rid"], navn=session["user"])
  else:
    return redirect('/logg_inn')



# Rute for å endre navn på retten
@app.route('/rediger/rett/<rett_id>/<rid>/<navn>', methods=["POST"])
def rediger_rett_tekst(rett_id, rid, navn):
  if "user" in session and "rid" in session:
    rett_tekst = request.form.get('tekst')
    requests.put('http://127.0.0.1:5010/rediger_tekst', json={"rett_id": rett_id, "rid": rid, "content": rett_tekst})
    return redirect(url_for('eier_sin_side', rid=session["rid"], navn=navn))
  else:
    return redirect('/logg_inn')



# Rute for å endre beskrivelse på retten
@app.route('/rediger/beskrivelse/<rett_id>/<rid>/<navn>', methods=["POST"])
def rediger_rett_beskrivelse(rett_id, rid, navn):
  if "user" in session and "rid" in session:
    rett_beskrivelse = request.form.get('beskrivelse')
    requests.put('http://127.0.0.1:5010/rediger_beskrivelse', json={"rett_id": rett_id, "rid": rid, "content": rett_beskrivelse})
    return redirect(url_for('eier_sin_side', rid=session["rid"], navn=session["user"]))
  else:
    return redirect('/logg_inn')



# Rute for å endre pris på retten
@app.route('/rediger/pris/<rett_id>/<rid>/<navn>', methods=["POST"])
def rediger_rett_pris(rett_id, rid, navn):
  if "user" in session and "rid" in session:
    rett_pris = request.form.get('pris')
    requests.put('http://127.0.0.1:5010/rediger_pris', json={"rett_id": rett_id, "rid": rid, "content": rett_pris})
    return redirect(url_for('eier_sin_side', rid=session["rid"], navn=session["user"]))
  else:
    return redirect('/logg_inn')



# Rute for å logge ut
@app.route('/logg_ut')
def logg_ut():
    session.pop('user', None)
    return redirect(url_for('index'))



# Starter applikasjonen på port 5000
if __name__ == "__main__":
  app.run(debug=True, port=5000)
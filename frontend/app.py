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
  return render_template('eier_sin_side.html', navn=navn, meny=restaurant_meny, restaurant=restaurant)

# Starter applikasjonen på port 5000
if __name__ == "__main__":
  app.run(debug=True, port=5000)
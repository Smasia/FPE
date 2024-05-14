from flask import Flask, request, send_from_directory
from flask_cors import CORS
import sqlite3

# Sette opp applikasjonen
app = Flask(__name__)
CORS(app)

# Sette opp kobling og peker til database
con = sqlite3.connect('./database.db', check_same_thread=False)
cur = con.cursor()

# Rute for å hente bilder fra serveren
@app.route('/get_image/<image_name>', methods = ["GET"])
def get_image(image_name):
    return send_from_directory('E:\\Utvikling\\forberedelsePrøveEksamen\\backend\\static\\images', image_name)
#/var/www/flask-application/static/images/

# Rute for å hente restauranter fra serveren
@app.route('/get_restauranter', methods = ["GET"])
def get_restaurants():
   cur.execute("SELECT * FROM restauranter")
   content = cur.fetchall()
   result = []
   for restaurant in content:
      result.append({"navn": restaurant[1], "id": restaurant[0]})
   return result

# Rute for å hente valgt restaurant fra serveren
@app.route('/get_restaurant', methods = ["GET"])
def get_restaurant():
   rid = request.get_json()["rid"]
   cur.execute("SELECT * FROM restauranter WHERE id = ?", (rid,))
   content = cur.fetchone()
   result = [content[0], content[1]]
   return result

# Rute for å hente menyer og retter fra serveren
@app.route('/get_restaurant_meny', methods = ["GET"])
def restaurant_meny():
  rid = request.get_json()["rid"]
  cur.execute("SELECT * FROM meny_retter WHERE restaurant_id = ?", (rid,))
  content = cur.fetchall()
  result = []
  for data in content:
    result.append({"id": data[0], "rid": data[1], "rett": data[2], "bilde": data[3], "beskrivelse": data[4], "pris": data[5]})
  return result

# rute som leter etter bruker i database og sender melder om den finnes eller ikke
@app.route('/logg_inn', methods = ["GET"])
def logg_inn():
   navn = request.get_json()["navn"]
   passord = request.get_json()["passord"]
   cur.execute("SELECT * FROM brukere WHERE navn = ? AND passord = ?", (navn, passord))
   bruker = cur.fetchone()
   if bruker:
    return {"status": "finnes", "navn": bruker[2], "rid": bruker[1]}
   return {"status": "finnes_ikke"}
# Starter applikasjonen på port 5010
if __name__ == "__main__":
  app.run(debug=True, port=5010)
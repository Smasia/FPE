import os
from flask import Flask, request, send_from_directory, redirect
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
# E:\\Utvikling\\forberedelsePrøveEksamen\\backend\\static\\images\\



# Rute for å lagre bilde i serveren og oppdatere databasen så den peker til det nye bilde. Fjerner også det gamle bilde
@app.route('/post_image/<rett_id>/<rid>/<navn>', methods=['POST'])
def upload_image(rett_id, rid, navn):
    new_image_file = request.files['image']
    cur.execute("SELECT bilde from meny_retter WHERE restaurant_id = ? AND id = ?", (rid, rett_id))
    old_image_file = cur.fetchone()[0]
    
    print("start")
    os.remove('E:\\Utvikling\\forberedelsePrøveEksamen\\backend\\static\\images\\' + old_image_file)
    print("Slutt")
    new_image_file.save('E:\\Utvikling\\forberedelsePrøveEksamen\\backend\\static\\images\\' + new_image_file.filename)

    cur.execute("UPDATE meny_retter SET bilde = ? WHERE restaurant_id = ? AND id = ?", (new_image_file.filename, rid, rett_id))
    con.commit()
    
    return redirect('http://127.0.0.1:5000/eier_sin_side/' + rid + "/" + navn)



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
def get_restaurant_meny():
  rid = request.get_json()["rid"]
  cur.execute("SELECT * FROM meny_retter WHERE restaurant_id = ?", (rid,))
  content = cur.fetchall()
  result = []
  for data in content:
    result.append({"id": data[0], "rid": data[1], "rett": data[2], "bilde": data[3], "beskrivelse": data[4], "pris": data[5]})
  return result



# Rute for å hente en rett
@app.route('/get_rett', methods = ["GET"])
def get_rett():
  rid = request.get_json()["rid"]
  rett_id = request.get_json()["rett_id"]
  cur.execute("SELECT * FROM meny_retter WHERE restaurant_id = ? AND id = ?", (rid,rett_id))
  content = cur.fetchone()
  result = {"id": content[0], "rid": content[1], "rett": content[2], "bilde": content[3], "beskrivelse": content[4], "pris": content[5]}
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



# Rute for å fjerne rett
@app.route('/fjern_rett', methods=["DELETE"])
def fjern_rett():
  rett_id = request.get_json()["rett_id"]
  rid = request.get_json()["rid"]
  cur.execute("SELECT bilde from meny_retter WHERE restaurant_id = ? AND id = ?", (rid, rett_id))
  old_image_file = cur.fetchone()[0]


  cur.execute("DELETE FROM meny_retter WHERE restaurant_id = ? AND id = ?", (rid, rett_id))
  con.commit()
  os.remove('E:\\Utvikling\\forberedelsePrøveEksamen\\backend\\static\\images\\' + old_image_file)

  return "succes", 200



# Rute for å endre navn på rett
@app.route('/rediger_tekst', methods=["PUT"])
def rediger_rett():
  rett_id = request.get_json()["rett_id"]
  rid = request.get_json()["rid"]
  content = request.get_json()["content"]
  cur.execute("UPDATE meny_retter SET rett = ? WHERE restaurant_id = ? AND id = ?", (content,rid, rett_id))
  con.commit()
  return "success", 200


# Rute for å endre besrivelse på rett
@app.route('/rediger_beskrivelse', methods=["PUT"])
def rediger_beskrivelse():
  rett_id = request.get_json()["rett_id"]
  rid = request.get_json()["rid"]
  content = request.get_json()["content"]
  cur.execute("UPDATE meny_retter SET beskrivelse = ? WHERE restaurant_id = ? AND id = ?", (content,rid, rett_id))
  con.commit()
  return "success", 200


# Rute for å endre pris på rett
@app.route('/rediger_pris', methods=["PUT"])
def rediger_pris():
  rett_id = request.get_json()["rett_id"]
  rid = request.get_json()["rid"]
  content = request.get_json()["content"]
  cur.execute("UPDATE meny_retter SET pris = ? WHERE restaurant_id = ? AND id = ?", (content,rid, rett_id))
  con.commit()
  return "success", 200



# Starter applikasjonen på port 5010
if __name__ == "__main__":
  app.run(debug=True, port=5010)
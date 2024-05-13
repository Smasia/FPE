from flask import Flask, request
from flask_cors import CORS
import sqlite3

# Sette opp applikasjonen
app = Flask(__name__)
CORS(app)

# Sette opp kobling og peker til database
con = sqlite3.connect('database.db', check_same_thread=False)
cur = con.cursor()

# Lager tabell for brukere
cur.execute("""CREATE TABLE IF NOT EXISTS brukere(
            id integer primary key NOT NULL,
            navn text NOT NULL,
            passord text NOT NULL
            )""")
con.commit()

# Lage tabell over ulike retter til alle restauranter med hvilke restaurant de hører til bestemt av restaurant_meny
cur.execute("""CREATE TABLE IF NOT EXISTS meny_retter(
            matrett_id integer primary key NOT NULL,
            restaurant_meny text,
            bilde blob,
            beskrivelse text
            )""")
con.commit()

# Lager brukere og legger de til i bruker tabellen, fjerner også tidligere brukere for å unngå kopier
brukere = ["RES1", "RES2", "RES3", "Kunde"]
cur.execute("DELETE FROM brukere")
con.commit()
cur.executemany("INSERT INTO brukere(navn, passord) VALUES(?,Passord1)", (bruker for bruker in brukere))
con.commit()

# Midlertidig rute for å teste koblingen mellom klient og server
@app.route('/index', methods = ["GET"])
def index():
  return {"text": "Hello World!"}


# Starter applikasjonen på port 5010
if __name__ == "__main__":
  app.run(debug=True, port=5010)
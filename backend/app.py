from flask import Flask, request
from flask_cors import CORS
import sqlite3

# Sette opp applikasjonen
app = Flask(__name__)
CORS(app)

# Sette opp kobling og peker til database
con = sqlite3.connect('database.db', check_same_thread=False)
cur = con.cursor()

# Midlertidig rute for å teste koblingen mellom klient og server
@app.route('/index', methods = ["GET"])
def index():
  return {"text": "Hello World!"}


# Starter applikasjonen på port 5010
if __name__ == "__main__":
  app.run(debug=True, port=5010)
from flask import Flask, render_template, request, redirect
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


# Starter applikasjonen på port 5000
if __name__ == "__main__":
  app.run(debug=True, port=5000)
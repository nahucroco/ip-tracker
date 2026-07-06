from flask import Flask, request
from datetime import datetime
import json
import requests
from flask_sqlalchemy import SQLAlchemy
import os

URL_APPS_SCRIPT = "https://script.google.com/macros/s/AKfycbzbF6FkoiQn_NRM4z65D3w-cXkOYvl7EHmmcM76RoTIbkCvXrd7S-zypseSo26saIzb/exec"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Visita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(50))
    ip = db.Column(db.String(50))
    user_agent = db.Column(db.Text)

with app.app_context():
    db.create_all()

@app.route("/")
def inicio():

    ip = request.headers.get(
        "X-Forwarded-For",
        request.remote_addr
    )

    if "," in ip:
        ip = ip.split(",")[0].strip()

    visita = Visita(
        fecha=datetime.now().isoformat(),
        ip=ip,
        user_agent=request.headers.get("User-Agent")
    )
    
    db.session.add(visita)
    db.session.commit()

    return """
    <h2>Conexión realizada correctamente.</h2>
    <p>Puedes cerrar esta página.</p>
    """

if __name__ == "__main__":
    app.run(debug=True)
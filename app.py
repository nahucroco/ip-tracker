from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from flask import jsonify

app = Flask(__name__)

database_url = os.getenv("DATABASE_URL")

# Render entrega una URL que empieza con postgres://
# SQLAlchemy espera postgresql://
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Visita(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    fecha = db.Column(db.String(50), nullable=False)

    ip = db.Column(db.String(100), nullable=False)

    pais = db.Column(db.String(100))
    provincia = db.Column(db.String(100))
    ciudad = db.Column(db.String(100))

    latitud = db.Column(db.Float)
    longitud = db.Column(db.Float)

    isp = db.Column(db.String(200))
    organizacion = db.Column(db.String(200))
    asn = db.Column(db.Integer)

    timezone = db.Column(db.String(100))

    user_agent = db.Column(db.Text)


with app.app_context():
    db.create_all()


@app.route("/")
def inicio():

    forwarded_for = request.headers.get("X-Forwarded-For")

    if forwarded_for:
        ip = forwarded_for.split(",")[0].strip()
    else:
        ip = request.remote_addr

    import requests

    geo = {}

    try:

        respuesta = requests.get(f"https://ipwho.is/{ip}", timeout=5)

        geo = respuesta.json()

    except Exception:

        geo = {}

    visita = Visita(
        fecha=datetime.now().isoformat(),
        ip=ip,
        pais=geo.get("country"),
        provincia=geo.get("region"),
        ciudad=geo.get("city"),
        latitud=geo.get("latitude"),
        longitud=geo.get("longitude"),
        timezone=geo.get("timezone", {}).get("id"),
        isp=geo.get("connection", {}).get("isp"),
        organizacion=geo.get("connection", {}).get("org"),
        asn=geo.get("connection", {}).get("asn"),
        user_agent=request.headers.get("User-Agent"),
    )

    db.session.add(visita)
    db.session.commit()

    return """
    <h2>Conexión realizada correctamente.</h2>
    <p>Puedes cerrar esta página.</p>
    """


@app.route("/visitas")
def visitas():

    registros = Visita.query.order_by(Visita.id.desc()).all()

    return jsonify(
        [
            {
                "fecha": r.fecha,
                "ip": r.ip,
                "pais": r.pais,
                "provincia": r.provincia,
                "ciudad": r.ciudad,
                "latitud": r.latitud,
                "longitud": r.longitud,
                "timezone": r.timezone,
                "isp": r.isp,
                "organizacion": r.organizacion,
                "asn": r.asn,
                "user_agent": r.user_agent,
            }
            for r in registros
        ]
    )


if __name__ == "__main__":
    app.run(debug=True)

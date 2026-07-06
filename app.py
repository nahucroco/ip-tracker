from flask import Flask, request
from datetime import datetime
import json

app = Flask(__name__)

ARCHIVO = "visitas.jsonl"

@app.route("/")
def inicio():

    ip = request.headers.get(
        "X-Forwarded-For",
        request.remote_addr
    )

    if "," in ip:
        ip = ip.split(",")[0].strip()

    visita = {
        "fecha": datetime.now().isoformat(),
        "ip": ip,
        "user_agent": request.headers.get("User-Agent")
    }

    with open(ARCHIVO, "a", encoding="utf8") as f:
        f.write(json.dumps(visita) + "\n")

    return """
    <h2>Conexión realizada correctamente.</h2>
    <p>Puedes cerrar esta página.</p>
    """

if __name__ == "__main__":
    app.run(debug=True)
import requests

url = "https://script.google.com/macros/s/AKfycbzbF6FkoiQn_NRM4z65D3w-cXkOYvl7EHmmcM76RoTIbkCvXrd7S-zypseSo26saIzb/exec"

datos = {
    "fecha": "2026-07-06",
    "ip": "1.2.3.4",
    "user_agent": "Prueba"
}

r = requests.post(url, json=datos)

print(r.status_code)
print(r.text)
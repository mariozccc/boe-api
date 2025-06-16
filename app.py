from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

normas = {
    "lsc": "BOE-A-2010-10544",
    "cc": "BOE-A-1889-4763",
    "ccom": "BOE-A-1885-6627"
}

@app.route('/boe/articulo', methods=['GET'])
def get_articulo():
    norma = request.args.get('norma')
    articulo = request.args.get('articulo')

    boe_id = normas.get(norma.lower())
    if not boe_id:
        return jsonify({"error": "Norma no reconocida"}), 400

    url = f"https://www.boe.es/buscar/act.php?id={boe_id}&articulo={articulo}&tipo=doc"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    texto = soup.find('div', class_='texto_articulo')

    if texto:
        return jsonify({
            "norma": norma,
            "articulo": articulo,
            "contenido": texto.get_text(strip=True)
        })
    else:
        return jsonify({"error": "Artículo no encontrado"}), 404

@app.route('/')
def index():
    return "API del BOE funcionando"

if __name__ == '__main__':
    app.run()

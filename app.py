from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

# Diccionario con identificadores del BOE
normas = {
    "lsc": "BOE-A-2010-10544",   # Ley de Sociedades de Capital
    "cc": "BOE-A-1889-4763",     # Código Civil
    "ccom": "BOE-A-1885-6627"    # Código de Comercio
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
    
    dispo = soup.find('div', class_='disposicion')

    if dispo:
        texto = dispo.get_text(separator="\n").strip()
        if articulo.lower() in texto.lower():
            return jsonify({
                "norma": norma,
                "articulo": articulo,
                "contenido": texto
            })
        else:
            return jsonify({"error": "Artículo no encontrado en disposición"}), 404
    else:
        return jsonify({"error": "Contenido no disponible"}), 404

@app.route('/')
def index():
    return "API del BOE funcionando"

# Configuración para entorno Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

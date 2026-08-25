from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import json
import os
import sys


# CHEMINS
# Dossier principal du projet FakeNewsDetector
if getattr(sys, "frozen", False):
    # Application lancée depuis l'exécutable PyInstaller
    BASE_DIR = sys._MEIPASS
else:
    # Application lancée normalement avec Python
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

BACKEND_DIR = os.path.join(BASE_DIR, "backend")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend", "dist")


# FLASK
app = Flask(
    __name__,
    static_folder=FRONTEND_DIR,
    static_url_path=""
)


# CORS
# Adresse du frontend React
FRONTEND_ORIGIN = os.environ.get(
    "FRONTEND_ORIGIN",
    "http://localhost:5173"
)

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                FRONTEND_ORIGIN,
                "https://fakenewsdetector-frontend-wajf.onrender.com"
            ]
        }
    },
    methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"]
)


# LABELS
labels = {
    0: "true statement",
    1: "false statement"
}


# CHARGEMENT DU MODÈLE
model_path = os.path.join(
    BACKEND_DIR,
    "fake_news_model.keras"
)

model = tf.keras.models.load_model(model_path)

print(
    ">>>>>>>>>> Modèle Keras chargé",
    flush=True
)


# CHARGEMENT DU VOCABULAIRE
vocab_path = os.path.join(
    BACKEND_DIR,
    "vocab.json"
)

with open(
    vocab_path,
    "r",
    encoding="utf-8"
) as f:
    vocab = json.load(f)

print(
    ">>>>>>>>>> Vocabulaire chargé",
    flush=True
)


# VECTORISATION
vectorizer = tf.keras.layers.TextVectorization(
    max_tokens=10000,
    output_sequence_length=30
)

vectorizer.set_vocabulary(vocab)

print(
    ">>>>>>>>>> Vectorizer chargé",
    flush=True
)


# API DE PRÉDICTION
@app.route("/api/predict", methods=["POST"])
def predict():

    # Récupération des données envoyées par React
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({
            "error": "Données JSON invalides."
        }), 400

    # Récupération du texte
    texte = data.get("texte", "").strip()

    if not texte:
        return jsonify({
            "error": "Le texte est vide."
        }), 400

    print(
        ">>>>>>>>>> Texte reçu :",
        texte,
        flush=True
    )

    # Transformation du texte en séquence
    sequence = vectorizer([texte])

    # Prédiction avec le Bi-LSTM
    prediction = model.predict(
        sequence,
        verbose=0
    )

    print(
        ">>>>>>>>>> Prédiction :",
        prediction,
        flush=True
    )

    # Classe gagnante
    classe = int(
        np.argmax(prediction[0])
    )

    # Confiance
    confiance = float(
        prediction[0][classe]
    )

    print(
        ">>>>>>>>>> Confiance :",
        confiance,
        flush=True
    )

    # Résultat
    resultat = labels[classe]

    print(
        ">>>>>>>>>> Résultat :",
        resultat,
        flush=True
    )

    # Réponse envoyée au frontend
    return jsonify({
        "prediction": resultat,
        "confidence": confiance
    })


# REACT
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):

    file_path = os.path.join(
        app.static_folder,
        path
    )

    if path and os.path.exists(file_path):
        return send_from_directory(
            app.static_folder,
            path
        )

    # Retourne index.html pour React
    index_path = os.path.join(
        app.static_folder,
        "index.html"
    )

    if os.path.exists(index_path):
        return send_from_directory(
            app.static_folder,
            "index.html"
        )

    return jsonify({
        "message": "FakeNewsDetector API fonctionne"
    })


# LANCEMENT LOCAL
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import json
import os
import sys

# CHEMINS
# Dossier du projet FakeNewsDetector
if getattr(sys, "frozen", False):
    PROJECT_DIR = sys._MEIPASS
else:
    PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BACKEND_DIR = os.path.join(PROJECT_DIR, "backend")
FRONTEND_DIR = os.path.join(PROJECT_DIR, "frontend", "dist")


# FLASK
app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(
    app,
    resources={r"/api/*": {"origins": "*"}},
    methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"]
)

# LABELS
labels = {0: "true statement", 1: "false statement"}

# CHARGEMENT DU MODÈLE
model_path = os.path.join(BACKEND_DIR, "fake_news_model.keras")
model = tf.keras.models.load_model(model_path)
print(">>>>>>>>>> Modèle Keras chargé")  # todebug

# CHARGEMENT DU VOCABULAIRE
vocab_path = os.path.join(BACKEND_DIR, "vocab.json")
with open(vocab_path, "r", encoding="utf-8") as f:
    vocab = json.load(f)
print(">>>>>>>>>> Vocabulaire chargé")  # todebug

# VECTORISER
vectorizer = tf.keras.layers.TextVectorization(max_tokens=10000, output_sequence_length=30)
vectorizer.set_vocabulary(vocab)
print(">>>>>>>>>> Vectorizer chargé")  # todebug


# API DE PRÉDICTION
@app.route("/api/predict", methods=["POST"])
# def predict():
#     # Récupération des données envoyées par React
#     data = request.get_json()

#     # Récupération du texte
#     texte = data.get("texte", "")

#     # Transformation du texte en séquence
#     sequence = vectorizer([texte])

#     # Prédiction avec le Bi-LSTM
#     prediction = model.predict(sequence,verbose=0)
#     print("Prédiction :", prediction)  # todebug

#     # Classe gagnante
#     classe = int(np.argmax(prediction[0]))

#     # Confiance
#     confiance = float(prediction[0][classe])
#     print("Confiance :", confiance)  # todebug

#     # Résultat
#     resultat = labels[classe]
#     print("Résultat :", resultat)

#     return jsonify({
#         "prediction": resultat,
#         "confidence": confiance
#     })

@app.route("/api/predict", methods=["POST"])
def predict():
    print("========== DEBUT PREDICTION ==========", flush=True)

    try:
        # 1. Récupération du JSON
        data = request.get_json(silent=True)
        print("DATA :", data, flush=True)

        if data is None:
            return jsonify({
                "error": "JSON invalide"
            }), 400

        # 2. Récupération du texte
        texte = data.get("texte", "")

        print("TEXTE :", texte, flush=True)

        if not isinstance(texte, str) or not texte.strip():
            return jsonify({
                "error": "Texte vide ou invalide"
            }), 400

        # 3. Vectorisation
        print("Début vectorisation...", flush=True)

        sequence = vectorizer([texte])

        print("Vectorisation terminée", flush=True)
        print("Shape :", sequence.shape, flush=True)

        # 4. Prédiction
        print("Début prédiction TensorFlow...", flush=True)

        prediction = model.predict(
            sequence,
            verbose=0
        )

        print("Prédiction terminée :", prediction, flush=True)

        # 5. Classe
        classe = int(np.argmax(prediction[0]))

        print("Classe :", classe, flush=True)

        # 6. Confiance
        confiance = float(prediction[0][classe])

        print("Confiance :", confiance, flush=True)

        # 7. Résultat
        resultat = labels[classe]

        print("Résultat :", resultat, flush=True)
        print("========== FIN PREDICTION ==========", flush=True)

        return jsonify({
            "prediction": resultat,
            "confidence": confiance
        })

    except Exception as e:
        print("========== ERREUR PREDICTION ==========", flush=True)
        print(type(e).__name__, flush=True)
        print(str(e), flush=True)

        return jsonify({
            "error": str(e)
        }), 500



# REACT
@app.route("/")
def index():
    return send_from_directory(app.static_folder,"index.html")


@app.route("/<path:path>")
def serve_react(path):
    file_path = os.path.join(app.static_folder,path)
    if os.path.exists(file_path):
        return send_from_directory(app.static_folder,path)
    return send_from_directory(app.static_folder,"index.html")


# LANCEMENT
if __name__ == "__main__":
    # app.run(host="127.0.0.1",port=5000, debug=False)
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
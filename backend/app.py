# from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS
# import tensorflow as tf
# import numpy as np
# import json
# import os
# import sys

# # CHEMINS
# # Dossier du projet FakeNewsDetector
# if getattr(sys, "frozen", False):
#     PROJECT_DIR = sys._MEIPASS
# else:
#     PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# BACKEND_DIR = os.path.join(PROJECT_DIR, "backend")
# FRONTEND_DIR = os.path.join(PROJECT_DIR, "frontend", "dist")


# # FLASK
# app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
# CORS(
#     app,
#     resources={r"/api/*": {"origins": "*"}},
#     methods=["GET", "POST", "OPTIONS"],
#     allow_headers=["Content-Type"]
# )

# # LABELS
# labels = {0: "true statement", 1: "false statement"}

# # CHARGEMENT DU MODÈLE
# model_path = os.path.join(BACKEND_DIR, "fake_news_model.keras")
# model = tf.keras.models.load_model(model_path)
# print(">>>>>>>>>> Modèle Keras chargé")  # todebug

# # CHARGEMENT DU VOCABULAIRE
# vocab_path = os.path.join(BACKEND_DIR, "vocab.json")
# with open(vocab_path, "r", encoding="utf-8") as f:
#     vocab = json.load(f)
# print(">>>>>>>>>> Vocabulaire chargé")  # todebug

# # VECTORISER
# vectorizer = tf.keras.layers.TextVectorization(max_tokens=10000, output_sequence_length=30)
# vectorizer.set_vocabulary(vocab)
# print(">>>>>>>>>> Vectorizer chargé")  # todebug


# # API DE PRÉDICTION
# @app.route("/api/predict", methods=["POST"])
# # def predict():
# #     # Récupération des données envoyées par React
# #     data = request.get_json()

# #     # Récupération du texte
# #     texte = data.get("texte", "")

# #     # Transformation du texte en séquence
# #     sequence = vectorizer([texte])

# #     # Prédiction avec le Bi-LSTM
# #     prediction = model.predict(sequence,verbose=0)
# #     print("Prédiction :", prediction)  # todebug

# #     # Classe gagnante
# #     classe = int(np.argmax(prediction[0]))

# #     # Confiance
# #     confiance = float(prediction[0][classe])
# #     print("Confiance :", confiance)  # todebug

# #     # Résultat
# #     resultat = labels[classe]
# #     print("Résultat :", resultat)

# #     return jsonify({
# #         "prediction": resultat,
# #         "confidence": confiance
# #     })

# @app.route("/api/predict", methods=["POST"])
# def predict():
#     print("========== TEST API ==========", flush=True)

#     data = request.get_json(silent=True)

#     print("DATA :", data, flush=True)

#     return jsonify({
#         "prediction": "true statement",
#         "confidence": 0.99
#     })



# # REACT
# @app.route("/")
# def index():
#     return send_from_directory(app.static_folder,"index.html")


# @app.route("/<path:path>")
# def serve_react(path):
#     file_path = os.path.join(app.static_folder,path)
#     if os.path.exists(file_path):
#         return send_from_directory(app.static_folder,path)
#     return send_from_directory(app.static_folder,"index.html")


# # LANCEMENT
# if __name__ == "__main__":
#     # app.run(host="127.0.0.1",port=5000, debug=False)
#     app.run(
#         host="0.0.0.0",
#         port=int(os.environ.get("PORT", 5000)),
#         debug=False
#     )

# __________________________________________________________________


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

app = Flask(__name__)

# Autoriser le frontend Render
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "https://fakenewsdetector-frontend-wajf.onrender.com"
            ]
        }
    }
)

# dictionnaire label binaire -> texte.
labels = {
    0: "true statement",
    1: "false statement"
}

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


@app.route("/api/predict", methods=["POST"])
def predict():
    print("========== TEST API ==========", flush=True)
    data = request.get_json(silent=True)
    print("DATA :", data, flush=True)
    return jsonify({
        "prediction": "true statement",
        "confidence": 0.99
    })


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "FakeNewsDetector API fonctionne"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
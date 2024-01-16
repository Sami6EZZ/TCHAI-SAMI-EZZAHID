from flask import Flask, Blueprint, request, jsonify
import sqlite3
import hashlib
from datetime import datetime

route_verificateur = Blueprint("F_verification", __name__)

def calculer_hash(expediteur, recepteur, date, montant):
    # Concaténer les informations de la transaction
    hash_input = f"{expediteur}_{recepteur}_{date}_{montant}".encode('utf-8')

    # Utiliser l'algorithme SHA-256 pour calculer le hash
    sha256 = hashlib.sha256()
    sha256.update(hash_input)
    return sha256.hexdigest()

@route_verificateur.route('/verifier_transactions', methods=['GET'])
def verifier_transactions():
    try:
        conn = sqlite3.connect('tchai.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM transactions')
        transactions = cursor.fetchall()

        transactions_frauduleuses = []

        for transaction in transactions:
            # Extraire les informations de la transaction
            hash_enregistre, expediteur, recepteur, date, montant = transaction
            # Utiliser format() pour formater la valeur avec deux chiffres après la virgule (round(montant, 2)
            montant = "{:.2f}".format(montant)

            # Calculer le hash des informations actuelles
            hash_calculé = calculer_hash(expediteur, recepteur, date, montant)

            # Vérifier si le hash enregistré correspond au hash calculé
            if hash_calculé != hash_enregistre:
                transactions_frauduleuses.append({
                    "expediteur": expediteur,
                    "recepteur": recepteur,
                    "date": date,
                    "montant": montant
                })

        conn.close()

        return jsonify({"transactions_frauduleuses": transactions_frauduleuses})

    except Exception as e:
        print(f"Erreur lors de la vérification des transactions : {e}")
        return jsonify({"transactions_frauduleuses": []})

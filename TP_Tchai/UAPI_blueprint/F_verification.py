from flask import Flask, Blueprint, request, jsonify
import sqlite3
import hashlib
from datetime import datetime
import uuid

route_verificateur = Blueprint("F_verification", __name__)

def calculer_hash(cursor, iteration, expediteur, recepteur, temps, montant):
    # Concaténer les informations de la transaction
    # Récupérez le hash de l'avant-dernière transaction en utilisant l'offset dynamique
    cursor.execute(f'SELECT hash FROM transactions ORDER BY date_heure ASC LIMIT 1 OFFSET {iteration}')
    avant_dernier_hash = cursor.fetchone()
    avant_dernier_hash = avant_dernier_hash[0] if avant_dernier_hash else str(uuid.uuid4())  # Utilisez un UUID si c'est la première transaction

    # Concaténez le hash précédent avec les autres données de la transaction
    hash_input = f"{avant_dernier_hash}_{expediteur}_{recepteur}_{temps}_{montant}".encode('utf-8')
    print(hash_input)

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
        
        i=0
        for transaction in transactions[1:]:
            # Extraire les informations de la transaction
            hash_enregistre, expediteur, recepteur, date, montant = transaction
            # Utiliser format() pour formater la valeur avec deux chiffres après la virgule (round(montant, 2)
            montant = "{:.2f}".format(montant)

            # fonction qui retourne le Calcule du hash des informations actuelles
            hash_calculé = calculer_hash(cursor,i,expediteur, recepteur, date, montant)
            i+=1

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

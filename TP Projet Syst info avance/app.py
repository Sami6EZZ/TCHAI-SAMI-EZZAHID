import os
from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
from flask_bcrypt import Bcrypt

from SQLite_bdd import creer_base_de_donnees
from UAPI_blueprint.F_pages_web import navigation
from UAPI_blueprint.F_inscription import route_inscription
from UAPI_blueprint.F_connexion import route_connexion



app = Flask(__name__)

creer_base_de_donnees()

# Récupérer la clé secrète à partir de la variable d'environnement MY_SECRET_KEY
CLE_ID = os.environ.get("CLE_ID", "CLE_ID")

# Vérifier si la clé secrète est définie
if CLE_ID is None:
    raise ValueError("La clé secrète n'est pas définie dans les variables d'environnement.")

# Enregistrer la clé secrète dans l'objet app.config
app.config['CLE_ID'] = CLE_ID
app.secret_key = CLE_ID

transactions = []

# Les routes Flask de l'application
app.register_blueprint(navigation)

app.register_blueprint(route_inscription)

app.register_blueprint(route_connexion)


# (A1) Enregistrer une transaction
@app.route('/enregistrer_transaction', methods=['POST'])
def enregistrer_transaction():
    data = request.get_json()
    sender = data['sender']
    receiver = data['receiver']
    amount = data['amount']

    conn = sqlite3.connect('tchai.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (sender, receiver, amount)
        VALUES (?, ?, ?)
    ''', (sender, receiver, amount))
    conn.commit()
    conn.close()

    return jsonify({"message": "Transaction enregistrée avec succès"}), 201

# (A2) Afficher une liste de toutes les transactions dans l’ordre chronologique
@app.route('/toutes_transactions', methods=['GET'])
def toutes_transactions():
    conn = sqlite3.connect('tchai.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM transactions
        ORDER BY timestamp
    ''')
    transactions = cursor.fetchall()
    conn.close()

    return jsonify({"transactions": transactions})

# (A3) Afficher une liste des transactions dans l’ordre chronologique liées à une personne donnée
@app.route('/transactions_personne/<personne>', methods=['GET'])
def transactions_personne(personne):
    conn = sqlite3.connect('tchai.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM transactions
        WHERE sender = ? OR receiver = ?
        ORDER BY timestamp
    ''', (personne, personne))
    transactions = cursor.fetchall()
    conn.close()

    return jsonify({"transactions": transactions})

# (A4) Afficher le solde du compte de la personne donnée
@app.route('/solde/<personne>', methods=['GET'])
def solde_personne(personne):
    conn = sqlite3.connect('tchai.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT (SUM(amount) FILTER (WHERE sender = ?) - SUM(amount) FILTER (WHERE receiver = ?)) AS solde
        FROM transactions
    ''', (personne, personne))
    solde = cursor.fetchone()[0]
    conn.close()

    return jsonify({"solde": solde})



# ... (autres configurations Flask)





if __name__ == '__main__':
    app.run(debug=True)


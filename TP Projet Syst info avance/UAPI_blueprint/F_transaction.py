from flask import Flask,Blueprint, request, jsonify, session
import sqlite3
from datetime import datetime



route_transaction = Blueprint("F_transaction", __name__)


    
# Enregistrer un nouvel utilisateur
@route_transaction.route('/enregistrer_transaction', methods=['POST'])
def enregistrer_utilisateur():
    data = request.get_json()

    expediteur = data.get('expediteur')
    recepteur = data.get('recepteur')
    montant = data.get('montant')
    temps = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   
    try:
        # Connectez-vous à la base de données SQLite
        conn = sqlite3.connect('tchai.db')
        cursor = conn.cursor()
    # Vérifiez si l'expéditeur existe dans la table des utilisateurs
        cursor.execute('SELECT solde FROM utilisateurs WHERE nom = ?', (expediteur,))
        expediteur_solde = cursor.fetchone()

        # Vérifiez si le récepteur existe dans la table des utilisateurs
        cursor.execute('SELECT solde FROM utilisateurs WHERE nom = ?', (recepteur,))
        recepteur_solde = cursor.fetchone()

        # Si l'expéditeur ou le récepteur n'existe pas, renvoyez une erreur
        if expediteur_solde is None or recepteur_solde is None:
            return jsonify({"success": False, "erreur": "L'expéditeur ou le récepteur n'existe pas"}), 400

        # Soustraire le montant du solde de l'expéditeur
        cursor.execute('''
            UPDATE utilisateurs
            SET solde = solde - ?
            WHERE nom = ?
        ''', (montant, expediteur))

        # Ajouter le montant au solde du récepteur
        cursor.execute('''
            UPDATE utilisateurs
            SET solde = solde + ?
            WHERE nom = ?
        ''', (montant, recepteur))

        # Insérez la nouvelle transaction dans la base de données
        cursor.execute('''
            INSERT INTO transactions (expediteur, recepteur, date_heure, montant)
            VALUES (?, ?, ?, ?)
        ''', (expediteur, recepteur, temps, montant))

        # Validez la transaction dans la base de données
        conn.commit()
        conn.close()

         # Retournez une réponse indiquant le succès de l'opération
        return jsonify({"success": True}), 201
    except Exception as e:
        # Gérez les erreurs, par exemple en renvoyant une réponse d'erreur appropriée
        print(f"Erreur lors de l'enregistrement de la transaction : {e}")
        return jsonify({"success": False, "erreur": str(e)}), 500
        
    
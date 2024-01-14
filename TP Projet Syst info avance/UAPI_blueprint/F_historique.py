from flask import Flask, jsonify, Blueprint
import sqlite3


route_historique = Blueprint("F_historique", __name__)


    
@route_historique.route('/charger_transactions', methods=['GET'])
def charger_transactions():
    try:
        conn = sqlite3.connect('tchai.db')
        cursor = conn.cursor()

        cursor.execute('SELECT date_heure, expediteur, recepteur, montant FROM transactions ORDER BY date_heure DESC')
        transactions = [{'date_heure': row[0],'expediteur' : row[1], 'recepteur' : row[2], 'montant': row[3]} for row in cursor.fetchall()]

        conn.close()

        return jsonify({"transactions": transactions})
    except Exception as e:
            # Gérez les erreurs, par exemple en renvoyant une réponse d'erreur appropriée
            print(f"Erreur lors de la récupération de l'historique : {e}")


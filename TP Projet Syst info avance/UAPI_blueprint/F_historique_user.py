from flask import Flask, jsonify, request, Blueprint
import sqlite3

route_filtre = Blueprint("F_histirique_user", __name__)

@route_filtre.route('/verifier_utilisateur', methods=['GET'])
def verifier_utilisateur():
    utilisateur = request.args.get('utilisateur', '').strip().lower()
    
    try:
        conn = sqlite3.connect('tchai.db')
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM utilisateurs WHERE nom = ?', (utilisateur,))
        utilisateur_existe = cursor.fetchone()[0] > 0

        conn.close()

        return jsonify({"utilisateurExiste": utilisateur_existe})

    except Exception as e:
        print(f"Erreur lors de la vérification de l'utilisateur : {e}")
        return jsonify({"utilisateurExiste": False})

@route_filtre.route('/charger_transactions_utilisateur', methods=['GET'])
def charger_transactions_utilisateur():
    utilisateur = request.args.get('utilisateur', '').strip().lower()

    try:
        conn = sqlite3.connect('tchai.db')
        cursor = conn.cursor()

        cursor.execute('SELECT date_heure, expediteur, recepteur, montant FROM transactions WHERE expediteur = ? OR recepteur = ? ORDER BY date_heure DESC', (utilisateur, utilisateur))
        transactions = [{'date_heure': row[0], 'expediteur': row[1], 'recepteur': row[2], 'montant': row[3]} for row in cursor.fetchall()]

        conn.close()

        return jsonify({"transactions": transactions})

    except Exception as e:
        print(f"Erreur lors du chargement des transactions pour l'utilisateur : {e}")
        return jsonify({"transactions": []})

from flask import Flask,Blueprint, request, jsonify, session
import sqlite3



route_inscription = Blueprint("F_inscription", __name__)


    
# Enregistrer un nouvel utilisateur
@route_inscription.route('/inscription', methods=['POST'])
def enregistrer_utilisateur():
    data = request.get_json()

    nom_utilisateur = data.get('nom_utilisateur')
    mdp = data.get('mot_de_passe')

   
    try:
        # Connectez-vous à la base de données SQLite
        conn = sqlite3.connect('tchai.db')
        cursor = conn.cursor()

        # Insérez le nouvel utilisateur dans la base de données
        cursor.execute('''
            INSERT INTO utilisateurs (nom, password)
            VALUES (?, ?)
        ''', (nom_utilisateur, mdp))

        # Validez la transaction dans la base de données
        conn.commit()
        conn.close()

        return jsonify({"message": f"{nom_utilisateur}"}), 201
    except Exception as e:
        # Gérez les erreurs, par exemple en renvoyant une réponse d'erreur appropriée
        print(f"Erreur lors de l'enregistrement de l'utilisateur : {e}")
        return jsonify({"erreur": str(e)}), 500
from flask import Flask, Blueprint, request, jsonify, session
import sqlite3

route_connexion = Blueprint("F_connexion", __name__)

# Connexion de l'utilisateur
@route_connexion.route('/connexion', methods=['POST'])
def connexion_utilisateur():
    data = request.get_json()

    username = data.get('username')
    password = data.get('mdp')

    try:
        # Connectez-vous à la base de données SQLite
        conn = sqlite3.connect('tchai.db')
        cursor = conn.cursor()

        # Vérifiez si le nom d'utilisateur et le mot de passe correspondent dans la base de données
        cursor.execute('SELECT * FROM utilisateurs WHERE nom = ? AND password = ?', (username, password))
        utilisateur = cursor.fetchone()

        # Fermez la connexion à la base de données
        conn.close()

        if utilisateur:
            # Connexion réussie, vous pouvez stocker l'ID utilisateur dans la session si nécessaire
            session['utilisateur'] = utilisateur[0]
            return jsonify({"message": "Connexion réussie"}), 200
        else:
            print(f"Erreur lors de la connexion")
            return jsonify({"error": "Nom d'utilisateur ou mot de passe incorrect"}), 401
    except Exception as e:
        # Gérez les erreurs, par exemple en renvoyant une réponse d'erreur appropriée
        print(f"Erreur lors de la connexion de l'utilisateur : {e}")
        return jsonify({"erreur": str(e)}), 500

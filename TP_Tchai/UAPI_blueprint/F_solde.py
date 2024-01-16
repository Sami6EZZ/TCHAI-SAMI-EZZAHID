from flask import Flask, jsonify, render_template,request,  Blueprint
import sqlite3


route_solde = Blueprint("F_solde", __name__ )

@route_solde.route('/recuperer_solde', methods=['POST'])
def solde():
    data = request.get_json()

    expediteur = data.get('expediteur')
    try:
        conn = sqlite3.connect('tchai.db')
        cursor = conn.cursor()

        cursor.execute('SELECT solde FROM utilisateurs WHERE nom = ?', (expediteur,))
        solde = cursor.fetchone()[0]


        conn.close()

        return jsonify({"solde": solde})

    except Exception as e:
        print(f"Erreur lors de la récupération du solde : {e}")
        return jsonify({"solde": 404.404})
import sqlite3

def creer_base_de_donnees():
    conn = sqlite3.connect('tchai.db')
    cursor = conn.cursor()

    # Création de la table des utilisateurs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS utilisateurs (
            nom  TEXT UNIQUE PRIMARY KEY NOT NULL,
            password TEXT NOT NULL,
            solde REAL DEFAULT 0.00
        )
    ''')

    # Création de la table des transactions (on défini le montant avec decimal et non pas real ôur éviter la suppréssion des zéros après la virgule)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            hash TEXT NOT NULL PRIMARY KEY ,
            expediteur TEXT NOT NULL,
            recepteur TEXT NOT NULL,
            date_heure DATETIME NOT NULL,
            montant FLOAT NOT NULL
        )
    ''')
    # Enregistrement
    conn.commit()
    conn.close()

creer_base_de_donnees()
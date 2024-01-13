import sqlite3

def creer_base_de_donnees():
    conn = sqlite3.connect('tchai.db')
    cursor = conn.cursor()

    # Création de la table des utilisateurs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS utilisateurs (
            nom  TEXT UNIQUE PRIMARY KEY NOT NULL,
            password TEXT NOT NULL,
            solde REAL DEFAULT 0.0
        )
    ''')

    # Création de la table des transactions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expediteur TEXT NOT NULL,
            recepteur TEXT NOT NULL,
            date_heure DATETIME NOT NULL,
            montant REAL NOT NULL
        )
    ''')

    # N'oubliez pas de valider les changements dans la base de données
    conn.commit()
    conn.close()

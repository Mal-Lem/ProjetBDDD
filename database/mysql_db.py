import mysql.connector

class MySQLDatabase:
    def __init__(self):
      try:
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1111",
            database="library_db"
        )
        self.cursor = self.connection.cursor()
        print("Connexion à la base de données MySQL réussie.")
        print("Type de self.connection:", type(self.connection))
        print("Contenu de self.connection:", self.connection)
      except Exception as e:
        print("Erreur lors de la connexion à la base de données MySQL :", str(e))


    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS livres (
                id INT AUTO_INCREMENT PRIMARY KEY,
                titre VARCHAR(255),
                auteur VARCHAR(255),
                isbn VARCHAR(20)
            )
        """)
    def check_table_existence(self):
        self.cursor.execute("SHOW TABLES LIKE 'livres'")
        result = self.cursor.fetchone()
        if result:
            print("La table 'livres' existe dans la base de données MySQL.")
        else:
            print("La table 'livres' n'existe pas dans la base de données MySQL.")
    
    
    def insert_data(self, title, author, isbn):
        livre_data = (title, author, isbn)
        self.cursor.execute("""
        INSERT INTO livres (titre, auteur, isbn) VALUES (%s, %s, %s)
        """, livre_data)
        self.connection.commit()

    def fetch_data(self):
        self.cursor.execute("SELECT * FROM livres")
        livres = self.cursor.fetchall()
        if livres:
            return livres  # Retourner les données si elles existent
        else:
            return

    def __del__(self):
        self.cursor.close()
        self.connection.close()

from database.mysql_db import MySQLDatabase
from database.mongo_db import MongoDB

def migrate_data():
    # Récupérer les données à partir de MySQL
    mysql_db = MySQLDatabase()
    mysql_books = mysql_db.fetch_data()

    # Insérer les données dans MongoDB
    mongo_db = MongoDB()
    for book in mysql_books:
        # Insérer les données en tant que document MongoDB avec une critique vide
        mongo_db.insert_data({"titre": book[1], "auteur": book[2], "isbn": book[3], "critique": "", "pdf_content": None})

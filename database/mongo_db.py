from pymongo import MongoClient

class MongoDB:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client['library_db']
        self.collection = self.db['livres_extra']
        
    def check_collection_existence(self):
        collections = self.db.list_collection_names()
        if "livres_extra" in collections:
            print("La collection 'livres_extra' existe dans la base de données MongoDB.")
        else:
            print("La collection 'livres_extra' n'existe pas dans la base de données MongoDB.")
    
    def insert_data(self, data):
        self.collection.insert_one(data)

    def fetch_data(self):
        livres_extra_data = self.collection.find()
        if livres_extra_data:
          for livre_extra in livres_extra_data:
            print(livre_extra)
        else:
            print("Aucune donnée trouvée dans la collection 'livres_extra'.")


    def __del__(self):
        self.client.close()

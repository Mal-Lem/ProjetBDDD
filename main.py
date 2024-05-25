import tkinter as tk
from tkinter import messagebox, filedialog
from database.mysql_db import MySQLDatabase
from database.mongo_db import MongoDB
import hashlib

# Variables globales pour les champs de saisie
entry_title = None
entry_author = None
entry_isbn = None
entry_critique = None
entry_password = None  # Nouveau champ pour le mot de passe

# Fonction pour afficher l'interface d'insertion de livre
def show_insert_interface():
    global entry_title, entry_author, entry_isbn, entry_critique, entry_password
    insert_window = tk.Toplevel(root)
    insert_window.title("Insertion de livre")
    insert_window.configure(bg="#f0f0f0")

    # Créer les étiquettes et les champs de saisie pour les détails du livre
    label_title = tk.Label(insert_window, text="Titre :", bg="#f0f0f0", font=("Arial", 12))
    label_title.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_title = tk.Entry(insert_window, font=("Arial", 12))
    entry_title.grid(row=0, column=1, padx=10, pady=5)

    label_author = tk.Label(insert_window, text="Auteur :", bg="#f0f0f0", font=("Arial", 12))
    label_author.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_author = tk.Entry(insert_window, font=("Arial", 12))
    entry_author.grid(row=1, column=1, padx=10, pady=5)

    label_isbn = tk.Label(insert_window, text="ISBN :", bg="#f0f0f0", font=("Arial", 12))
    label_isbn.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_isbn = tk.Entry(insert_window, font=("Arial", 12))
    entry_isbn.grid(row=2, column=1, padx=10, pady=5)

    # Champ pour la critique
    label_critique = tk.Label(insert_window, text="Critique :", bg="#f0f0f0", font=("Arial", 12))
    label_critique.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    entry_critique = tk.Entry(insert_window, font=("Arial", 12))
    entry_critique.grid(row=3, column=1, padx=10, pady=5)

    # Champ pour le mot de passe
    label_password = tk.Label(insert_window, text="Mot de passe :", bg="#f0f0f0", font=("Arial", 12))
    label_password.grid(row=4, column=0, padx=10, pady=5, sticky="w")
    entry_password = tk.Entry(insert_window, show="*", font=("Arial", 12))  # Pour masquer le mot de passe
    entry_password.grid(row=4, column=1, padx=10, pady=5)

    # Bouton pour sélectionner un fichier PDF
    select_pdf_button = tk.Button(insert_window, text="Sélectionner un PDF", command=select_pdf)
    select_pdf_button.grid(row=5, columnspan=2, padx=10, pady=10)

    # Étiquette pour afficher le nom du fichier PDF sélectionné
    global pdf_label
    pdf_label = tk.Label(insert_window, text="")
    pdf_label.grid(row=6, columnspan=2, padx=10, pady=5)
    
    # Bouton pour insérer le livre
    insert_button = tk.Button(insert_window, text="Insérer le livre", command=insert_book)
    insert_button.grid(row=7, columnspan=2, padx=10, pady=10)

    # Définir le focus initial sur le champ de titre
    entry_title.focus_set()

# Fonction pour sélectionner un fichier PDF
def select_pdf():
    global pdf_path
    pdf_path = filedialog.askopenfilename(title="Sélectionner PDF")
    if pdf_path:
        pdf_label.config(text="PDF sélectionné : {}".format(pdf_path))

# Fonction pour insérer un livre dans les bases de données MySQL et MongoDB
def insert_book():
    global pdf_path

    # Récupérer les données du formulaire
    title = entry_title.get()
    author = entry_author.get()
    isbn = entry_isbn.get()
    critique = entry_critique.get()
    password = entry_password.get()  # Récupérer le mot de passe

    # Vérifier si les champs sont vides
    if title == '' or author == '' or isbn == '' or critique == '' or password == '':
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
    else:
        try:
            # Hacher le mot de passe avant de l'insérer dans MongoDB
            hashed_password = hash_password(password)

            # Insérer les données dans MySQL
            mysql_db = MySQLDatabase()
            mysql_db.insert_data(title, author, isbn)
            # Insérer les données dans MongoDB avec le chemin du fichier PDF
            mongo_db = MongoDB()
            pdf_content = None
            if pdf_path:
                with open(pdf_path, 'rb') as file:
                    pdf_content = file.read()
            mongo_db.insert_data({"titre": title, "critique": critique, "pdf_content": pdf_content, "hashed_password": hashed_password})

            messagebox.showinfo("Succès", "Livre inséré avec succès dans les deux bases de données.")

            # Effacer les champs après l'insertion
            entry_title.delete(0, tk.END)
            entry_author.delete(0, tk.END)
            entry_isbn.delete(0, tk.END)
            entry_critique.delete(0, tk.END)
            entry_password.delete(0, tk.END)

            # Réinitialiser le chemin du fichier PDF
            pdf_path = None
            pdf_label.config(text="")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

# Fonction pour hacher le mot de passe avec SHA-256
def hash_password(password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    return sha256.hexdigest()

# Créer la fenêtre principale
root = tk.Tk()
root.title("Gestion des livres")

# Bouton pour insérer un livre
insert_button = tk.Button(root, text="Insérer un livre", command=show_insert_interface)
insert_button.pack(pady=10)

# Lancer la boucle principale de l'interface utilisateur
root.mainloop()
"""Classe Bdd
"""

import sqlite3
import datetime

from Ressource.Classe.Ingredient import Ingredient
from Ressource.Classe.Recette import Recette
from Ressource.Classe.Repas import Repas


# Base de données
class Bdd:
    """ Classe liée à la gestion et l'utilisation de la base de données SQLite"""

    # Création des tables
    def init_ingredient(self):
        """Création de la table des ingrédients"""
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredient(
             id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
             nom TEXT,
             unite TEXT,
             lieu TEXT,
             nb REAL,
             commentaire TEXT
        )
        """)
        self.conn.commit()

    def init_recette(self):
        """Création des tables liées a une recette"""
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS recette(
             id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
             titre TEXT,
             url TEXT,
             nb_personne INT,
             difficulte INT,
             recette TEXT,
             note INT,
             temps_prepa INT,
             temps_cuisson INT,
             commentaire TEXT
            )
        """)

        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS recette_ingredients(
             id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
             id_recette INT,
             nom TEXT,
             unite TEXT,
             lieu TEXT,
             nb INT,
             commentaire TEXT
            )
        """)

        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS recette_mot_clef(
             id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
             id_recette INT,
             mot_clef TEXT
            )
        """)
        self.conn.commit()

    def init_repas(self):
        """Création des tables liées a un repas"""
        cursor = self.conn.cursor()
        cursor.execute("""
           CREATE TABLE IF NOT EXISTS repas(
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                date DATE,
                moment TEXT,
                nb_personne INT,
                commentaire TEXT
               )
           """)
        cursor.execute("""
           CREATE TABLE IF NOT EXISTS repas_ingredients(
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                id_repas INT,
                nom TEXT,
                unite TEXT,
                lieu TEXT,
                nb INT,
                commentaire TEXT
               )
           """)
        cursor.execute("""
           CREATE TABLE IF NOT EXISTS repas_recettes(
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                id_repas INT,
                id_recette INT
               )
           """)
        self.conn.commit()

    def supp_table(self):
        """ remplacer le nom de ma table et décommenter l'appel à l'init de la class BDD"""
        # cursor = self.conn.cursor()
        # cursor.execute(""" DROP TABLE IF EXISTS ingredient ;""")
        # cursor.execute(""" DROP TABLE IF EXISTS recette ;""")
        # cursor.execute(""" DROP TABLE IF EXISTS recette_ingredients ;""")
        # cursor.execute(""" DROP TABLE IF EXISTS recette_mot_clef ;""")
        # self.conn.commit()

    def __init__(self):
        self.conn = sqlite3.connect('../../Ressource/BDD/GestionRepas.db')
        # A décommenter pour réinitialiser les tables plus décommenter dans la fonction
        # self.supp_table()
        #
        self.init_ingredient()
        self.init_recette()
        self.init_repas()

    # def ouvrir_bdd(self):
    #    return sqlite3.connect('Ressource/BDD/GestionRepas.db')

    def fermer_bdd(self):
        """A priori jamais appelé"""
        self.conn.close()

    # Gestion table ingrédient
    def add_ingredient(self, ingredient: Ingredient):
        """ Ajout d'un ingrédient dans la BDD"""
        cursor = self.conn.cursor()
        cursor.execute("""
                INSERT INTO ingredient(nom, unite, lieu, nb, commentaire) VALUES(?, ?, ?, ?, ?)""",
                       (ingredient.get_nom(), ingredient.get_unite(), ingredient.get_lieu(), ingredient.get_nb(),
                        ingredient.get_commentaire()))
        self.conn.commit()
        i = cursor.lastrowid
        return i

    def modif_ingredient(self, ingredient: Ingredient):
        """ Modif d'un ingrédient dans la BDD"""
        cursor = self.conn.cursor()
        cursor.execute("""
                UPDATE ingredient set nom = ?, unite=?, lieu=?, nb=?, commentaire=? where id = ?""",
                       (ingredient.get_nom(), ingredient.get_unite(), ingredient.get_lieu(), ingredient.get_nb(),
                        ingredient.get_commentaire(), ingredient.get_id()))
        self.conn.commit()

    def supp_ingredient(self, id_ingredient: int):
        """ Suppresion d'un ingrédient par son id dans la bdd"""
        cursor = self.conn.cursor()
        cursor.execute("""
                delete from ingredient where id = ?""",
                       (id_ingredient,))
        self.conn.commit()

    def get_liste_ingredients(self):
        """ récupération de la liste des ingrédients de la BDD"""
        list_ing = []
        cursor = self.conn.cursor()
        cursor.execute("""SELECT id, nom, lieu, unite, nb, commentaire FROM ingredient""")
        rows = cursor.fetchall()
        for row in rows:
            i = Ingredient(nom=row[1], lieu=row[2], unite=row[3], nb=row[4], commentaire=row[5], id_ingredient=row[0])
            list_ing.append(i)
        return list_ing

    # Gestion table recette
    def add_recette(self, recette: Recette):
        """ récupération de la liste des ingrédients de la BDD"""
        cursor = self.conn.cursor()
        cursor.execute("""INSERT INTO recette(titre, url, nb_personne, difficulte ,recette,note,temps_prepa, 
        temps_cuisson, commentaire) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                       (recette.get_titre(), recette.get_url(), recette.get_nb_personne(), recette.get_difficulte(),
                        recette.get_recette(), recette.get_note(), recette.get_temps_prepa(),
                        recette.get_temps_cuisson(), recette.get_commentaire()))
        self.conn.commit()
        i = cursor.lastrowid
        for ing in recette.get_ingredients():
            cursor.execute("""INSERT INTO recette_ingredients(id_recette, nom,lieu,unite ,nb, commentaire) 
            VALUES(?, ?, ?, ?, ?, ? )""",
                           (i, ing.nom, ing.lieu, ing.unite, ing.nb, ing.commentaire))
        for mc in recette.get_mot_clef():
            cursor.execute("""INSERT INTO recette_mot_clef(id_recette, mot_clef) 
            VALUES(?, ?  )""", (i, mc))
        self.conn.commit()
        return i

    def modif_recette(self, recette: Recette):
        """ modification d'une recette de la BDD"""
        cursor = self.conn.cursor()
        cursor.execute("""UPDATE recette set titre = ?, url = ?, nb_personne = ?, difficulte = ?, recette = ?,  
        note = ?, temps_prepa = ?, temps_cuisson = ?, commentaire = ? where id = ?""",
                       (recette.get_titre(), recette.get_url(), recette.get_nb_personne(), recette.get_difficulte(),
                        recette.get_recette(), recette.get_note(), recette.get_temps_prepa(),
                        recette.get_temps_cuisson(), recette.get_commentaire(), recette.get_id()))
        self.conn.commit()
        cursor = self.conn.cursor()
        cursor.execute(""" delete from recette_ingredients where id_recette = ?""",
                       (recette.get_id(),))
        self.conn.commit()
        cursor = self.conn.cursor()
        cursor.execute(""" delete from recette_mot_clef where id_recette = ?""",
                       (recette.get_id(),))
        self.conn.commit()
        for ing in recette.get_ingredients():
            cursor = self.conn.cursor()
            cursor.execute("""INSERT INTO recette_ingredients(id_recette, nom, lieu, unite, nb, commentaire) 
                              VALUES(?, ?, ?, ?, ?, ? )""",
                           (recette.get_id(), ing.get_nom(), ing.get_lieu(), ing.get_unite(), ing.get_nb(),
                            ing.get_commentaire()))
            self.conn.commit()
        for mc in recette.get_mot_clef():
            cursor = self.conn.cursor()
            cursor.execute("""INSERT INTO recette_mot_clef(id_recette, mot_clef) 
                              VALUES(?, ? )""", (recette.get_id(), mc))
            self.conn.commit()

    def supp_recette(self, id_recette: int):
        """ suppression d'une recette de la BDD"""
        cursor = self.conn.cursor()
        cursor.execute("""
                delete from recette where id = ?""",
                       (id_recette,))
        cursor.execute("""
                delete from recette_ingredients where id = ?""",
                       (id_recette,))
        cursor.execute("""
                delete from recette_mot_clef where id = ?""",
                       (id_recette,))
        self.conn.commit()

    def get_liste_recette(self):
        """ Récupération de la iste des recettes de la BDD"""
        list_rec = []
        cursor = self.conn.cursor()
        cursor.execute("""SELECT id, titre, url, recette, nb_personne, difficulte, note, 
        temps_prepa, temps_cuisson, commentaire FROM recette""")
        rows = cursor.fetchall()
        for row in rows:
            list_ing = []
            cursor2 = self.conn.cursor()
            cursor2.execute("""
                SELECT id, nom, lieu, unite , nb, commentaire FROM recette_ingredients where id_recette= ?""",
                            (row[0],))
            rows2 = cursor2.fetchall()
            for row2 in rows2:
                i = Ingredient(nom=row2[1], lieu=row2[2], unite=row2[3], nb=row2[4], commentaire=row2[5],
                               id_ingredient=row2[0])
                list_ing.append(i)
            cursor3 = self.conn.cursor()
            cursor3.execute("""
                                SELECT mot_clef FROM recette_mot_clef where id_recette= ?""",
                            (row[0],))
            mc = []
            rows3 = cursor3.fetchall()
            for row3 in rows3:
                mc.append(row3[0])
                print(mc)
            r = Recette(titre=row[1], mc=mc, url=row[2], recette=row[3], nb_personne=row[4], difficulte=row[5],
                        note=row[6], temps_prepa=row[7], temps_cuisson=row[8], commentaire=row[9],
                        ingredients=list_ing, id_recette=row[0])
            list_rec.append(r)
        return list_rec

    def get_recette(self, id_recette: int):
        """ Récupération de la iste des recettes de la BDD"""
        recette = Recette()
        cursor = self.conn.cursor()
        cursor.execute("""SELECT id, titre, url, recette, nb_personne, difficulte, note, 
        temps_prepa, temps_cuisson, commentaire FROM recette where id= ?""",
                       (id_recette,))
        rows = cursor.fetchall()
        for row in rows:
            list_ing = []
            cursor2 = self.conn.cursor()
            cursor2.execute("""
                SELECT id, nom, lieu, unite , nb, commentaire FROM recette_ingredients where id_recette= ?""",
                            (id_recette,))
            rows2 = cursor2.fetchall()
            for row2 in rows2:
                i = Ingredient(nom=row2[1], lieu=row2[2], unite=row2[3], nb=row2[4], commentaire=row2[5],
                               id_ingredient=row2[0])
                list_ing.append(i)
            mc = []
            cursor3 = self.conn.cursor()
            cursor3.execute("""
                                SELECT mot_clef FROM recette_mot_clef where id_recette= ?""",
                            (id_recette,))
            rows3 = cursor3.fetchall()
            for row3 in rows3:
                mc.append(row3[0])
            recette = Recette(titre=row[1], mc=mc, url=row[2], recette=row[3], nb_personne=row[4], difficulte=row[5],
                              note=row[6], temps_prepa=row[7], temps_cuisson=row[8], commentaire=row[9],
                              ingredients=list_ing, id_recette=row[0])
        return recette

    def get_liste_mot_clef(self):
        """ Récupération de la iste des recettes de la BDD"""
        mc = []
        cursor = self.conn.cursor()
        cursor.execute("""SELECT distinct mot_clef FROM recette_mot_clef order by mot_clef""")
        rows = cursor.fetchall()
        for row in rows:
            mc.append(row[0])
        return mc

    # Gestion table repas
    def add_repas(self, repas: Repas):
        """ ajout du repas dans la BDD"""
        cursor = self.conn.cursor()
        cursor.execute("""INSERT INTO repas(date, moment, nb_personne, commentaire) VALUES(?, ?, ?, ?)""",
                       (repas.get_date(), repas.get_moment(), repas.get_nbpersonnes(), repas.get_commentaire()))
        self.conn.commit()
        i = cursor.lastrowid
        for ing in repas.get_ingredients():
            cursor.execute("""INSERT INTO repas_ingredients(id_repas, nom,lieu,unite ,nb, commentaire) 
            VALUES(?, ?, ?, ?, ?, ? )""",
                           (i, ing.nom, ing.lieu, ing.unite, ing.nb, ing.commentaire))
        for rec in repas.get_recettes():
            cursor.execute("""INSERT INTO repas_recettes(id_repas, id_recette) 
            VALUES(?, ?  )""", (i, rec.get_id()))
        self.conn.commit()
        return i

    def modif_repas(self, repas: Repas):
        """ modification d'un repas de la BDD"""
        cursor = self.conn.cursor()
        cursor.execute("""UPDATE repas set date = ?, moemnt = ?, nb_personne = ?, commentaire = ? where id = ?""",
                       (repas.get_date(), repas.get_moment(), repas.get_nbpersonnes(), repas.get_commentaire(),
                        repas.get_id()))
        self.conn.commit()
        cursor = self.conn.cursor()
        cursor.execute(""" delete from repas_ingredients where id_repas = ?""",
                       (repas.get_id(),))
        cursor.execute(""" delete from repas_recettes where id_repas = ?""",
                       (repas.get_id(),))
        self.conn.commit()
        for ing in repas.get_ingredients():
            cursor.execute("""INSERT INTO repas_ingredients(id_repas, nom, lieu, unite, nb, commentaire) 
                              VALUES(?, ?, ?, ?, ?, ? )""",
                           (repas.get_id(), ing.get_nom(), ing.get_lieu(), ing.get_unite(), ing.get_nb(),
                            ing.get_commentaire()))
        self.conn.commit()
        for rec in repas.get_recettes():
            cursor = self.conn.cursor()
            cursor.execute("""INSERT INTO repas_recettes(id_repas, id_recette) 
                              VALUES(?, ? )""", (repas.get_id(), rec.get_id()))
            self.conn.commit()

    def supp_repas(self, id_repas: int):
        """ suppression d'un repas de la BDD"""
        cursor = self.conn.cursor()
        cursor.execute("""
                delete from repas where id = ?""",
                       (id_repas,))
        cursor.execute("""
                delete from repas_recettes where id = ?""",
                       (id_repas,))
        cursor.execute("""
                delete from repas_ingredients where id = ?""",
                       (id_repas,))
        self.conn.commit()

    def get_repas(self, id_repas: int):
        """ Récupération d'un repas par son id de la BDD"""
        cursor = self.conn.cursor()
        cursor.execute("""SELECT id, date, moment, nb_personne, commentaire FROM repas where id= ?""",
                       (id_repas,))
        rows = cursor.fetchall()
        repas = None
        for row in rows:
            list_ing = []
            cursor2 = self.conn.cursor()
            cursor2.execute("""
                SELECT id, nom, lieu, unite , nb, commentaire FROM repas_ingredients where id_repas= ?""",
                            (id_repas,))
            rows2 = cursor2.fetchall()
            for row2 in rows2:
                i = Ingredient(nom=row2[1], lieu=row2[2], unite=row2[3], nb=row2[4], commentaire=row2[5],
                               id_ingredient=row2[0])
                list_ing.append(i)
            list_recette = []
            cursor3 = self.conn.cursor()
            cursor3.execute("""
                                SELECT id_recette FROM repas_recettes where id_repas= ?""",
                            (id_repas,))
            rows3 = cursor3.fetchall()
            for row3 in rows3:
                list_recette.append(self.get_recette(row3[0]))
            repas = Repas(date=row[1], moment=row[2], nb=row[3], commentaire=row[4],
                          ingredients=list_ing, recettes=list_recette, id_repas=row[0])
        return repas

    def get_repas_date(self, date: datetime.date, moment: str):
        """ Récupération du repas à une date et un moemnt"""
        cursor = self.conn.cursor()
        cursor.execute("""SELECT id, date, moment, nb_personne, commentaire FROM repas where date= ? and moment= ?""",
                       (date, moment))
        rows = cursor.fetchall()
        repas = None
        for row in rows:
            id_repas = row[0]
            list_ing = []
            cursor2 = self.conn.cursor()
            cursor2.execute("""
                SELECT id, nom, lieu, unite , nb, commentaire FROM repas_ingredients where id_repas= ?""",
                            (id_repas,))
            rows2 = cursor2.fetchall()
            for row2 in rows2:
                i = Ingredient(nom=row2[1], lieu=row2[2], unite=row2[3], nb=row2[4], commentaire=row2[5],
                               id_ingredient=row2[0])
                list_ing.append(i)
            list_recette = []
            cursor3 = self.conn.cursor()
            cursor3.execute("""
                                SELECT id_recette FROM repas_recettes where id_repas= ?""",
                            (id_repas,))
            rows3 = cursor3.fetchall()
            for row3 in rows3:
                list_recette.append(self.get_recette(row3[0]))
            repas = Repas(date=row[1], moment=row[2], nb=row[3], commentaire=row[4],
                          ingredients=list_ing, recettes=list_recette, id_repas=row[0])
        return repas

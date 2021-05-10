""" Classe Repas
"""
import datetime

import Ressource.Classe.Constante as Ct
from Ressource.Classe.Recette import Recette
from Ressource.Classe.Ingredient import Ingredient


class Repas:
    """ Definition de la classe repas :
            Input :
            - date
            - moment (Midi ou Soir)
            Faculatif
            - Liste de Recette
            - Liste d'ingredients
            - nb de personne
            - commentaire
    """
    def __init__(self, date: datetime, moment: str, recettes: [Recette] = None, ingredients: [Ingredient] = None, nb=4,
                 commentaire='', id_repas: int = None):
        if recettes is None:
            recettes = []
        if ingredients is None:
            ingredients = []
        if moment not in Ct.MOMENTS:
            moment = 'Midi'
        self.id = id_repas
        self.date = date
        self.moment = moment
        self.nb_personnes = nb
        self.recettes = recettes
        self.ingredients = ingredients
        self.commentaire = commentaire

    def get_date(self):
        """retourne la date du repas (datetime)"""
        return self.date

    def get_moment(self):
        """retourne la moment du repas ('Midi' ou 'Soir')"""
        return self.moment

    def get_recettes(self):
        """retourne la liste des recettes ([Recettes])"""
        return self.recettes

    def get_ingredients(self):
        """retourne la liste des ingredients ([Ingredients])"""
        return self.ingredients

    def get_titre_recettes(self):
        """Retourne la liste des titres des recettes et des ingredients supp"""
        t = []
        for r in self.recettes:
            t.append(r.get_titre())
        for i in self.ingredients:
            t.append(i.get_nom())
        return t

    def get_commentaire(self):
        """retourne le commentaire sur le repas (str)"""
        return self.commentaire

    def get_nbpersonnes(self):
        """retourne la nombre de personnes (int)"""
        return self.nb_personnes

    def set_id(self, id_repas: str):
        """assigne l'identifient (int)"""
        self.id = id_repas

    def get_id(self):
        """renvoie l'id du repas (int)"""
        return self.id

    def set_recettes(self, r: [Recette]):
        """assigne la liste de recettes (liste de Recette)"""
        self.recettes = r

    def set_ingredients(self, i: [Ingredient]):
        """assigne la liste de ingredients (liste de Ingredient)"""
        self.ingredients = i

    def set_nbpersonnes(self, nb: int):
        """assigne le nb de personnes (int)"""
        self.nb_personnes = nb

    def set_commentaire(self, c: str):
        """assigne un commentaire (texte)"""
        self.commentaire = c

    def set_date(self, d: datetime):
        """assigne la date du repas (datetime)"""
        self.date = d

    def set_moment(self, m: str):
        """assigne le moment du repas (texte)"""
        if m not in Ct.MOMENTS:
            m = 'Midi'
        self.moment = m

    def add_recette(self, r: Recette):
        """Ajoute une recette a la liste des recettes (Recette)"""
        self.recettes.append(r)

    def supp_recette(self, i: int):
        """Supprime une recette par rapport à son emplacement dans la liste (int)"""
        self.recettes.pop(i)

    def add_ingrediente(self, i: Ingredient):
        """Ajoute une ingredient a la liste des ingredients (Ingredient)"""
        self.ingredients.append(i)

    def supp_ingredient(self, i: int):
        """Supprime une ingredient par rapport à son emplacement dans la liste (int)"""
        self.ingredients.pop(i)

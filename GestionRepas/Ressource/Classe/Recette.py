""" Définition de la classe recette
"""
from Ressource.Classe.Ingredient import Ingredient


class Recette:
    """ Definition de la classe recette :
        Input facultatif:
        - Titre de la recette (texte)
        - Liste de mots clefs (liste)
        - url (texte)
        - le texte de la reectte (texte)
        - nb personne (int)
        - la liste des ingredients (liste de Ingredient)
        - difficulte (texte)
        - note (int)
        - temps de préparation (int)
        - temps de cuisson (int)
        - texte du commentaire (texte)
        - id de la recette (int) """

    def __init__(self, titre="", mc: [str] = None, url="", recette="", nb_personne=4, ingredients: [Ingredient] = None,
                 difficulte='Facile', note=5, temps_prepa=0, temps_cuisson=0, commentaire="", id_recette: int = None):
        if mc is None:
            mc = []
        if ingredients is None:
            ingredients = []
        self.id = id_recette
        self.titre = titre
        self.url = url
        self.nb_personne = nb_personne
        self.recette = recette
        self.ingredients = ingredients
        self.note = note
        self.mot_clef = mc
        self.temps_prepa = temps_prepa
        self.temps_cuisson = temps_cuisson
        self.commentaire = commentaire
        self.difficulte = difficulte

    def set_titre(self, titre: str):
        """assigne titre (texte)"""
        self.titre = titre

    def set_url(self, url: str):
        """assigne url (texte)"""
        self.url = url

    def set_nb_personne(self, nb: int):
        """assigne nb personne (int)"""
        self.nb_personne = nb

    def set_recette(self, recette: str):
        """assigne recette (texte)"""
        self.recette = recette

    def set_ingredients(self, ingredients: [Ingredient]):
        """assigne liste des ingredients (liste de Ingredient)"""
        self.ingredients = ingredients

    def set_note(self, note: int):
        """assigne note (int)"""
        self.note = note

    def set_mot_clef(self, mc: [str]):
        """assigne liste des mots clefs(liste de texte)"""
        self.mot_clef = mc

    def set_temps_prepa(self, tp: int):
        """assigne temps de preparation (int)"""
        self.temps_prepa = tp

    def set_temps_cuisson(self, tc: int):
        """assigne temps de cuisson (int)"""
        self.temps_cuisson = tc

    def set_difficulte(self, d: str):
        """assigne difficulte (texte)"""
        self.difficulte = d

    def set_commentaire(self, c: str):
        """assigne commentaire (texte)"""
        self.commentaire = c

    def set_id(self, id_recette: str):
        """assigne l'identifient (int)"""
        self.id = id_recette

    def get_id(self):
        """renvoie l'id de la recette (int)"""
        return self.id

    def get_titre(self):
        """renvoie le titre de la recette (texte)"""
        return self.titre

    def get_url(self):
        """renvoie l'url de la recette (texte)"""
        return self.url

    def get_nb_personne(self):
        """renvoie le nb de personne de la recette (int)"""
        return self.nb_personne

    def get_recette(self):
        """renvoie le texte de la recette (texte)"""
        return self.recette

    def get_ingredients(self):
        """renvoie la liste de ingrédients associés à la recette (liste de Ingredient)"""
        return self.ingredients

    def get_nom_ingredients(self):
        """renvoie la liste des noms des ingrédients associés à la recette (liste de texte)"""
        n = []
        for i in self.ingredients:
            n.append(i.get_nom())
        return n

    def get_note(self):
        """renvoie la note de la recette (int)"""
        return self.note

    def get_mot_clef(self):
        """renvoie la liste de mots clefs associés à la recette (liste de texte)"""
        return self.mot_clef

    def get_temps_prepa(self):
        """renvoie le temps de prepa de la recette (int)"""
        return self.temps_prepa

    def get_temps_cuisson(self):
        """renvoie le temps de cuisson de la recette (int)"""
        return self.temps_cuisson

    def get_commentaire(self):
        """renvoie le commentaire de la recette (texte)"""
        return self.commentaire

    def get_difficulte(self):
        """renvoie la difficulte de la recette (texte)"""
        return self.difficulte

    def add_ingredients(self, ing: Ingredient):
        """Ajoute un ingrédient à la liste des ingrédients de la recette
           Tri des ingrédients par le lieu puis le nom de l'ingrédient"""
        self.ingredients.append(ing)
        self.ingredients = sorted(self.ingredients,
                                  key=lambda ingredient: ingredient.lieu + ingredient.nom)

    def supp_ingredients(self, id_ing: int):
        """Supprime un ingrédient par son emplacement dans la liste des ingrédients"""
        self.ingredients.pop(id_ing)

    def supp_all_ingredients(self):
        """Supprime tous les ingrédients de la liste des ingrédients"""
        self.ingredients = []

    def add_mot_clef(self, mc: str):
        """Ajoute un mot clef à la recette
           Tri des mots clefs par ordre alphabétique"""
        if mc not in self.mot_clef:
            self.mot_clef.append(mc)
            self.mot_clef = sorted(self.mot_clef)

    def supp_mot_clef(self, id_mc: int):
        """Supprime un mot clef par son emplacement dans la liste des mots clefs"""
        self.mot_clef.pop(id_mc)

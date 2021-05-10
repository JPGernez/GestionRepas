""" Définition de la classe ingrédient
"""


class Ingredient:
    """ Definition de la classe ingrédient :
        Input:
        - le nom de l'ingrédient (texte)
        Facultatif:
        - lieu d'achat de l'ingrédient (texte)
        - l'unite de mesure(texte)
        - un nombre d'élément par défaut (int)
        - un commentaire (texte)
        - id de l'ingrédient (int)
        """

    def __init__(self, nom: str, lieu="", unite="", nb: int = None, commentaire="", id_ingredient: int = None):
        self.id = id_ingredient
        self.nom = nom
        self.lieu = lieu
        self.unite = unite
        self.nb = nb
        self.commentaire = commentaire

    def set_nom(self, n: str):
        """assigne nom (texte)"""
        self.nom = n

    def set_unite(self, u: str):
        """assigne unité de mesure(texte)"""
        self.unite = u

    def set_lieu(self, li: str):
        """assigne le lieu d'achat (texte)"""
        self.lieu = li

    def set_nb(self, n: int):
        """assigne nb d'unité (int)"""
        self.nb = n

    def set_commentaire(self, c: str):
        """assigne commentaire (texte)"""
        self.commentaire = c

    def get_id(self):
        """renvoie l'id de l'ingrédient (int)"""
        return self.id

    def get_nom(self):
        """renvoie le nom de l'ingrédient (texte)"""
        return self.nom

    def get_unite(self):
        """renvoie l'unité de mesure de l'ingrédient (texte)"""
        return self.unite

    def get_lieu(self):
        """renvoie le lieu d'achat de l'ingrédient (texte)"""
        return self.lieu

    def get_nb(self):
        """renvoie le nombre d'unité de l'ingrédient (int)"""
        return self.nb

    def get_commentaire(self):
        """renvoie le commentaire de l'ingrédient (texte)"""
        return self.commentaire

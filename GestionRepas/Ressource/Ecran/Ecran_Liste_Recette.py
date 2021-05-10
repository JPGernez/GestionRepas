"""Ecran liste les recettes
   """
import tkinter as tk

import Ressource.Ecran.Ecran_Recette as Ecran_recette
import Ressource.Ecran.Ecran_Accueil as Ecran_accueil

from Ressource.Classe.Bdd import Bdd
import Ressource.Classe.Constante as Ct


class Ecran_Liste_Recette(tk.Frame):
    """Définition de l'écran de saisi modification des ingrédients"""

    def recup_liste_nom_ingredient(self):
        """ Recuperation de la liste noms d'ingrédient"""
        liste_ingredient = Bdd.get_liste_ingredients(self.bdd)
        self.liste_nom_ingredient = []
        for i in liste_ingredient:
            if i.get_nom() not in self.liste_nom_ingredient:
                self.liste_nom_ingredient.append(i.get_nom())
        self.liste_nom_ingredient.sort()

    def recup_mot_clef(self):
        """ Recuperation de la liste noms d'ingrédient"""
        self.liste_mot_clef = Bdd.get_liste_mot_clef(self.bdd)

    def recup_liste_recette(self):
        """Recuperation de la liste des recettes et des mots clefs depuis la BDD
           Mets a jour 2 listes existantes: liste_recette et liste_mot_clef
           """
        self.liste_recette = Bdd.get_liste_recette(self.bdd)
        self.liste_recette = sorted(self.liste_recette,
                                    key=lambda recette: recette.get_titre())
        self.liste_mot_clef = Bdd.get_liste_mot_clef(self.bdd)

    def ajout_recette(self):
        """Ouvre l'écran de saisi d'une recette
           """
        self.id_recette = None
        self.controller.show_frame(Ecran_recette.Ecran_Recette)

    def affich_recette(self):
        """Ouvre l'écran de saisi d'une recette sur une recette définie
           """
        if self.lbox_recette.curselection() is not None and self.lbox_recette.curselection() != ():
            selection = self.lbox_recette.curselection()[0]
            self.id_recette = self.liste_recette_affiche[selection].get_id()
            self.controller.show_frame(Ecran_recette.Ecran_Recette)

    def afficher_liste_recette(self, *event):
        """ Affichage de la liste des recettes à l'écran
            Remise à 0 de la partie modificaton de l'ingrédient"""
        print('Ingredient ', event)
        self.lbox_recette.delete(0, tk.END)
        self.liste_recette_affiche = []
        if self.lbox_ingredients.curselection() is not None and self.lbox_ingredients.curselection() != ():
            selected_ing = [self.lbox_ingredients.get(i) for i in self.lbox_ingredients.curselection()]
        else:
            selected_ing = []
        if self.lbox_mot_clef.curselection() is not None and self.lbox_mot_clef.curselection() != ():
            selected_mot = [self.lbox_mot_clef.get(m) for m in self.lbox_mot_clef.curselection()]
        else:
            selected_mot = []
        for rec in self.liste_recette:
            garder = 'OUI'
            for ing in selected_ing:
                if ing not in rec.get_nom_ingredients():
                    garder = 'NON'
            for mot in selected_mot:
                if mot not in rec.get_mot_clef():
                    garder = 'NON'
            if garder == 'OUI':
                self.liste_recette_affiche.append(rec)
                self.lbox_recette.insert(tk.END, rec.get_titre())

    def afficher_liste_ingredient(self):
        """ Affichage de la liste des ingredients à l'écran"""
        self.lbox_ingredients.delete(0, tk.END)
        for ing in self.liste_nom_ingredient:
            self.lbox_ingredients.insert(tk.END, ing)

    def afficher_liste_mot_clef(self):
        """ Affichage de la liste des mots clefs à l'écran"""
        self.lbox_mot_clef.delete(0, tk.END)
        for m in self.liste_mot_clef:
            self.lbox_mot_clef.insert(tk.END, m)

    def on_show_frame(self, event):
        """Initialisation de la fenetre """
        print(event)
        # Recup de la liste de départ
        self.recup_liste_nom_ingredient()
        self.recup_mot_clef()
        self.afficher_liste_ingredient()
        self.afficher_liste_mot_clef()
        self.recup_liste_recette()
        self.afficher_liste_recette()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=Ct.BG)
        # Init variable
        self.liste_recette = []
        self.liste_recette_affiche = []
        self.liste_mot_clef = []
        self.bdd = Bdd()
        self.controller = controller
        self.id_recette = None
        self.bind("<<ShowFrame>>", self.on_show_frame)
        self.liste_nom_ingredient = []

        self.button_back = tk.Button(self, text="Retour",
                                     command=lambda: controller.show_frame(Ecran_accueil.Ecran_Accueil), font=Ct.FONT,
                                     bg=Ct.BG, fg=Ct.FG)
        self.button_back.pack()
        self.window = tk.Frame(self)
        self.window.config(background=Ct.BG)

        # initialization des composants
        self.label = tk.Label(self.window, text="Choix parmi les recettes existantes: ", font=Ct.FONT_TITRE, bg=Ct.BG,
                              fg=Ct.FG)
        self.label.pack(padx=2, pady=2, fill=tk.X)

        # --- FRAME RECHERCHE
        self.frame_recherche = tk.Frame(self.window, bg=Ct.BG)
        # liste des ingrédients
        self.label = tk.Label(self.frame_recherche, text="Choix ingrédient: ", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.label.pack(padx=2, pady=2)

        self.lbox_ingredients = tk.Listbox(self.frame_recherche, bd=2, width=50, font=Ct.FONT, fg=Ct.FG_TEXTE,
                                           selectbackground=Ct.BG_SELECT, selectmode=tk.MULTIPLE,
                                           exportselection=tk.FALSE)
        self.vscroll_ingredients = tk.Scrollbar(self.frame_recherche, command=self.lbox_ingredients.yview, bg=Ct.BG)
        self.lbox_ingredients.config(yscrollcommand=self.vscroll_ingredients.set)
        self.lbox_ingredients.bind("<<ListboxSelect>>", self.afficher_liste_recette)
        self.vscroll_ingredients.pack(side=tk.RIGHT, expand=tk.N, fill=tk.Y, padx=1, pady=1)
        self.lbox_ingredients.pack( padx=2, pady=2)
        # liste des ingrédients
        self.label = tk.Label(self.frame_recherche, text="Choix mots clefs: ", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.label.pack(padx=2, pady=12)
        self.lbox_mot_clef = tk.Listbox(self.frame_recherche, bd=2, width=50, font=Ct.FONT, fg=Ct.FG_TEXTE,
                                        selectbackground=Ct.BG_SELECT, selectmode=tk.MULTIPLE,
                                        exportselection=tk.FALSE)
        self.vscroll_mot_clef = tk.Scrollbar(self.frame_recherche, command=self.lbox_mot_clef.yview, bg=Ct.BG)
        self.lbox_mot_clef.config(yscrollcommand=self.vscroll_mot_clef.set)
        self.lbox_mot_clef.bind("<<ListboxSelect>>", self.afficher_liste_recette)
        self.vscroll_ingredients.pack(side=tk.RIGHT, expand=tk.N, fill=tk.Y, padx=1, pady=1)
        self.lbox_mot_clef.pack(padx=2, pady=2)

        # --- FRAME RECHERCHE FIN
        self.frame_recherche.pack(side=tk.LEFT)

        # --- FRAME LISTE DES RECETTES
        self.frame_liste_recette = tk.Frame(self.window, bg=Ct.BG)
        self.label = tk.Label(self.frame_liste_recette, text="Liste des recettes: ", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.label.pack(padx=2, pady=12)
        # liste des recettes
        self.lbox_recette = tk.Listbox(self.frame_liste_recette, bd=2, width=50, font=Ct.FONT, fg=Ct.FG_TEXTE,
                                       selectbackground=Ct.BG_SELECT, exportselection=tk.FALSE)
        self.vscroll_recette = tk.Scrollbar(self.frame_liste_recette, command=self.lbox_recette.yview, bg=Ct.BG)
        self.lbox_recette.config(yscrollcommand=self.vscroll_recette.set)
        self.vscroll_recette.pack(side=tk.RIGHT, expand=tk.N, fill=tk.Y, padx=1, pady=1)
        self.lbox_recette.pack(side=tk.LEFT, padx=2, pady=2, fill=tk.Y)

        # --- FRAME LISTE DES RECETTES FIN
        self.frame_liste_recette.pack(padx=20, pady=2, fill=tk.BOTH, expand=tk.Y)

        # --- FRAME BOUTON
        self.frame_bouton = tk.Frame(self.window, bg=Ct.BG)
        # Bouton ajout/ modif/ Supp
        self.add_recette = tk.Button(self.frame_bouton, text="Nouvelle recette", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG,
                                     command=self.ajout_recette)
        self.add_recette.pack(padx=10, pady=10, fill=tk.X)

        self.modif_recette = tk.Button(self.frame_bouton, text="Voir la recette", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG,
                                       command=self.affich_recette)
        self.modif_recette.pack(padx=10, pady=10, fill=tk.X)
        # --- FRAME BOUTON FIN
        self.frame_bouton.pack(side=tk.BOTTOM, padx=10, pady=10, fill=tk.X)

        # empaquetage final
        self.window.pack()

    def execute(self):
        """Non utilisé"""
        pass

    def cancel(self):
        """Non utilisé"""
        pass

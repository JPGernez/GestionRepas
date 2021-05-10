"""Ecran ingrédient
   Saisi et modification de la description d'objet ingrédient
   """
import tkinter as tk
from tkinter import ttk

import Ressource.Ecran.Ecran_Accueil as Ecran_acceuil
import Ressource.Ecran.Ecran_Recette as Ecran_recette

from Ressource.Classe.Bdd import Bdd
import Ressource.Classe.Constante as Ct
from Ressource.Classe.Ingredient import Ingredient


class Ecran_Ingredient(tk.Frame):
    """Définition de l'écran de saisi modification des ingrédients"""

    def recup_liste_ingredient(self):
        """Recuperation de la liste des ingredients dans la BDD
           Mets a jour 2 listes existantes: liste_ingredient_complete et liste_lieu
           """
        self.liste_ingredient_complete = Bdd.get_liste_ingredients(self.bdd)
        self.liste_ingredient_complete = sorted(self.liste_ingredient_complete,
                                                key=lambda ingredient: ingredient.get_nom())
        self.liste_lieu = []
        for x in self.liste_ingredient_complete:
            if x.get_lieu() not in self.liste_lieu:
                self.liste_lieu.append(x.get_lieu())
        self.liste_lieu.sort()
        self.liste_lieu.insert(0, 'Tous')

    def ajout_ingredient(self):
        """Ajout de l'ingrédient saisi dans la BDD,
           relance de la recup des listes ds'ingredient
           et affichage de ces listes a l'écran"""
        try:
            nb = float(self.saisinb.get())
        except ValueError:
            nb = 0
        if len(self.saisinom.get()) > 2:
            ing = Ingredient(nom=self.saisinom.get(), lieu=self.saisilieu.get(), unite=self.saisiunite.get(), nb=nb,
                             commentaire=self.saisicomm.get())
            Bdd.add_ingredient(self.bdd, ing)
            self.recup_liste_ingredient()
            self.afficher_liste_ingredients()

    def modif_ingredient(self):
        """Modification de l'ingrédient sélectionné dans la BDD,
           relance de la recup des listes ds'ingredient
           et affichage de ces listes a l'écran"""
        try:
            nb = float(self.saisinb.get())
        except ValueError:
            nb = 0
        if self.id_select is not None and len(self.saisinom.get()) > 2:
            ing = Ingredient(nom=self.saisinom.get(), lieu=self.saisilieu.get(), unite=self.saisiunite.get(), nb=nb,
                             commentaire=self.saisicomm.get(),
                             id_ingredient=self.liste_ingredient[self.id_select].get_id())
            Bdd.modif_ingredient(self.bdd, ing)
        self.recup_liste_ingredient()
        self.afficher_liste_ingredients()

    def supp_ingredient(self):
        """Suppression de l'ingrédient sélectionné dans la BDD,
           relance de la recup des listes ds'ingredient
           et affichage de ces listes a l'écran"""
        if self.id_select is not None:
            id_supp = self.liste_ingredient[self.id_select].get_id()
            Bdd.supp_ingredient(self.bdd, id_supp)
        self.recup_liste_ingredient()
        self.afficher_liste_ingredients()

    def afficher_detail_ingredient(self):
        """Affichage du détail de l'ingrédient sélectionné """
        if self.id_select is not None:
            self.labelId.config(text=self.liste_ingredient[self.id_select].get_id())
            self.saisinom.delete(0, tk.END)
            self.saisinom.insert(0, self.liste_ingredient[self.id_select].get_nom())
            self.saisilieu.delete(0, tk.END)
            self.saisilieu.insert(0, self.liste_ingredient[self.id_select].get_lieu())
            self.saisiunite.delete(0, tk.END)
            self.saisiunite.insert(0, self.liste_ingredient[self.id_select].get_unite())
            self.saisinb.delete(0, tk.END)
            self.saisinb.insert(0, str(self.liste_ingredient[self.id_select].get_nb()))
            self.saisicomm.delete(0, tk.END)
            self.saisicomm.insert(0, self.liste_ingredient[self.id_select].get_commentaire())
            self.mod_ing.configure(state=tk.NORMAL)
            self.del_ing.configure(state=tk.NORMAL)

    def selection_ingredient(self, *event):
        """
          Récupération de l'id sélectionner
          Affichge des details de l'ingredient
        """
        print(event)
        if self.lbox_ingredient.curselection() is not None and self.lbox_ingredient.curselection() != ():
            selection = self.lbox_ingredient.curselection()[0]
            if selection != self.id_select:
                self.id_select = selection
                self.afficher_detail_ingredient()
                self.saisinom.focus()

    def afficher_liste_ingredients(self, *event):
        """ Affichage de la liste des ingredients à l'écran
            Remise à 0 de la partie modificaton de l'ingrédient"""
        print(event)
        self.lbox_ingredient.delete(0, tk.END)
        self.liste_ingredient = []
        for ing in self.liste_ingredient_complete:
            if self.cb_lieu.get() == "Tous" or ing.lieu == self.cb_lieu.get():
                self.liste_ingredient.append(ing)
                self.lbox_ingredient.insert(tk.END,
                                            "{} ({}) - {}".format(ing.get_nom(), ing.get_unite(), ing.get_lieu(),
                                                                  ing.get_id()))
        self.mod_ing.configure(state=tk.DISABLED)
        self.del_ing.configure(state=tk.DISABLED)
        self.labelId.config(text='')
        self.saisinom.delete(0, tk.END)
        self.saisilieu.delete(0, tk.END)
        self.saisiunite.delete(0, tk.END)
        self.saisinb.delete(0, tk.END)
        self.saisicomm.delete(0, tk.END)
        self.id_select = None

    def on_show_frame(self, event):
        """Initialisation de la fenetre """
        print(event)
        # Recup de la liste de départ
        ecran_origine = self.controller.frame_prec
        if ecran_origine == "Ecran_Recette":
            lien = Ecran_recette.Ecran_Recette
        else:
            lien = Ecran_acceuil.Ecran_Accueil
        self.button_back.config(command=lambda: self.controller.show_frame(lien), font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        # Recup de la liste de départ
        self.recup_liste_ingredient()
        self.cb_lieu['values'] = self.liste_lieu
        self.cb_lieu.current(0)
        self.afficher_liste_ingredients()

    def __init__(self, parent, controller):
        # Init variable
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.liste_ingredient_complete = []
        self.liste_ingredient = []
        self.liste_lieu = []
        self.id_select = None
        self.bdd = Bdd()
        self.bind("<<ShowFrame>>", self.on_show_frame)

        # Création de la fenetre

        self.button_back = tk.Button(self, text="retour", font=Ct.FONT_TITRE, bg=Ct.BG, fg=Ct.FG,
                                     command=lambda: controller.show_frame(Ecran_acceuil.Ecran_Accueil))
        self.button_back.pack()

        self.window = tk.Frame(self)
        self.window.config(background=Ct.BG)

        # initialization des composants
        self.frame1 = tk.Frame(self.window, bg=Ct.BG)
        self.label = tk.Label(self.frame1, text="Liste des ingrédients existants: ", font=Ct.FONT_TITRE, bg=Ct.BG,
                              fg=Ct.FG)
        self.label.pack(padx=2, pady=2, fill=tk.X)

        # liste des ingredients
        self.frame2 = tk.Frame(self.frame1, bd=4, height=200, bg=Ct.BG)

        # Liste déroulante
        self.label = tk.Label(self.frame2, text="Lieu achat: ", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.label.grid(row=1, column=0, sticky=tk.W)
        self.cb_lieu = ttk.Combobox(self.frame2, width=30, textvariable='Tous', font=Ct.FONT)
        self.cb_lieu.grid(row=1, column=1, padx=10, sticky=tk.W)
        self.cb_lieu.bind('<<ComboboxSelected>>', self.afficher_liste_ingredients)
        self.frame2.pack(padx=2, pady=2, fill=tk.X)
        self.cb_lieu.focus()

        # liste des ingrédients du lieu sélectionné
        self.frame2b = tk.Frame(self.frame1, bd=4, height=250, bg=Ct.BG)
        self.lbox_ingredient = tk.Listbox(self.frame2b, bd=2, width=50, font=Ct.FONT, fg=Ct.FG_TEXTE,
                                          selectbackground=Ct.BG_SELECT)
        self.vscroll = tk.Scrollbar(self.frame2b, command=self.lbox_ingredient.yview, bg=Ct.BG)
        self.lbox_ingredient.config(yscrollcommand=self.vscroll.set)
        self.lbox_ingredient.bind("<<ListboxSelect>>", self.selection_ingredient)
        self.vscroll.pack(side=tk.RIGHT, expand=tk.N, fill=tk.Y, padx=1, pady=1)
        self.lbox_ingredient.pack(side=tk.LEFT, padx=2, pady=2)
        self.frame2b.pack(padx=2, pady=2, fill=tk.X)

        # Saisi nouvel ingredient
        self.frame3 = tk.Frame(self.frame1, bd=4, height=200, bg=Ct.BG)
        self.label = tk.Label(self.frame3, text="Détail ingrédient: ", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.label.grid(row=0, column=0, sticky=tk.W)
        self.labelId = tk.Label(self.frame3, text=" ", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.labelId.grid(row=0, column=1, sticky=tk.W)
        self.label = tk.Label(self.frame3, text="Nom ingrédient", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.label.grid(row=1, column=0, sticky=tk.W)
        self.saisinom = tk.Entry(self.frame3, font=Ct.FONT, fg=Ct.FG_TEXTE, width=40)
        self.saisinom.grid(row=1, column=1, sticky=tk.W, columnspan=2)
        self.label = tk.Label(self.frame3, text="Lieu d'achat", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.label.grid(row=2, column=0, sticky=tk.W)
        self.saisilieu = tk.Entry(self.frame3, font=Ct.FONT, fg=Ct.FG_TEXTE, width=40)
        self.saisilieu.grid(row=2, column=1, sticky=tk.W, columnspan=2)
        self.label = tk.Label(self.frame3, text="Nb par défaut", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.label.grid(row=3, column=0, sticky=tk.W)
        self.saisinb = tk.Entry(self.frame3, font=Ct.FONT, fg=Ct.FG_TEXTE, width=40)
        self.saisinb.grid(row=3, column=1, sticky=tk.W, columnspan=2)
        self.label = tk.Label(self.frame3, text="Unité par défaut", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.label.grid(row=4, column=0, sticky=tk.W)
        self.saisiunite = tk.Entry(self.frame3, font=Ct.FONT, fg=Ct.FG_TEXTE, width=40)
        self.saisiunite.grid(row=4, column=1, sticky=tk.W, columnspan=2)
        self.label = tk.Label(self.frame3, text="Commentaire", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.label.grid(row=5, column=0, sticky=tk.W)
        self.saisicomm = tk.Entry(self.frame3, font=Ct.FONT, fg=Ct.FG_TEXTE, width=40)
        self.saisicomm.grid(row=5, column=1, sticky=tk.W, columnspan=2)

        self.frame3.pack(padx=10, pady=10, fill=tk.X)

        # Bouton ajout/ modif/ Supp
        self.frame4 = tk.Frame(self.frame1, bd=4, height=200, bg=Ct.BG)
        self.add_ing = tk.Button(self.frame4, text="Ajouter", font=Ct.FONT_TITRE, bg=Ct.BG, fg=Ct.FG,
                                 command=self.ajout_ingredient)
        self.add_ing.pack(padx=10, pady=10, fill=tk.X)
        self.mod_ing = tk.Button(self.frame4, text="Modifier", font=Ct.FONT_TITRE, bg=Ct.BG, fg=Ct.FG,
                                 command=self.modif_ingredient, state=tk.DISABLED)
        self.mod_ing.pack(padx=10, pady=10, fill=tk.X)
        self.del_ing = tk.Button(self.frame4, text="Supprimer", font=Ct.FONT_TITRE, bg=Ct.BG, fg=Ct.FG,
                                 command=self.supp_ingredient, state=tk.DISABLED)
        self.del_ing.pack(padx=10, pady=10, fill=tk.X)
        self.frame4.pack(side=tk.BOTTOM, padx=10, pady=10, fill=tk.X)

        # empaquetage final
        self.frame1.pack(expand=tk.YES)
        self.afficher_liste_ingredients()
        self.window.pack()

    def execute(self):
        """Non utilisé"""
        pass

    def cancel(self):
        """Non utilisé"""
        pass

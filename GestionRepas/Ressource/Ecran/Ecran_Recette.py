"""Ecran recette
   Saisi et modification de la description d'objet recette
   """

import tkinter as tk
from tkinter import messagebox
import webbrowser

import Ressource.Ecran.Ecran_Accueil as Ecran_acceuil
import Ressource.Ecran.Ecran_Liste_Recette as Ecran_Liste_Recette
import Ressource.Ecran.Ecran_Ingredient as Ecran_Ingredient

import Ressource.Classe.Constante as Ct
from Ressource.Classe.Bdd import Bdd
from Ressource.Classe.Recette import Recette
from Ressource.Classe.AutocompletComboBox import AutocompleteCombobox


# from loguru import logger
# from snoop import snoop
# from heartrate import trace
# trace(browser=True)
class Ecran_Recette(tk.Frame):
    """Définition de l'écran de saisi modification des recettes"""

    def recup_liste_ingredient(self):
        """ Recuperation de la liste des ingredients et de la liste des noms d'ingrédient"""
        self.liste_ingredient_complete = self.bdd.get_liste_ingredients()
        self.liste_ingredient_complete = sorted(self.liste_ingredient_complete, key=lambda ingredient: ingredient.nom)
        self.liste_nom_ingredient = []
        for i in self.liste_ingredient_complete:
            if i.get_nom() not in self.liste_nom_ingredient:
                self.liste_nom_ingredient.append(i.get_nom())
        self.liste_nom_ingredient.sort()

    def recup_liste_mot_clef(self):
        """ Recuperation de la liste des mots clefs"""
        self.liste_mot_clef = self.bdd.get_liste_mot_clef()

    def afficher_detail_ingredient(self):
        """ Afficher le détail d'un ingrédient sélectionné"""
        for i in self.liste_ingredient_complete:
            if i.get_nom() == self.saisinom.get():
                self.saisilieu.delete(0, tk.END)
                self.saisilieu.insert(0, i.get_lieu())
                self.saisiunite.delete(0, tk.END)
                self.saisiunite.insert(0, i.get_unite())
                self.saisinbing.delete(0, tk.END)
                self.saisinbing.insert(0, str(i.get_nb()))
                self.saisicomm.delete(0, tk.END)
                self.saisicomm.insert(0, i.get_commentaire())

    def ajout_ingredient(self):
        """ Ajout d'un ingrédient a laliste des ingredients de la recette
            relance de l'affichage de la liste des ingrédients"""
        try:
            nb = float(self.saisinbing.get())
        except ValueError:
            nb = 0
        if len(self.saisinom.get()) > 2:
            ing = Ecran_Ingredient.Ingredient(nom=self.saisinom.get(), lieu=self.saisilieu.get(),
                                              unite=self.saisiunite.get(), nb=nb, commentaire=self.saisicomm.get())
            self.recette.add_ingredients(ing)
            self.afficher_liste_ingredients_recette()

    # Modification d'un ingrédient dans la recette
    def mod_ingredient(self):
        """ Mise a jour du détail de l'ingrédient sur l'écran
            retrait d'un ingrédient de laliste des ingredients de la recette
            relance de l'affichage de la liste des ingrédients"""
        if self.lbox_recette.curselection() is not None and self.lbox_recette.curselection() != ():
            selection = self.lbox_recette.curselection()[0]
            i = self.recette.ingredients[selection]
            self.saisinom.delete(0, tk.END)
            self.saisinom.insert(0, i.get_nom())
            self.saisilieu.delete(0, tk.END)
            self.saisilieu.insert(0, i.get_lieu())
            self.saisiunite.delete(0, tk.END)
            self.saisiunite.insert(0, i.get_unite())
            self.saisinbing.delete(0, tk.END)
            self.saisinbing.insert(0, str(i.get_nb()))
            self.saisicomm.delete(0, tk.END)
            self.saisicomm.insert(0, i.get_commentaire())
            self.recette.supp_ingredients(selection)
            self.afficher_liste_ingredients_recette()

    def supp_ingredient(self):
        """ Fenetre alerte puis Suppression de l'ensemble des ingrédients de la liste"""
        m = messagebox.askyesno(title="Effacer la liste de tous les ingrédients", message="Etes-vous sur?")
        if m:
            self.recette.supp_all_ingredients()
            self.afficher_liste_ingredients_recette()
        else:
            messagebox.showinfo(title='Effacer la liste de tous les ingrédients', message='Vous avez eu peur!')

    def saisi_nom_ingredient(self, *event):
        """"Saisi ou sélection d'un nom ingrédient : récupération de l'id selectionné
            Affichage du détail de cet ingrédient"""
        print(event)
        self.afficher_detail_ingredient()
        self.saisinbing.focus()

    # Mise à jour de la liste des ingrédients de la recette
    def afficher_liste_ingredients_recette(self):
        """Affichge de la liste des ingrédients associés à la recette"""
        self.lbox_recette.delete(0, tk.END)
        for ing in self.recette.ingredients:
            self.lbox_recette.insert(tk.END, "{}: {} {} ({}) - {}".format(ing.nom, ing.nb, ing.unite, ing.lieu,
                                                                          ing.commentaire))

    def openweb(self):
        """ ouverture d'une page web en foncion de l'url saisi"""
        webbrowser.open_new(self.saisiurl.get())

    def saisi_mot_clef(self, *event):
        """Sélection ou saisi d'un mot clef a ajouter à la liste"""
        print(event)
        mc = self.saisimotclef.get()
        self.recette.add_mot_clef(mc)
        self.affichage_mot_clef_recette()

    def affichage_mot_clef_recette(self):
        """ Affiche les mots clefs associés à la recette """
        self.lbox_motclef.delete(0, tk.END)
        for mc in self.recette.get_mot_clef():
            self.lbox_motclef.insert(tk.END, mc)

    def select_motclef(self, *event):
        """Suppression du mot clef cliquer et ajout dans la saisie de mot clef"""
        print(event)
        if self.lbox_motclef.curselection() is not None and self.lbox_motclef.curselection() != ():
            self.saisimotclef.delete(0, tk.END)
            self.saisimotclef.insert(0, self.recette.get_mot_clef()[self.lbox_motclef.curselection()[0]])
            self.recette.supp_mot_clef(self.lbox_motclef.curselection()[0])
            self.affichage_mot_clef_recette()

    def init_saisi_recette(self):
        """Initialise l'affichage de l'écran avec les infos de la recette"""
        self.saisititre.delete(0, tk.END)
        self.saisititre.insert(0, self.recette.get_titre())
        self.saisinote.delete(0, tk.END)
        self.saisinote.insert(0, self.recette.get_note())
        self.saisinbpers.delete(0, tk.END)
        self.saisinbpers.insert(0, self.recette.get_nb_personne())
        self.saisitpsprepa.delete(0, tk.END)
        self.saisitpsprepa.insert(0, self.recette.get_temps_prepa())
        self.saisitpscuisson.delete(0, tk.END)
        self.saisitpscuisson.insert(0, self.recette.get_temps_cuisson())
        self.saisidiff.delete(0, tk.END)
        self.saisidiff.insert(0, self.recette.get_difficulte())
        self.saisiurl.delete(0, tk.END)
        self.saisiurl.insert(0, self.recette.get_url())
        self.affichage_mot_clef_recette()
        self.afficher_liste_ingredients_recette()
        self.texte_recette.delete(1.0, tk.END)
        self.texte_recette.insert(1.0, self.recette.get_recette())
        self.comm_recette.delete(1.0, tk.END)
        self.comm_recette.insert(1.0, self.recette.get_commentaire())

    def enregistrement_recette(self, *event):
        """Enregistrement de la recette dans la BDD"""
        print(event)
        self.recette.set_titre(self.saisititre.get())
        self.recette.set_url(self.saisiurl.get())
        self.recette.set_recette(self.texte_recette.get('1.0', tk.END))
        self.recette.set_nb_personne(self.saisinbpers.get())
        self.recette.set_difficulte(self.saisidiff.get())
        self.recette.set_note(self.saisinote.get())
        self.recette.set_temps_prepa(self.saisitpsprepa.get())
        self.recette.set_temps_cuisson(self.saisitpscuisson.get())
        self.recette.set_commentaire(self.comm_recette.get('1.0', tk.END))
        if self.recette.get_id() is None:
            self.recette.set_id(self.bdd.add_recette(self.recette))
        else:
            self.bdd.modif_recette(self.recette)

    def on_show_frame(self, event):
        """Initialisation de la fenetre en recuperant l'écran d'origine
           et suivant l'écran d'origine on regarde si l'id_recette correspondant à une recette sélectionnée
           est renseignée sinon on affiche l'écran de saisi à vide"""
        print(event)
        # recupération de l'écran précédent
        ecran_origine = self.controller.frame_prec
        if ecran_origine == "Ecran_Liste_Recette":
            lien = Ecran_Liste_Recette.Ecran_Liste_Recette
        else:
            lien = None
        if ecran_origine != "Ecran_Ingredient":
            # Récupération de l'id de recette de l'cran précédent
            id_recette = self.controller.get_page(ecran_origine).id_recette
            if id_recette is None:
                self.recette = Recette()
            else:
                self.recette = self.bdd.get_recette(id_recette)
            # Recup et affichage de la liste de départ
            self.recup_liste_ingredient()
            self.recup_liste_mot_clef()
            self.saisimotclef.set_completion_list(self.liste_mot_clef)
            self.init_saisi_recette()
            self.saisinom.set_completion_list(self.liste_nom_ingredient)
            self.saisititre.focus()
            self.button_back.config(command=lambda: self.controller.show_frame(lien), font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        else:
            self.recup_liste_ingredient()
            self.saisinom.set_completion_list(self.liste_nom_ingredient)

    # @snoop
    # @logger.catch
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Init variable
        self.liste_ingredient_complete = []
        self.liste_nom_ingredient = []
        self.id_select = None
        self.bdd = Bdd()
        self.liste_mot_clef = []
        self.bind("<<ShowFrame>>", self.on_show_frame)
        self.recette = Recette()

        # Création de la fenetre

        self.button_back = tk.Button(self, text="Retour",
                                     command=lambda: controller.show_frame(Ecran_acceuil.Ecran_Accueil), font=Ct.FONT,
                                     bg=Ct.BG, fg=Ct.FG)
        self.button_back.pack()

        self.window = tk.Frame(self)
        self.window.config(background=Ct.BG)

        # initialization des composants

        # --- FRAME TITRE
        self.frame_titre = tk.Frame(self.window, bg=Ct.BG, bd=5, highlightbackground=Ct.FG, highlightthickness=1)
        # - Titre
        self.label = tk.Label(self.frame_titre, text="Titre: ", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.label.grid(row=0, column=0, sticky=tk.W)
        self.saisititre = tk.Entry(self.frame_titre, font=Ct.FONT, fg=Ct.FG_TEXTE, width=60)
        self.saisititre.grid(row=0, column=1, columnspan=5, sticky=tk.W)
        # - Note
        self.label = tk.Label(self.frame_titre, text="Note: ", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.label.grid(row=0, column=7, padx=10, sticky=tk.W)
        self.saisinote = tk.Spinbox(self.frame_titre, from_=0, to=10, font=Ct.FONT, fg=Ct.FG_TEXTE, width=5)
        self.saisinote.grid(row=0, column=8, sticky=tk.W)
        # - Nb personnes
        self.label = tk.Label(self.frame_titre, text="Nombre de personnes: ", font=Ct.FONT, bg=Ct.BG,
                              fg=Ct.FG)
        self.label.grid(row=1, column=0, pady=20, sticky=tk.W)
        self.saisinbpers = tk.Spinbox(self.frame_titre, from_=1, to=12, font=Ct.FONT, fg=Ct.FG_TEXTE, width=5)
        self.saisinbpers.grid(row=1, column=1, sticky=tk.W)
        # - Temps de preparation
        self.label = tk.Label(self.frame_titre, text="Temps préparation: ", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.label.grid(row=1, column=2, padx=10, sticky=tk.W)
        self.saisitpsprepa = tk.Entry(self.frame_titre, font=Ct.FONT, fg=Ct.FG_TEXTE, width=5)
        self.saisitpsprepa.grid(row=1, column=3, sticky=tk.W)
        # - Temps de cuisson
        self.label = tk.Label(self.frame_titre, text="Temps cuisson: ", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.label.grid(row=1, column=4, padx=10, sticky=tk.W)
        self.saisitpscuisson = tk.Entry(self.frame_titre, font=Ct.FONT, fg=Ct.FG_TEXTE, width=5)
        self.saisitpscuisson.grid(row=1, column=5, sticky=tk.W)
        # - Difficulté
        self.label = tk.Label(self.frame_titre, text="Difficulté: ", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.label.grid(row=1, column=6, padx=10, sticky=tk.W)
        self.saisidiff = tk.Spinbox(self.frame_titre, values=('Facile', 'Moyen', 'Difficile', 'Expert'),
                                    font=Ct.FONT, fg=Ct.FG_TEXTE, width=15)
        self.saisidiff.grid(row=1, column=7, columnspan=2, sticky=tk.W)
        # - URL
        self.label = tk.Label(self.frame_titre, text="URL: ", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.label.grid(row=2, column=0, sticky=tk.W)
        self.saisiurl = tk.Entry(self.frame_titre, font=Ct.FONT, fg=Ct.FG_TEXTE, width=90)
        self.saisiurl.grid(row=2, column=1, columnspan=10, sticky=tk.W)
        self.urlbouton = tk.Button(self.frame_titre, text="->", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG,
                                   command=self.openweb)
        self.urlbouton.grid(row=2, column=11, columnspan=10, sticky=tk.W)
        # --- FRAME TITRE FIN
        self.frame_titre.pack(pady=20, side=tk.TOP, fill=tk.X)

        # --- FRAME SAISI DES INGREDIENTS
        self.frame_saisi_ingredient = tk.Frame(self.window, bg=Ct.BG, bd=5, highlightbackground=Ct.FG,
                                               highlightthickness=1)

        # -- SS FRAME DETAIL INGREDIENT
        self.frame_detail_ing = tk.Frame(self.frame_saisi_ingredient, bd=4, bg=Ct.BG)
        # - label
        self.label = tk.Label(self.frame_detail_ing, justify=tk.LEFT, text="Sélection des ingrédients: ",
                              font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.label.grid(row=0, column=0, columnspan=2, sticky=tk.W)
        # --- Saisi nom
        self.label = tk.Label(self.frame_detail_ing, text="Nom ingrédient", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.label.grid(row=1, column=0, padx=20, sticky=tk.W)
        self.saisinom = AutocompleteCombobox(self.frame_detail_ing, font=Ct.FONT)
        self.saisinom.bind("<<ComboboxSelected>>", self.saisi_nom_ingredient)
        self.saisinom.bind("<Return>", self.saisi_nom_ingredient)
        self.saisinom.grid(row=1, column=1, padx=20, sticky=tk.W)
        self.ing_bouton = tk.Button(self.frame_detail_ing, text="+", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG,
                                    command=lambda: self.controller.show_frame(Ecran_Ingredient.Ecran_Ingredient))
        self.ing_bouton.grid(row=1, column=2, sticky=tk.W)

        # --- Saisi lieu
        self.label = tk.Label(self.frame_detail_ing, text="Lieu d'achat", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.label.grid(row=2, column=0, padx=20, sticky=tk.W)
        self.saisilieu = tk.Entry(self.frame_detail_ing, font=Ct.FONT, fg=Ct.FG_TEXTE, width=20)
        self.saisilieu.grid(row=2, column=1, padx=20, sticky=tk.W, columnspan=2)
        # --- Saisi nb ingrédient
        self.label = tk.Label(self.frame_detail_ing, text="Nombre", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.label.grid(row=3, column=0, padx=20, sticky=tk.W)
        self.saisinbing = tk.Entry(self.frame_detail_ing, font=Ct.FONT, fg=Ct.FG_TEXTE, width=20)
        self.saisinbing.grid(row=3, column=1, padx=20, sticky=tk.W, columnspan=2)
        # --- Saisi unité
        self.label = tk.Label(self.frame_detail_ing, text="Unité par défaut", font=Ct.FONT, bg=Ct.BG,
                              fg=Ct.FG)
        self.label.grid(row=4, column=0, padx=20, sticky=tk.W)
        self.saisiunite = tk.Entry(self.frame_detail_ing, font=Ct.FONT, fg=Ct.FG_TEXTE, width=20)
        self.saisiunite.grid(row=4, column=1, padx=20, sticky=tk.W, columnspan=2)
        # --- Saisi commentaire
        self.label = tk.Label(self.frame_detail_ing, text="Commentaire", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.label.grid(row=5, column=0, padx=20, sticky=tk.W)
        self.saisicomm = tk.Entry(self.frame_detail_ing, font=Ct.FONT, fg=Ct.FG_TEXTE, width=20)
        self.saisicomm.grid(row=5, column=1, padx=20, sticky=tk.W, columnspan=2)
        # -- SS FRAME DETAIL INGREDIENT FIN
        self.frame_detail_ing.grid(row=1, column=0, sticky=tk.W)

        # -- SS FRAME BOUTON INGREDIENT
        self.frame_bouton_ingredient = tk.Frame(self.frame_saisi_ingredient, bd=4, height=150, bg=Ct.BG)
        # --- Bouton ajout ingrédient
        self.add_ing = tk.Button(self.frame_bouton_ingredient, text="Ajouter à la recette", font=Ct.FONT,
                                 bg=Ct.BG, fg=Ct.FG, command=self.ajout_ingredient)
        self.add_ing.grid(row=0, column=0, columnspan=2, pady=5, sticky=tk.N)
        # --- Bouton retrait ingrédient
        self.mod_ing = tk.Button(self.frame_bouton_ingredient, text="Retirer l'ingrédient", font=Ct.FONT,
                                 bg=Ct.BG, fg=Ct.FG, command=self.mod_ingredient)
        self.mod_ing.grid(row=1, column=0, pady=10, sticky=tk.N)
        # --- Bouton retrait ingrédient
        self.supp_liste_ing = tk.Button(self.frame_bouton_ingredient, text="Vider la liste", font=Ct.FONT,
                                        bg=Ct.BG, fg=Ct.FG, command=self.supp_ingredient)
        self.supp_liste_ing.grid(row=2, column=0, pady=10, sticky=tk.N)
        # -- SS FRAME BOUTON INGREDIENT FIN
        self.frame_bouton_ingredient.grid(row=1, column=1, padx=5, sticky=tk.W)

        # -- SS FRAME LISTE INGREDIENT
        self.frame_list_ing_recette = tk.Frame(self.frame_saisi_ingredient, height=150, bg=Ct.BG)
        # - Liste des ingrédients de la recette
        self.lbox_recette = tk.Listbox(self.frame_list_ing_recette, bd=0, width=60, font=Ct.FONT,
                                       fg=Ct.FG_TEXTE, selectbackground=Ct.BG_SELECT)
        self.vscroll_recette = tk.Scrollbar(self.frame_list_ing_recette, command=self.lbox_recette.yview, bg=Ct.BG)
        self.lbox_recette.config(yscrollcommand=self.vscroll_recette.set)
        self.vscroll_recette.pack(side=tk.RIGHT, expand=tk.N, fill=tk.Y, padx=1, pady=1)
        self.lbox_recette.pack(side=tk.LEFT, padx=2, pady=2, fill=tk.X)
        # -- SS FRAME LISTE INGREDIENT FIN
        self.frame_list_ing_recette.grid(row=1, column=2)

        # --- FRAME SAISI DES INGREDIENTS FIN
        self.frame_saisi_ingredient.pack(side=tk.TOP, fill=tk.X, anchor=tk.W)

        # --- FRAME SAISI RECETTE
        self.frame_info_recette = tk.Frame(self.window, bg=Ct.BG, bd=5, highlightbackground=Ct.FG,
                                           highlightthickness=1)

        # -- SS FRAME SAISI MOT CLEFS
        self.frame_mot_recette = tk.Frame(self.frame_info_recette, bg=Ct.BG)
        # Saisi mot clefs
        self.label = tk.Label(self.frame_mot_recette, text="Ajout mots clef", font=Ct.FONT, bg=Ct.BG,
                              fg=Ct.FG)
        self.label.grid(row=0, column=0, sticky=tk.W)
        self.saisimotclef = AutocompleteCombobox(self.frame_mot_recette, font=Ct.FONT)
        self.saisimotclef.bind("<<ComboboxSelected>>", self.saisi_mot_clef)
        self.saisimotclef.bind("<Return>", self.saisi_mot_clef)
        self.saisimotclef.grid(row=1, column=0, sticky=tk.W)
        # Liste des mots clefs
        self.frame_list_mot_clef = tk.Frame(self.frame_mot_recette)
        self.lbox_motclef = tk.Listbox(self.frame_list_mot_clef, bd=0, width=20, font=Ct.FONT,
                                       fg=Ct.FG_TEXTE, selectbackground=Ct.BG_SELECT)
        self.vscroll_motclef = tk.Scrollbar(self.frame_list_mot_clef, command=self.lbox_motclef.yview, bg=Ct.BG)
        self.lbox_motclef.config(yscrollcommand=self.vscroll_motclef.set)
        self.lbox_motclef.bind("<<ListboxSelect>>", self.select_motclef)
        self.vscroll_motclef.pack(side=tk.RIGHT, expand=tk.N, fill=tk.Y, padx=1, pady=1)
        self.lbox_motclef.pack(side=tk.LEFT, padx=2, pady=2, fill=tk.X)
        self.frame_list_mot_clef.grid(row=2, column=0, pady=10, sticky=tk.W)
        # -- SS FRAME MOTS CLEFS FIN
        self.frame_mot_recette.grid(row=0, column=0, pady=10, padx=5, sticky=tk.NW)

        # -- SS FRAME SAISI TEXTE DE LA RECETTE
        self.frame_text_recette = tk.Frame(self.frame_info_recette, height=30, width=100, bg=Ct.BG)
        # Texte de la recette
        self.label = tk.Label(self.frame_text_recette, text="Recette:", font=Ct.FONT, bg='#972810', fg='white')
        self.label.pack(side=tk.LEFT, fill=tk.X, expand=tk.N, anchor=tk.W)
        self.texte_recette = tk.Text(self.frame_text_recette, height=15, bd=2, width=95, font=Ct.FONT,
                                     fg=Ct.FG_TEXTE)
        self.vscroll_recette_text = tk.Scrollbar(self.frame_text_recette, command=self.texte_recette.yview, bg=Ct.BG)
        self.texte_recette.config(yscrollcommand=self.vscroll_recette_text.set)
        self.vscroll_recette_text.pack(side=tk.RIGHT, expand=tk.N, fill=tk.Y, padx=1, pady=1)
        self.texte_recette.pack(side=tk.RIGHT, expand=tk.N, padx=1, pady=1)
        # -- SS FRAME SAISI TEXTE DE LA RECETTE FIN
        self.frame_text_recette.grid(row=0, column=1, padx=45)

        # -- SS FRAME SAISI COMMENTAIRE DE LA RECETTE
        self.frame_comm_recette = tk.Frame(self.frame_info_recette, height=30, width=123, bg=Ct.BG)
        # Texte de la recette
        self.label = tk.Label(self.frame_comm_recette, text="Commentaire:", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.label.pack(side=tk.LEFT, fill=tk.X, expand=tk.N, anchor=tk.W)
        self.comm_recette = tk.Text(self.frame_comm_recette, height=3, bd=2, width=118, font=Ct.FONT, fg=Ct.FG_TEXTE)
        self.vscroll_recette_comm = tk.Scrollbar(self.frame_comm_recette, command=self.comm_recette.yview, bg=Ct.BG)
        self.comm_recette.config(yscrollcommand=self.vscroll_recette_comm.set)
        self.vscroll_recette_comm.pack(side=tk.RIGHT, expand=tk.N, fill=tk.Y, padx=1, pady=1)
        self.comm_recette.pack(side=tk.RIGHT, expand=tk.N, padx=1, pady=1)
        # -- SS FRAME SAISI TEXTE DE LA RECETTE FIN
        self.frame_comm_recette.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)

        # --- FRAME SAISI RECETTE FIN
        self.frame_info_recette.pack(side=tk.TOP, fill=tk.X, pady=20, anchor=tk.W)

        # -- FRAME BOUTON ENREGISTREMENT
        self.frame_bouton_enregistrement = tk.Frame(self.window, bg=Ct.BG, bd=5, highlightbackground=Ct.FG,
                                                    highlightthickness=1)
        # --- Bouton Enregistrer
        self.save_recette = tk.Button(self.frame_bouton_enregistrement, text="Enregistrer", font=Ct.FONT,
                                      bg=Ct.BG, fg=Ct.FG, command=self.enregistrement_recette)
        self.save_recette.grid(row=0, column=0, columnspan=2, pady=5, sticky=tk.N)
        # --- FRAME BOUTON ENREGISTREMENT FIN
        self.frame_bouton_enregistrement.pack(side=tk.TOP, pady=20)

        self.window.pack(side=tk.TOP, pady=5)

    def execute(self):
        """Pas utilisé"""
        pass

    def cancel(self):
        """Pas utilisé: attention prévoir info sur nom enregistrement de la recette, ou enregistrement auto"""
        pass

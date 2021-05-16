"""Ecran d'accueil
"""
import datetime
import tkinter as tk
from tkinter import ttk

import Ressource.Classe.Constante as Ct
from Ressource.Classe.AutocompletComboBox import AutocompleteCombobox
from Ressource.Classe.Bdd import Bdd
from Ressource.Classe.Repas import Repas

import Ressource.Ecran.Ecran_Ingredient as Ecran_Ingredient
import Ressource.Ecran.Ecran_Liste_Recette as Ecran_Liste_Recette

# from Ressource.Classe.Recette import Recette
from Ressource.Classe.Ingredient import Ingredient


class Ecran_Accueil(tk.Frame):
    """Classe de l'écran d'accueil"""

    def liste_jour(self):
        """Mise a jour de la liste des jours a faire apparaitre sur le calendrier"""
        self.l_jours = []
        for i in range(self.nb_jour):
            dt = self.premier_jour + datetime.timedelta(days=i)
            self.l_jours.append(dt)

    def recup_liste_ingredient(self):
        """ Recuperation de la liste des ingredients et de la liste des noms d'ingrédient"""
        self.liste_ingredient_complete = self.bdd.get_liste_ingredients()
        self.liste_ingredient_complete = sorted(self.liste_ingredient_complete, key=lambda ingredient: ingredient.nom)
        self.liste_nom_ingredient = []
        for i in self.liste_ingredient_complete:
            if i.get_nom() not in self.liste_nom_ingredient:
                self.liste_nom_ingredient.append(i.get_nom())
        self.liste_nom_ingredient.sort()

    def recup_liste_recette(self):
        """Recuperation de la liste des recettes  depuis la BDD
           """
        self.liste_recette = self.bdd.get_liste_recette()
        self.liste_recette = sorted(self.liste_recette,
                                    key=lambda recette: recette.get_titre())
        self.liste_nom_recette = []
        for r in self.liste_recette:
            self.liste_nom_recette.append(r.get_titre())
        self.liste_nom_recette.sort()

    def affichage_detail_repas(self):
        """Affichage du détail du repas sélectionné"""
        dt = self.repas_select.get_date()
        d = dt.strftime("%d/%m/%y")
        jsem = Ct.JOURS[dt.weekday()]
        m = self.repas_select.get_moment()
        self.label_detail.config(text=f"Détail du repas du {jsem} {d} {m}")

        self.lbox_recette.delete(0, tk.END)
        for rec in self.repas_select.get_recettes():
            self.lbox_recette.insert(tk.END, rec.get_titre())
        for ing in self.repas_select.get_ingredients():
            self.lbox_recette.insert(tk.END, "{}: {} {} ({}) {}".format(ing.nom, ing.nb, ing.unite, ing.lieu,
                                                                        ing.commentaire))
        self.saisinbpers.delete(0, tk.END)
        self.saisinbpers.insert(0, self.repas_select.get_nbpersonnes())
        self.saisicomm_repas.delete(0, tk.END)
        self.saisicomm_repas.insert(0, self.repas_select.get_commentaire())

    def navig_avant(self):
        """Navigation Avant"""
        self.premier_jour=self.premier_jour-datetime.timedelta(days=self.nb_jour)
        self.liste_jour()
        self.affichage_calendrier()

    def navig_apres(self):
        """Navigation Apres"""
        self.premier_jour = self.premier_jour + datetime.timedelta(days=self.nb_jour)
        self.liste_jour()
        self.affichage_calendrier()

    def detail_repas(self, dt: datetime.date, m: str):
        """Affichage du détail du repas sélectionné"""
        self.repas_select = self.bdd.get_repas_date(date=dt, moment=m)
        self.affichage_calendrier()
        self.affichage_detail_repas()

    def menu_calendrier_do_popup(self, event, dt: datetime.date, m: str):
        """Affichage du menu qui est associé au click droit"""
        try:
            self.detail_repas(dt, m)
            self.menu_calendrier.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu_calendrier.grab_release()

    def affichage_calendrier(self):
        """Affichage du calendrier"""
        self.ss_frame_calendrier.destroy()
        self.ss_frame_calendrier = tk.Frame(self.frame_calendrier, bg=Ct.BG, bd=5, highlightbackground=Ct.FG,
                                            highlightthickness=1)
        self.ss_frame_calendrier.grid_columnconfigure(0, weight=1)
        self.ss_frame_calendrier.grid_columnconfigure(1, weight=10)
        self.ss_frame_calendrier.grid_columnconfigure(2, weight=10)
        frame_navigation = tk.Frame(self.ss_frame_calendrier, bg=Ct.BG)
        navig_avant_bouton = tk.Button(frame_navigation, text="Avant", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG,
                                       command=self.navig_avant)
        navig_avant_bouton.grid(row=0, column=0, padx=2, sticky=tk.W)
        navig_apres_bouton = tk.Button(frame_navigation, text="Après", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG,
                                       command=self.navig_apres)
        navig_apres_bouton.grid(row=0, column=1, padx=15, sticky=tk.W)
        frame_navigation.grid(row=0, column=0, sticky=tk.W)
        label = tk.Label(self.ss_frame_calendrier, text="Menu du midi", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        label.grid(row=0, column=1, sticky=tk.W)
        label = tk.Label(self.ss_frame_calendrier, text="Menu du soir", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        label.grid(row=0, column=2, sticky=tk.W)
        nb = 1
        for j in self.l_jours:
            ttk.Separator(self.ss_frame_calendrier, orient=tk.HORIZONTAL).grid(column=0, row=nb, columnspan=3,
                                                                               sticky='we')
            nb += 1
            jsem = Ct.JOURS[j.weekday()]
            dt = j.strftime("%d/%m")
            label = tk.Label(self.ss_frame_calendrier, text=f"{jsem} {dt}", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG, width=20,
                             height=3, anchor='w')
            if j == datetime.date.today():
                label.config(fg='yellow')
            label.grid(row=nb, column=0, sticky=tk.W)
            repas = '\n'.join(self.bdd.get_liste_menu_date(j, 'Midi'))
            if len(repas) < 2:
                repas = "----"
            label = tk.Label(self.ss_frame_calendrier, text=repas, font=Ct.FONT, bg=Ct.BG, fg=Ct.FG, anchor='w')
            if self.repas_select.get_date() == j and self.repas_select.get_moment() == 'Midi':
                label.configure(bg='red')
            elif self.repas_copie is not None:
                if self.repas_copie.get_date() == j and self.repas_copie.get_moment() == 'Midi':
                    label.configure(bg='orange')
            label.bind("<Button-1>", lambda e, d=j: self.detail_repas(d, 'Midi'))
            label.bind("<Button-3>", lambda e, d=j: self.menu_calendrier_do_popup(e, d, 'Midi'))
            label.grid(row=nb, column=1, sticky=tk.W)
            repas = '\n'.join(self.bdd.get_liste_menu_date(j, 'Soir'))
            if len(repas) < 2:
                repas = "----"
            label = tk.Label(self.ss_frame_calendrier, text=repas, font=Ct.FONT, bg=Ct.BG, fg=Ct.FG, anchor='w')
            if self.repas_select.get_date() == j and self.repas_select.get_moment() == 'Soir':
                label.configure(bg='red')
            elif self.repas_copie is not None:
                if self.repas_copie.get_date() == j and self.repas_copie.get_moment() == 'Soir':
                    label.configure(bg='orange')
            label.bind("<Button-1>", lambda e, d=j: self.detail_repas(d, 'Soir'))
            label.bind("<Button-3>", lambda e, d=j: self.menu_calendrier_do_popup(e, d, 'Soir'))
            label.grid(row=nb, column=2, sticky=tk.W)
            nb += 1
        self.ss_frame_calendrier.pack(side=tk.LEFT, expand=True, fill=tk.X)

    def afficher_detail_ingredient(self):
        """ Afficher le détail d'un ingrédient sélectionné"""
        for i in self.liste_ingredient_complete:
            if i.get_nom() == self.saisiingredient.get():
                self.saisilieu.delete(0, tk.END)
                self.saisilieu.insert(0, i.get_lieu())
                self.saisiunite.delete(0, tk.END)
                self.saisiunite.insert(0, i.get_unite())
                self.saisinbing.delete(0, tk.END)
                self.saisinbing.insert(0, str(i.get_nb()))
                self.saisicomm.delete(0, tk.END)
                self.saisicomm.insert(0, i.get_commentaire())

    def saisi_nom_ingredient(self, *event):
        """"Saisi ou sélection d'un nom ingrédient : récupération de l'id selectionné
            Affichage du détail de cet ingrédient"""
        self.afficher_detail_ingredient()
        self.saisinbing.focus()

    def add_ingredient(self):
        """Ajout d'un ingredient au repas"""
        try:
            nb = float(self.saisinbing.get())
        except ValueError:
            nb = 0
        if len(self.saisiingredient.get()) > 2:
            ing = Ingredient(nom=self.saisiingredient.get(), lieu=self.saisilieu.get(),
                             unite=self.saisiunite.get(), nb=nb, commentaire=self.saisicomm.get())
            self.repas_select.add_ingrediente(ing)
            self.saisiingredient.set('')
            self.saisilieu.delete(0, tk.END)
            self.saisiunite.delete(0, tk.END)
            self.saisicomm.delete(0, tk.END)
            self.saisinbing.delete(0, tk.END)
        self.affichage_detail_repas()

    def add_recette(self):
        """Ajout d'un ingredient au repas"""
        rec = self.saisirecette.current()
        if rec >= 0:
            self.repas_select.add_recette(self.liste_recette[rec])
            self.affichage_detail_repas()
            self.saisirecette.set('')

    def supp_recette(self):
        """Suppression d'un ingredient ou d'une recette du repas"""
        if self is not None and self.lbox_recette.curselection() != ():
            selection = self.lbox_recette.curselection()[0]
            print(selection)
            if selection < len(self.repas_select.get_recettes()):
                self.repas_select.supp_recette(selection)
            else:
                self.repas_select.supp_ingredient(selection-len(self.repas_select.get_recettes()))
            self.affichage_detail_repas()

    def save_repas_bdd(self):
        if self.repas_select.get_id() is None:
            id_repas = self.bdd.add_repas(self.repas_select)
            self.repas_select.set_id(id_repas)
        else:
            self.bdd.modif_repas(self.repas_select)
        self.affichage_calendrier()

    def save_repas_copie_bdd(self):
        if self.repas_copie.get_id() is None:
            id_repas = self.bdd.add_repas(self.repas_copie)
            self.repas_copie.set_id(id_repas)
        else:
            self.bdd.modif_repas(self.repas_copie)

    def save_repas(self):
        """Ajout d'un ingredient au repas"""
        self.repas_select.set_commentaire(self.saisicomm_repas.get())
        self.repas_select.set_nbpersonnes(self.saisinbpers.get())
        self.save_repas_bdd()

    def copie_selected(self):
        self.repas_copie = self.repas_select

    def colle_remplace_selected(self):
        if self.repas_copie is not None:
            self.repas_select.set_ingredients(self.repas_copie.get_ingredients())
            self.repas_select.set_recettes(self.repas_copie.get_recettes())
            self.repas_select.set_nbpersonnes(self.repas_copie.get_nbpersonnes())
            self.repas_select.set_commentaire(self.repas_copie.get_commentaire())
            self.repas_copie = None
            self.save_repas_bdd()
            self.affichage_detail_repas()

    def colle_ajoute_selected(self):
        if self.repas_copie is not None:
            self.repas_select.add_ingredients(self.repas_copie.get_ingredients())
            self.repas_select.add_recettes(self.repas_copie.get_recettes())
            self.repas_copie = None
            self.save_repas_bdd()
            self.affichage_detail_repas()

    def echange_selected(self):
        if self.repas_copie is not None:
            d=self.repas_select.get_date()
            m=self.repas_select.get_moment()
            self.repas_select.set_date(self.repas_copie.get_date())
            self.repas_select.set_moment(self.repas_copie.get_moment())
            self.repas_copie.set_date(d)
            self.repas_copie.set_moment(m)
            self.save_repas_copie_bdd()
            self.repas_copie = None
            self.save_repas_bdd()
            self.affichage_detail_repas()


    def supprime_selected(self):
        if self.repas_select.get_id() is not None:
            self.bdd.supp_repas(self.repas_select.get_id())
            self.detail_repas(self.repas_select.get_date(), self.repas_select.get_moment())
            self.repas_copie = None

    def on_show_frame(self, event):
        """Initialisation de la fenetre """
        self.recup_liste_ingredient()
        self.recup_liste_recette()
        self.saisirecette.set_completion_list(self.liste_nom_recette)
        self.saisiingredient.set_completion_list(self.liste_nom_ingredient)
        # recupération de l'écran précédent
        ecran_origine = self.controller.frame_prec
        if ecran_origine == "Ecran_Liste_Recette":
            rec = self.controller.get_page(ecran_origine).lbox_recette.curselection()
            if rec is not None and rec != ():
                selection = rec[0]
                id_recette = self.controller.get_page(ecran_origine).liste_recette_affiche[selection].get_id()
                index = 0
                for r in self.liste_recette:
                    if r.get_id() == id_recette:
                        break
                    index += 1
                self.saisirecette.current(index)

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent, bg=Ct.BG)
        # Init variable
        self.nb_jour = 7
        self.l_jours = []
        self.bdd = Bdd()
        self.liste_ingredient_complete = []
        self.liste_nom_ingredient = []
        self.liste_recette = []
        self.liste_nom_recette = []
        self.bind("<<ShowFrame>>", self.on_show_frame)
        self.repas_copie = None

        # Récupération du samedi de la semaine
        dt = datetime.date.today()
        self.premier_jour = dt - datetime.timedelta(days=(dt.isoweekday() + 1) % 7)
        if datetime.datetime.now().hour <= 14:
            self.repas_select = Repas(date=dt, moment='Midi')
        else:
            self.repas_select = Repas(date=dt, moment='Soir')
        # Récupération de la liste des jours
        self.liste_jour()

        # Création de la fenetre
        self.window = tk.Frame(self, bg=Ct.BG)

        # Création du menu pop up au clik sur un label du calendrier
        self.menu_calendrier = tk.Menu(self.window, tearoff=0)
        self.menu_calendrier.add_command(label="Copier",
                                         command=self.copie_selected)
        self.menu_calendrier.add_command(label="Coller-Remplacer",
                                         command=self.colle_remplace_selected)
        self.menu_calendrier.add_command(label="Ajouter les recettes",
                                         command=self.colle_ajoute_selected)
        self.menu_calendrier.add_command(label="Echanger",
                                         command=self.echange_selected)
        self.menu_calendrier.add_separator()
        self.menu_calendrier.add_command(label="Supprimer",
                                         command=self.supprime_selected)

        # Affichage de la partie calendrier
        self.frame_calendrier = tk.Frame(self.window, bg=Ct.BG)
        self.ss_frame_calendrier = tk.Frame(self.frame_calendrier, bg=Ct.BG, bd=5, highlightbackground=Ct.FG,
                                            highlightthickness=1)
        self.frame_calendrier.pack(padx=10, pady=10, fill=tk.X)

        # Affichage de la partie détail
        self.frame_detail = tk.Frame(self.window, bg=Ct.BG, bd=30, highlightbackground=Ct.FG,
                                     highlightthickness=1)
        self.label_detail = tk.Label(self.frame_detail, text="Sélectionnez un repas", font=Ct.FONT, bg=Ct.BG,
                                     width=40, fg=Ct.FG)
        self.label_detail.grid(column=0, row=0, sticky=tk.W)
        self.label = tk.Label(self.frame_detail, text="Nombre de personnes: ", font=Ct.FONT, bg=Ct.BG,
                              fg=Ct.FG)
        self.label.grid(row=0, column=1, pady=20, sticky=tk.E)
        self.saisinbpers = tk.Spinbox(self.frame_detail, from_=1, to=99, font=Ct.FONT, fg=Ct.FG_TEXTE, width=5)
        self.saisinbpers.grid(row=0, column=2, sticky=tk.W)
        self.enregistrement_repas = tk.Button(self.frame_detail, text="ENREGISTRER", font=Ct.FONT, bg=Ct.BG,
                                              fg=Ct.FG, command=self.save_repas)
        self.enregistrement_repas.grid(row=0, column=3, padx=10, sticky=tk.W)

        # liste des recettes
        self.frame_liste_recette = tk.Frame(self.frame_detail, bg=Ct.BG)
        self.lbox_recette = tk.Listbox(self.frame_liste_recette, bd=2, width=100, height=12, font=Ct.FONT,
                                       fg=Ct.FG_TEXTE, selectbackground=Ct.BG_SELECT, exportselection=tk.FALSE)
        self.vscroll_recette = tk.Scrollbar(self.frame_liste_recette, command=self.lbox_recette.yview, bg=Ct.BG)
        self.lbox_recette.config(yscrollcommand=self.vscroll_recette.set)
        self.vscroll_recette.pack(side=tk.RIGHT, expand=tk.N, fill=tk.Y, padx=1, pady=1)
        self.lbox_recette.pack(side=tk.LEFT, padx=2, pady=2)
        self.suppression_recette = tk.Button(self.frame_detail, text="SUPPRIMER", font=Ct.FONT, bg=Ct.BG,
                                             fg=Ct.FG, command=self.supp_recette)
        self.suppression_recette.grid(column=0, row=3,  sticky=tk.E)
        self.label = tk.Label(self.frame_detail, text="Commentaire: ", font=Ct.FONT, bg=Ct.BG,
                              fg=Ct.FG)
        self.label.grid(row=4, column=0, pady=20, sticky=tk.E)

        self.saisicomm_repas = tk.Entry(self.frame_detail, font=Ct.FONT, fg=Ct.FG_TEXTE, width=50)
        self.saisicomm_repas.grid(row=4, column=1, pady=20, sticky=tk.W, columnspan=2)

        self.frame_liste_recette.grid(column=0, row=1, columnspan=3, rowspan=2, sticky=tk.W)

        self.frame_ajout_recette = tk.Frame(self.frame_detail, bg=Ct.BG)
        # Ajout Recette
        self.label = tk.Label(self.frame_ajout_recette, text="Ajout recette:", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.label.grid(row=0, column=0, columnspan=2, padx=2, sticky=tk.W)
        self.ajout_recette_bouton = tk.Button(self.frame_ajout_recette, text="<-", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG,
                                              command=self.add_recette)
        self.ajout_recette_bouton.grid(row=1, column=0, padx=2, sticky=tk.W)
        self.saisirecette = AutocompleteCombobox(self.frame_ajout_recette, font=Ct.FONT, width=60)
        self.saisirecette.grid(row=1, column=1, padx=2, sticky=tk.W, columnspan=2)
        # recherche recette
        self.recherche_recette = tk.Button(self.frame_ajout_recette, text="?", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG,
                                           command=lambda:
                                           self.controller.show_frame(Ecran_Liste_Recette.Ecran_Liste_Recette))
        self.recherche_recette.grid(row=1, column=3, sticky=tk.W)

        # Ajout ingredient
        self.label = tk.Label(self.frame_ajout_recette, text="Ajout ingredient:", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.label.grid(row=2, column=0, columnspan=2, padx=2, pady=10, sticky=tk.W)
        # bouton ajout recette
        self.ajout_ingredient_bouton = tk.Button(self.frame_ajout_recette, text="<-", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG,
                                                 command=self.add_ingredient)
        self.ajout_ingredient_bouton.grid(row=3, column=0, padx=2, sticky=tk.W)
        # Choix ingrédient
        self.saisiingredient = AutocompleteCombobox(self.frame_ajout_recette, font=Ct.FONT, width=60)
        self.saisiingredient.bind("<<ComboboxSelected>>", self.saisi_nom_ingredient)
        self.saisiingredient.bind("<Return>", self.saisi_nom_ingredient)
        self.saisiingredient.grid(row=3, column=1, padx=2, columnspan=2, sticky=tk.W)
        # Enregistrement nouvel ingrédient
        self.ing_bouton = tk.Button(self.frame_ajout_recette, text="+", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG,
                                    command=lambda: self.controller.show_frame(Ecran_Ingredient.Ecran_Ingredient))
        self.ing_bouton.grid(row=3, column=3, sticky=tk.W)
        # --- Saisi lieu
        self.label = tk.Label(self.frame_ajout_recette, text="Lieu d'achat", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.label.grid(row=4, column=1, padx=20, sticky=tk.W)
        self.saisilieu = tk.Entry(self.frame_ajout_recette, font=Ct.FONT, fg=Ct.FG_TEXTE, width=40)
        self.saisilieu.grid(row=4, column=2, padx=20, sticky=tk.W, columnspan=2)
        # --- Saisi nb ingrédient
        self.label = tk.Label(self.frame_ajout_recette, text="Nombre", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.label.grid(row=5, column=1, padx=20, sticky=tk.W)
        self.saisinbing = tk.Entry(self.frame_ajout_recette, font=Ct.FONT, fg=Ct.FG_TEXTE, width=40)
        self.saisinbing.grid(row=5, column=2, padx=20, sticky=tk.W, columnspan=2)
        # --- Saisi unité
        self.label = tk.Label(self.frame_ajout_recette, text="Unité par défaut", font=Ct.FONT, bg=Ct.BG,
                              fg=Ct.FG)
        self.label.grid(row=6, column=1, padx=20, sticky=tk.W)
        self.saisiunite = tk.Entry(self.frame_ajout_recette, font=Ct.FONT, fg=Ct.FG_TEXTE, width=40)
        self.saisiunite.grid(row=6, column=2, padx=20, sticky=tk.W, columnspan=2)
        # --- Saisi commentaire
        self.label = tk.Label(self.frame_ajout_recette, text="Commentaire", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.label.grid(row=7, column=1, padx=20, sticky=tk.W)
        self.saisicomm = tk.Entry(self.frame_ajout_recette, font=Ct.FONT, fg=Ct.FG_TEXTE, width=40)
        self.saisicomm.grid(row=7, column=2, padx=20, sticky=tk.W, columnspan=2)

        self.frame_ajout_recette.grid(column=3, row=1, padx=20, sticky=tk.W)
        self.frame_detail.pack(padx=35, pady=5, fill=tk.X)
        self.window.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.detail_repas(self.repas_select.get_date(), self.repas_select.get_moment())
        self.recup_liste_ingredient()
        self.saisiingredient.set_completion_list(self.liste_nom_ingredient)
        self.recup_liste_recette()
        self.saisirecette.set_completion_list(self.liste_nom_recette)

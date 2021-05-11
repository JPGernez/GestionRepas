"""Ecran d'accueil
"""
import datetime
import tkinter as tk

import Ressource.Classe.Constante as Ct
from Ressource.Classe.AutocompletComboBox import AutocompleteCombobox
from Ressource.Classe.Bdd import Bdd
from Ressource.Classe.Repas import Repas
from Ressource.Classe.Recette import Recette
from Ressource.Classe.Ingredient import Ingredient


class Ecran_Accueil(tk.Frame):
    """Classe de l'écran d'accueil"""

    def liste_jour(self):
        """Mise a jour de la liste des jours a faire apparaitre"""
        self.l_jours = []
        for i in range(self.nb_jour):
            self.l_jours.append(self.premier_jour + datetime.timedelta(days=i))

    def detail_repas(self, dt: datetime.date, m: str):
        """Affichage du détail du repas sélectionné"""
        d = dt.strftime("%d/%m/%y")
        self.label_detail.config(text=f"Détail du repas du {d} {m}")
        self.repas_select = self.bdd.get_repas_date(date=dt, moment=m)

    def affichage_calendrier(self):
        """Affichage du calendrier"""
        f = tk.Frame(self.frame_calendrier, bg=Ct.BG, bd=5, highlightbackground=Ct.FG, highlightthickness=1)
        f.grid_columnconfigure(0, weight=1)
        f.grid_columnconfigure(1, weight=10)
        f.grid_columnconfigure(2, weight=10)
        label = tk.Label(f, text="Menu du midi", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        label.grid(row=0, column=1, sticky=tk.W)
        label = tk.Label(f, text="Menu du soir", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        label.grid(row=0, column=2, sticky=tk.W)
        nb = 1
        for j in self.l_jours:
            jsem = Ct.JOURS[j.weekday()]
            dt = j.strftime("%d/%m")
            label = tk.Label(f, text=f"{jsem} {dt}", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG, width=20, height=2)
            if j == datetime.date.today():
                label.config(fg='yellow')
            label.grid(row=nb, column=0, sticky=tk.W)
            repas = '\n'.join(self.bdd.get_liste_menu_date(dt, 'Midi'))
            if len(repas) < 2:
                repas = "Rien de prévu"
            label = tk.Label(f, text=repas, font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
            label.bind("<Button-1>", lambda e, d=j: self.detail_repas(d, 'Midi'))
            label.grid(row=nb, column=1, sticky=tk.W)
            repas = '\n'.join(self.bdd.get_liste_menu_date(dt, 'Soir'))
            if len(repas) < 2:
                repas = "Rien de prévu"
            label = tk.Label(f, text=repas, font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
            label.bind("<Button-1>", lambda e, d=j: self.detail_repas(d, 'Soir'))
            label.grid(row=nb, column=2, sticky=tk.W)
            nb += 1
        f.pack(side=tk.LEFT, expand=True, fill=tk.X)

    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self, parent, bg=Ct.BG)
        # Init variable
        self.nb_jour = 7
        self.l_jours = []
        self.bdd = Bdd()
        self.repas_select = Repas()

        # Récupération du samedi de la semaine
        dt = datetime.date.today()
        self.premier_jour = dt - datetime.timedelta(days=(dt.isoweekday() + 1) % 7)

        # Récupération de la liste des jours
        self.liste_jour()

        # Création de la fenetre
        self.window = tk.Frame(self, bg=Ct.BG)

        # Affichage de la partie calendrier
        self.frame_calendrier = tk.Frame(self.window, bg=Ct.BG)
        self.affichage_calendrier()
        self.frame_calendrier.pack(padx=10, pady=10, fill=tk.X)

        # Affichage de la partie détail
        self.frame_detail = tk.Frame(self.window, bg=Ct.BG)
        self.label_detail = tk.Label(self.frame_detail, text="Sélectionnez un repas", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.label_detail.grid(column=0, row=0, sticky=tk.W)

        # liste des recettes
        self.frame_liste_recette = tk.Frame(self.frame_detail, bg=Ct.BG)
        self.lbox_recette = tk.Listbox(self.frame_liste_recette, bd=2, width=100, font=Ct.FONT, fg=Ct.FG_TEXTE,
                                       selectbackground=Ct.BG_SELECT, exportselection=tk.FALSE)
        self.vscroll_recette = tk.Scrollbar(self.frame_liste_recette, command=self.lbox_recette.yview, bg=Ct.BG)
        self.lbox_recette.config(yscrollcommand=self.vscroll_recette.set)
        self.vscroll_recette.pack(side=tk.RIGHT, expand=tk.N, fill=tk.Y, padx=1, pady=1)
        self.lbox_recette.pack(side=tk.LEFT, padx=2, pady=2)
        self.frame_liste_recette.grid(column=0, row=1, rowspan=2, sticky=tk.W)

        self.frame_ajout_recette = tk.Frame(self.frame_detail, bg=Ct.BG)
        self.label = tk.Label(self.frame_ajout_recette, text="Ajout recette:", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.label.grid(row=0, column=0, columnspan=2, padx=2, sticky=tk.W)
        self.ajout_recette_bouton = tk.Button(self.frame_ajout_recette, text="<-", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.ajout_recette_bouton.grid(row=1, column=0, padx=2, sticky=tk.W)
        self.saisirecette = AutocompleteCombobox(self.frame_ajout_recette, font=Ct.FONT)
        self.saisirecette.grid(row=1, column=1, padx=2, sticky=tk.W)
        self.label = tk.Label(self.frame_ajout_recette, text="Ajout ingredient:", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.label.grid(row=2, column=0, columnspan=2, padx=2, pady=10, sticky=tk.W)
        self.ajout_ingredient_bouton = tk.Button(self.frame_ajout_recette, text="<-", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.ajout_ingredient_bouton.grid(row=3, column=0, padx=2, sticky=tk.W)
        self.saisiingredient = AutocompleteCombobox(self.frame_ajout_recette, font=Ct.FONT)
        self.saisiingredient.grid(row=3, column=1, padx=2, sticky=tk.W)

        self.frame_ajout_recette.grid(column=1, row=1, sticky=tk.W)

        self.frame_detail.pack(padx=2, pady=2, fill=tk.X)
        self.window.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.detail_repas(self.premier_jour, 'Midi')

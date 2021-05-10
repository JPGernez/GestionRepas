"""Ecran d'accueil
"""
import datetime
import tkinter as tk

import Ressource.Classe.Constante as Ct


class Ecran_Accueil(tk.Frame):
    """Classe de l'écran d'accueil"""

    def liste_jour(self):
        """Mise a jour de la liste des jours a faire apparaitre"""
        self.l_jours = []
        for i in range(self.nb_jour):
            self.l_jours.append(self.premier_jour + datetime.timedelta(days=i))

    def detail_repas(self, dt: datetime, m: str):
        """Affichage du détail du repas sélectionné"""
        d = dt.strftime("%d/%m/%y")
        self.label_detail.config(text=f"Détail du repas du {d} {m}")

    def affichage_calendrier(self):
        """Affichage du calendrier"""
        f = tk.Frame(self.calendrier, bg=Ct.BG, bd=5, highlightbackground=Ct.FG, highlightthickness=1)
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
            label = tk.Label(f, text=f"{jsem} {dt}", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG, width=20, height=3)
            if j == datetime.date.today():
                label.config(fg='yellow')
            label.grid(row=nb, column=0, sticky=tk.W)
            label = tk.Label(f, text="Rien de prévu", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
            label.bind("<Button-1>", lambda e, d=j: self.detail_repas(d, 'Midi'))
            label.grid(row=nb, column=1, sticky=tk.W)
            label = tk.Label(f, text="Rien de prévu", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
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

        # Récupération du samedi de la semaine
        dt = datetime.date.today()
        self.premier_jour = dt - datetime.timedelta(days=(dt.isoweekday() + 1) % 7)

        # Récupération de la liste des jours
        self.liste_jour()

        # Création de la fenetre
        self.window = tk.Frame(self, bg=Ct.BG)

        # Affichage de la partie calendrier
        self.calendrier = tk.Frame(self.window, bg=Ct.BG)
        self.affichage_calendrier()
        self.calendrier.pack(padx=10, pady=10, fill=tk.X)

        # Affichage de la partie détail
        self.detail = tk.Frame(self.window, bg=Ct.BG)
        self.label_detail = tk.Label(self.detail, text="Sélectionnez un repas", font=Ct.FONT, bg=Ct.BG, fg=Ct.FG)
        self.label_detail.pack()

        # liste des recettes
        self.lbox_recette = tk.Listbox(self.detail, bd=2, width=50, font=Ct.FONT, fg=Ct.FG_TEXTE,
                                       selectbackground=Ct.BG_SELECT, exportselection=tk.FALSE)
        self.vscroll_recette = tk.Scrollbar(self.detail, command=self.lbox_recette.yview, bg=Ct.BG)
        self.lbox_recette.config(yscrollcommand=self.vscroll_recette.set)
        self.vscroll_recette.pack(side=tk.RIGHT, expand=tk.N, fill=tk.Y, padx=1, pady=1)
        self.lbox_recette.pack(side=tk.LEFT, padx=2, pady=2, fill=tk.Y)

        self.detail.pack()
        self.window.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

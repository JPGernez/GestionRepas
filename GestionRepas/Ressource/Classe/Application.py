""" Lancement des différents écrans
"""

import tkinter as tk

import Ressource.Ecran.Ecran_Accueil as Ecran_acceuil
import Ressource.Ecran.Ecran_Ingredient as Ecran_ingredient
import Ressource.Ecran.Ecran_Liste_Recette as Ecran_liste_recettes
import Ressource.Ecran.Ecran_Recette as Ecran_Recette

import Ressource.Classe.Constante as Ct


class Application(tk.Tk):
    """Classe de lancement de l'application
    """

    def create_menubar(self):
        """tk.Menu de l'application"""
        menubar = tk.Menu(self, fg=Ct.FG_TEXTE)

        menufile = tk.Menu(menubar, tearoff=0, fg=Ct.FG_TEXTE)
        menufile.add_command(label="Liste des ingrédients",
                             command=lambda: self.show_frame(Ecran_ingredient.Ecran_Ingredient))
        menufile.add_command(label="Liste des recettes",
                             command=lambda: self.show_frame(Ecran_liste_recettes.Ecran_Liste_Recette))
        menufile.add_separator()
        menufile.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="Options", menu=menufile)
        self.config(menu=menubar)

    def get_page(self, classname):
        """Returns an instance of a page given it's class name as a string"""
        for page in self.frames.values():
            if str(page.__class__.__name__) == classname:
                return page
        return None

    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("1500x900+10+10")
        self.minsize(1800, 950)
        self.iconbitmap("../../Ressource/Image/pimientorojo.ico")
        self.config(background=Ct.BG)
        self.title("APPLICATION DE GESTION DES RECETTES DE LA SEMAINE")
        container = tk.Frame(self, bd=4, bg=Ct.BG)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Ecran_acceuil.Ecran_Accueil, Ecran_ingredient.Ecran_Ingredient,
                  Ecran_liste_recettes.Ecran_Liste_Recette, Ecran_Recette.Ecran_Recette):
            frame = F(container, self)
            self.frames[F] = frame
            frame.config(background=Ct.BG)
            frame.grid(row=0, column=0, sticky="nsew")

        self.create_menubar()
        self.frame_encours = ""
        self.frame_prec = ""
        self.cont_encours = ""
        self.cont_prec = ""

        self.show_frame(Ecran_acceuil.Ecran_Accueil)

    def show_frame(self, cont):
        """Ouverture des différnts écrans"""
        self.cont_prec = self.cont_encours
        self.cont_encours = cont
        frame = self.frames[cont]
        frame.tkraise()
        self.frame_prec = self.frame_encours
        self.frame_encours = frame.__class__.__name__
        frame.event_generate("<<ShowFrame>>")


if __name__ == "__main__":
    app = Application()
    app.mainloop()

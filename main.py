import tkinter as tk
from lists import *
from move_set import *
from check_pos import *
#--------------------------------------------------------------CLASSES----------------------------------------------------------------------------
class Barre:
    def __init__(self, nb):
        """Constructeur de la classe qui corespond à une barre"""
        self.nombre = nb
        self.list = Pile()
        self.pos = [0,0]
        self.creation_barres()

    def creation_barres(self):
        """Fonction qui s'occupe de la creation de la partie visuelle des barres"""
        col_barre = "black"
        #position en x
        depart_x = largeur//6 
        un_tier_fenetre=largeur//3
        eppaisseur = 10
        self.pos[0] = depart_x+(self.nombre-1)*un_tier_fenetre+eppaisseur//2
        #position en y
        depart_y = 50
        hauteur_barre = 300
        self.pos[1] = depart_y+hauteur_barre
        #creation des rectangles
        toile.create_rectangle(depart_x+(self.nombre-1)*un_tier_fenetre-eppaisseur//2, depart_y,depart_x+(self.nombre-1)*un_tier_fenetre+eppaisseur//2, depart_y+hauteur_barre, fill=col_barre)


class Anneau:
    def __init__(self, nb):
        """Constructeur de la classe qui correspond à un anneau"""
        self.nombre=nb
        self.barre_id = 0
        
        self.body = None
        self.pos = [0,0]
        self.origin_pos = [0,0]
        self.taille = [0,0]
        self.creation_anneau()

        self.bouge = False
        self.func = None
        #ajoute l'anneau a la pile de depart:
        liste_barres[self.barre_id].list.ajouter(self)

    def creation_anneau(self):
        """Fonction qui créée un anneau de manière visuelle"""
        bas_barre = 220+(6-nb_anneaux)*20
        list_col=["red","blue","green","purple","yellow","brown"]

        col_ann = list_col[self.nombre-1]
        #position et taille en x
        self.pos[0] = largeur//6
        self.taille[0] = self.nombre*10
        #position et taille en y
        self.pos[1] = bas_barre+self.nombre*20
        self.taille[1] = 10
        self.origin_pos = self.pos
        self.body = toile.create_rectangle(self.pos[0]-self.taille[0],self.pos[1]-self.taille[1],self.pos[0]+self.taille[0],self.pos[1]+self.taille[1], fill=col_ann)

    def movement_anneau(self,direction, arrive, barre_id):
        """Fonction qui permet de deplacer l'anneau dans la barre"""
        if barre_id != self.barre_id: #on verifie qu'il a deja ete ajouté a la liste
            liste_barres[self.barre_id].list.enlever() #toujours celui tout en haut
            self.barre_id=barre_id
            liste_barres[self.barre_id].list.ajouter(self)

        #nouvelle direction
        x = direction[0]
        y = direction[1]
        self.pos = [self.pos[0]+x,self.pos[1]+y]
        toile.move(self.body,x,y)
        self.func = toile.after(17, self.movement_anneau, direction, arrive,self.barre_id)
        #on est arrivé
        if abs(arrive[0]-self.pos[0]) < 2 and abs(arrive[1]-self.pos[1]) < 1:
            toile.after_cancel(self.func)
            self.bouge=False

    def movement_haut_anneau(self, direction, arrive, barre_id, arrive_next_y):
        """Fonction qui correspond au déplacement de l'anneau en haut de la barre"""
        self.bouge=True
        
        #on le change de pile par rapport aux barres
        if barre_id != self.barre_id: #on verifie qu'il a deja ete ajouté a la liste
            liste_barres[self.barre_id].list.enlever() #toujours celui tout en haut
            self.barre_id=barre_id
            liste_barres[self.barre_id].list.ajouter(self)

        x = direction[0]
        y = direction[1]
        
        self.pos = [self.pos[0]+x,self.pos[1]+y]
        toile.move(self.body,x,y)
        self.func = toile.after(17, self.movement_haut_anneau, direction, arrive,self.barre_id, arrive_next_y)

        #on est arrivé a destination
        if abs(arrive[0]-self.pos[0]) < 1 and abs(arrive[1]-self.pos[1]) < 1:
            toile.after_cancel(self.func)
            arrive_next = [arrive[0],arrive_next_y]
            
            #direction
            n_x = (arrive_next[0]-self.pos[0])/50
            n_y = (arrive_next[1]-self.pos[1])/50
            dir_next = [n_x,n_y]
            #deuxième partie du voyage
            self.movement_anneau(dir_next,arrive_next, barre_id)
        
    def reset_pos(self):
        """Fonction qui permet de reset la position et les variables des anneaux"""
        self.bouge=False
        self.pos=self.origin_pos
        toile.coords(self.body,self.pos[0]-self.taille[0],self.pos[1]-self.taille[1],self.pos[0]+self.taille[0],self.pos[1]+self.taille[1])
        liste_barres[self.barre_id].list.enlever() #toujours celui tout en haut
        self.barre_id=0
        liste_barres[self.barre_id].list.ajouter(self)
        if self.func != None:
            toile.after_cancel(self.func)
            self.func=None



#-------------------------------------------------------------FONCTIONS---------------------------------------------------------------------------
 # main code :
def reset():
    """Fonction qui permet de reset le code pour être pret à redémarer les déplacements"""
    global deplacements
    deplacements=deplacements_depart.copy()
    for ann in liste_anneaux:
        ann.reset_pos()

def update():
    """Fonction qui est appelé pour update la position des blocs"""
    if deplacements.taille() >= 1 and liste_anneaux[deplacements.verifie()-1].bouge == False:
        ann,barre=deplacements.enlever()
        #on recupère les bons ids
        ann-=1
        barre-=1

        #determine l'endroit d'arrivée
        pos=liste_barres[barre].pos
        x_arrive = pos[0]-5
        y_arrive = pos[1]-liste_barres[barre].list.taille()*20-10
        
        #direction
        x = (x_arrive-liste_anneaux[ann].pos[0])/50
        y = (haut_barre-liste_anneaux[ann].pos[1])/50
        liste_anneaux[ann].movement_haut_anneau((x,y),(x_arrive,haut_barre),barre, y_arrive)

def socle_visuel():
    """Fonction qui créée un socle en bas de la fenètre"""
    #en bas de la fenètre
    col_barre = "black"
    depart_x = largeur//6 
    eppaisseur = 10
    depart_y = 50
    toile.create_rectangle(depart_x//2,hauteur-depart_y,largeur-depart_x//2,hauteur-depart_y+eppaisseur, fill=col_barre)

 # deplacements des anneaux :
def select_anneau():
    """Fonction qui selectionne l'anneau à partir du curseur"""
    global selected_anneau
    deja_choisi = False
    for anneau in liste_anneaux:
        pos = anneau.pos
        taille = anneau.taille
        #on regarde si la position de l'anneau correspond à celle du curseur
        if verifie_pos(mouse_pos,pos,taille):
            if selected_anneau != None:
                unselect_anim(selected_anneau)

            deja_choisi=True
            selected_anneau = anneau
            select_anim(selected_anneau)
        #sinon on désélectionne l'anneau
        elif deja_choisi == False:
            if selected_anneau != None:
                unselect_anim(selected_anneau)
            selected_anneau = None

def select_anim(ann):
    """animation grossissant la bordure de l'anneau"""
    toile.itemconfig(ann.body, width=5)

def unselect_anim(ann):
    """animation rétrécissant la bordure de l'anneau"""
    toile.itemconfig(ann.body, width=1)

 # pression des touches :
def motion(event):
    """Fonction qui récupère la position de la souris a chaque fois qu'elle se déplace"""
    global mouse_pos
    mouse_pos = (event.x, event.y)

def clic_gauche(event):
    """Fonction qui s'active lors d'un clique"""
    select_anneau()

#---------------------------------------------------------------MAIN------------------------------------------------------------------------------
nb_anneaux = 4

#global var
largeur = 600
hauteur = 400

fenetre = tk.Tk()
toile = tk.Canvas(fenetre, width = largeur, height = hauteur, bg = "white")
toile.pack()

#deplacements manuels
mouse_pos = (0,0)
selected_anneau = None
haut_barre=40 #corespond à la hauteur des barres

#stockage des anneaux sur les barres
liste_barres = [Barre(1),Barre(2),Barre(3)] #liste de toutes les barres


#stockage des anneaux
liste_id_anneaux = [1 for i in range(nb_anneaux)]
liste_anneaux = [Anneau(i) for i in range(1,nb_anneaux+1)]

#stockage des deplacements
deplacements_depart = recursion(liste_id_anneaux,File(),3,nb_anneaux, True)
deplacements = deplacements_depart.copy()
print(deplacements)

#creation des autres visuels
socle_visuel()

#bouttons
suivant = tk.Button(fenetre, cursor="arrow", width=20, height=1, text = "NEXT", command = update)
suivant.pack()
reset_button = tk.Button(fenetre, cursor="arrow", width=20, height=1, text = "RESET", command = reset)
reset_button.pack()
boutton_quit = tk.Button(fenetre, cursor="arrow", width=20, height=1, text = "QUIT", command = fenetre.destroy)
boutton_quit.pack()
fenetre.bind('<Motion>', motion)
fenetre.bind('<Button-1>', clic_gauche)
fenetre.mainloop()
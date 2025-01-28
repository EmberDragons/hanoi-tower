from lists import *


def recursion(liste_anneaux,deplacements=File(),precendent_pos=1,profondeur=1, venir=False):
    """Fonction récursive qui permet la création de la liste des movements
    Concept très simple: 
        1. Recursion jusqu'à profondeur = 1 (le premier) + envoie de notre position + venir = False (aller a l'autre endroit)
        2. Deplacement de notre anneau
        3. 2eme recursion jusqu'à 1 + envoie de notre position + venir=True (aller)"""
    #deplacement
    prochaine_barre = pos_selection(liste_anneaux[profondeur-1], precendent_pos)
    if venir == True: #alors il faut se délacer au même endroit que l'anneau précédent
        prochaine_barre = precendent_pos

    if profondeur == 1: #plus de recursion
        deplacements.ajouter((profondeur,prochaine_barre))
        liste_anneaux[profondeur-1] = prochaine_barre
        return deplacements
    else:
        #1.
        deplacements = recursion(liste_anneaux,deplacements,prochaine_barre,profondeur-1)
        #2.
        deplacements.ajouter((profondeur,prochaine_barre))
        liste_anneaux[profondeur-1] = prochaine_barre
        #3.
        return recursion(liste_anneaux,deplacements,prochaine_barre,profondeur-1,True)

def pos_selection(pos1, pos2):
    """Fonction qui sélectionne la barre sur laquelle aller si les 2 autres sont prises"""
    our_pos=1
    if pos1 == 1:
        if pos2==2:
            our_pos=3
        if pos2==3:
            our_pos=2
    if pos1 == 2:
        if pos2==1:
            our_pos=3
        if pos2==3:
            our_pos=1
    if pos1 == 3:
        if pos2==1:
            our_pos=2
        if pos2==2:
            our_pos=1
    return our_pos
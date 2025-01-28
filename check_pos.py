def verifie_pos(mouse_pos,pos,taille):
    """Fonction qui prend en paramètre la position et taille d'un anneau et la position de la souris et renvoie si ce dernier a été cliqué"""
    renvoie = False
    if pos[0]-taille[0] < mouse_pos[0]:
        if pos[0]+taille[0] > mouse_pos[0]:
            if pos[1]-taille[1] < mouse_pos[1]:
                if pos[1]+taille[1] > mouse_pos[1]:
                    renvoie = True
    return renvoie
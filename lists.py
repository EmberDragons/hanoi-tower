class Maillon:
    """Classe de maillon pour les file et pile : avec v la valeur sauvegardée"""
    def __init__(self, v=None, s=None):
        """Constructeur de la classe qui s'occupe de stoquer les valeurs"""
        self.valeur = v
        self.suivant = s
    def __str__(self):
        """Fonction qui permet l'affichage des lists"""
        if self.suivant == None:
            return f"{self.valeur}"
        else:
            return f"{self.valeur} - {self.suivant}"
        
class Pile:
    """Classe d'une pile"""
    def __init__(self):
        """Constructeur de la classe Pile"""
        #constructeur de la classe
        self.premier = None

    def ajouter(self,v):
        """Fonction qui ajoute un maillon avec la nouvelle valeur à la liste"""
        m = Maillon(v)
        if self.premier == None:
            self.premier=m
        else:
            precedent=self.premier
            while precedent.suivant!=None:
                precedent=precedent.suivant
            precedent.suivant = m
    
    def enlever(self):
        """Fonction qui enlève l'élément tout en haut"""
        if self.premier != None:
            v=None
            precedent=self.premier
            if precedent.suivant != None:
                while precedent.suivant.suivant!=None:
                    precedent=precedent.suivant
                v = precedent.suivant.valeur
                precedent.suivant = None
            else:
                v=precedent
                self.premier = None
            return v

    def taille(self):
        """Fonction qui renvoie la taille de la liste"""
        n=0
        if self.premier != None:
            precedent=self.premier
            n=n+1
            while precedent.suivant!=None:
                n=n+1
                precedent=precedent.suivant
        return n
    
    def contient(self, valeur):
        """Fonction qui vérifie si une valeur est présente dans la Pile"""
        ans=False
        if self.premier != None:
            precedent=self.premier
            while precedent.suivant!=None:
                if precedent.valeur == valeur:
                    ans=True
                precedent=precedent.suivant
        return ans

    
    def __str__(self):
        return f"{self.premier}"

class File:
    """Classe d'une file"""
    def __init__(self):
        """Constructeur de la classe File"""
        #constructeur de la classe
        self.premier = None

    def ajouter(self,v):
        """Fonction qui ajoute un maillon avec la nouvelle valeur à la liste"""
        m = Maillon(v)
        if self.premier == None:
            self.premier=m
        else:
            precedent=self.premier
            while precedent.suivant!=None:
                precedent=precedent.suivant
            precedent.suivant = m
    
    def enlever(self):
        """Fonction qui enlève le premier élément"""
        if self.premier != None:
            v = self.premier.valeur
            self.premier = self.premier.suivant
            return v
    
    def verifie(self):
        """Fonction qui renvoie la barre du premier élément"""
        if self.premier != None:
            v = self.premier.valeur
            return v[0]
    
    def copy(self):
        """Fonction qui permet la copie d'une File entière"""
        list_elts = []
        precedent=None
        if self.premier != None:
            precedent=self.premier
            list_elts.append(precedent.valeur)
            while precedent.suivant!=None:
                list_elts.append(precedent.suivant.valeur)
                precedent=precedent.suivant
        new_File = File()
        for elt in list_elts:
            new_File.ajouter(elt)
        return new_File
    
    def taille(self):
        """Fonction qui renvoie la taille de la liste"""
        n=0
        if self.premier != None:
            precedent=self.premier
            n=n+1
            while precedent.suivant!=None:
                n=n+1
                precedent=precedent.suivant
        return n

    def __str__(self):
        return f"{self.premier}"
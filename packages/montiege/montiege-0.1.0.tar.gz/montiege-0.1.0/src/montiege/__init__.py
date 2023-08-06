
"""
Permet de représenter une pile"""
class Pile:
    '''création d'une instance Pile avec une liste que l'on nommera L'''
    def __init__(self):
        "Initialisation des 2 attributs : une liste L vide et la taille de la pile"
        self.L=[]
        self.taille=0

    def vide(self):
        "test si la pile est vide en retournant Vrai si c’est le cas"
        return self.taille==0

    def depiler(self):
        "retourne la pile à laquelle on a enlevé le sommet "
        assert(self.taille!=0),"La pile est deja vide"
        self.taille-=1
        return self.L.pop()


    def empiler(self,x):
        "retourne la pile avec pour sommet x"
        self.taille+=1
        return self.L.append(x)

    def longueur(self):
        return self.taille

    def sommet(self):
        assert(self.taille!=0)
        return self.L[self.taille-1]




"""
Permet de représenter des graphs
"""
class Noeud:
    def __init__(self,valeur,filsG,filsD,vie,genre):
        self.valeur=valeur
        self.filsG=filsG
        self.filsD=filsD
        self.vie=int(vie)
        self.genre=genre
    
    def EstVide(self):
        return self.valeur==None
    
    def EstFeuille(self):
        return self.filsG==None and self.filsD==None
    
    def DansArbre(self,val):
        if not self.EstVide():
            if self.valeur==val:
                return True
            else:
                if self.filsG is not None or self.filsD is not None:
                    return self.filsG.DansArbre(val) or self.filsD.DansArbre(val)
        return False

    def hauteur(self):
        if not self.EstVide():
            if self.EstFeuille():
                return 1
            else:
                hD=0
                hG=0
                if self.filsG: # idem que self.filsG is not None
                    hG=1+self.filsG.hauteur()
                if self.filsD:
                    hD=1+self.filsD.hauteur()
                return max(hD,hG)
        return None
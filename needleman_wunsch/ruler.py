from colorama import Fore, Style
import numpy as np

def red_text(text):
    return f"{Fore.RED}{text}{Style.RESET_ALL}"

class Ruler:
    """
    La classe Ruler sert à calculer la distance entre deux chaines.
    L'utilisateur doit lui-même lancer le calcul (compute()) pour construire la 
    "matrice de distance" F.
    report() renvoie les deux chaines avec les espaces rajoutés et les erreurs mise en rouge.
    """
    
    def __init__(self, chaine1, chaine2):
        self.chaine1 = chaine1
        self.chaine2 = chaine2
    
    def compute(self):
        F = np.zeros((len(self.chaine1)+1, len(self.chaine2)+1))
        pt = 1 #pénalité de trou (modifiable)
        ps = 1 #pénalité de substitution
        pi = 1 # pénalité d'insertion
        
        for i in range(len(self.chaine1)+1):
            F[i, 0] = pt*i
        for j in range(len(self.chaine2)+1):
            F[0, j] = pt*j
    
        for i in range(1, len(self.chaine1)+1):
            for j in range(1,len(self.chaine2)+1): #on teste les pénalités possibles et on choisit 
                d1 = F[i-1, j-1] + ps * (1 - int(self.chaine1[i-1] == self.chaine2[j-1]))
                #la penalité ajoutée à cette étape vaut ps si les chaine sont différentes et 0 sinon
                d2 = F[i-1, j] + pi
                d3 = F[i, j-1] + pt
                F[i, j] = min(d1, d2, d3)
        self.distance = int(F[i, j])
        self.matrice = F
        
    def report(self):
        F = self.matrice
        pt = 1 # pénalité de trou (modifiable)
        ps = 1 # pénalité de substitution
        pi = 1 # pénalité d'insertion
        
        Alignement1 = ""  # chaines que l'on va afficher, avec les espaces et les erreurs en rouge
        Alignement2 = ""
        i = len(self.chaine1) 
        j = len(self.chaine2) 
        
        
        while i > 0 and j > 0:
            Score = F[i, j]
            ScoreDiag = F[i-1, j-1]
            ScoreUp = F[i, j-1]
            ScoreLeft = F[i-1, j]
            if Score == ScoreDiag + ps * (1 - int(self.chaine1[i-1] == self.chaine2[j-1])):
                if self.chaine1[i-1] == self.chaine2[j-1]:
                    Alignement1 = self.chaine1[i-1] + Alignement1
                    Alignement2 = self.chaine2[j-1] + Alignement2
                else:
                    Alignement1 = red_text(self.chaine1[i-1]) + Alignement1
                    Alignement2 = red_text(self.chaine2[j-1]) + Alignement2
                i -= 1
                j -= 1
            elif Score == ScoreLeft + pi:
              Alignement1 = self.chaine1[i-1] + Alignement1
              Alignement2 = red_text("=") + Alignement2
              i -= 1
            elif Score == ScoreUp + pt:
              Alignement1 = red_text("=") + Alignement1
              Alignement2 = self.chaine2[j-1] + Alignement2
              j -= 1
        
        while i >= 0 and j>0:
            Alignement1 = self.chaine1[i] + Alignement1
            Alignement2 = red_text("=") + Alignement2
            i -= 1
            
        while j >= 0 and i>0:
            Alignement1 = red_text("=") + Alignement1
            Alignement2 = self.chaine2[j] + Alignement2
            j -= 1
        
        return Alignement1, Alignement2        
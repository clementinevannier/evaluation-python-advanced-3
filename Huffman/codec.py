""" Python advanced - EVAL """

""" #2 Codage de Huffman """
def compte(chaine): #compte le nombre d'apparitions de chaque lettre                               
    occurence = [] #lettres deja dans le dictionnaire
    L = {}
    for lettre in chaine:
        if lettre not in occurence:
            L[lettre] = 1
            occurence.append(lettre)
        else:
            L[lettre] += 1    
    return L
    
def deux_faibles(L1, L2):  
    """
    selectionne les deux embranchements de frequences les plus faibles et les supprime des listes
    """
    L=[]  #contient les 2 premiers embranchements de L1 et L2 s'ils existent
    if len(L1) >= 2:
        L.append((L1[0], 0))
        L.append((L1[1], 1))  # l'indice sert pour pouvoir supprimer les embranchements selectionnés 
    elif len(L1) == 1:
        L.append((L1[0], 0))
            
    if len(L2) >= 2:
        L.append((L2[0], 2))
        L.append((L2[1], 3))
    elif len(L2) == 1:
        L.append((L2[0], 2))
        
    res=[L[0], L[1]]
    for i in range(2, len(L)):
        if L[i][0].freq < res[0][0].freq:
            res[1] = res[0]
            res[0] = L[i]
        elif L[i][0].freq < res[1][0].freq:
            res[1] = L[i]
    
    for i in range(2):  
        #on commence par la fin pour eviter le probleme d'index au deuxieme tour de boucle
        if res[-(i+1)][1] == 1:  
            del L1[1]
        elif res[-(i+1)][1] == 0:
            del L1[0]
        elif res[-(i+1)][1] == 3:
            del L2[1]
        elif res[-(i+1)][1] == 2:
            del L2[0]
        
    return res[0][0],res[1][0]
        
class Embranchement:
    """
    Un embrenchement fait reference à un groupement de caracteres (text) ainsi que la somme des
    nombres d'occurence de ces caracteres (freq).
    Le noeud a egalement des "fils" qui sont les noeuds correspondants aux
    sous-groupements le composant.
    """
    def __init__(self, n1, n2):
        self.freq = n1.freq + n2.freq
        
        if n1.freq <= n2.freq:
            self.text = n1.text + n2.text
            self.fils_gauche = n1   # le fils de gauche est codé par 0
            self.fils_droite = n2
        else:
            self.text = n2.text + n1.text
            self.fils_gauche = n2
            self.fils_droite = n1
        
    def __repr__(self):
        return self.text+":"+str(self.freq)
        
class Feuille:
    """
    Une feuille est l'extrémité des branches de l'arbre.
    Il possède un texte (text) et une fréquence (freq) mais n'a contrairement aux noeuds 
    pas de fils.
    """
    def __init__(self, lettre, freq):
        self.text = lettre
        self.freq = freq
        
    def __repr__(self):
        return self.text+":"+str(self.freq)
        
        
class TreeBuilder:
    """
    Cette classe permet de construire (construction) un arbre à partir d'une phrase (text) à coder.
    Une fois l'arbre construit, la fonction (tree) construit l'arbre binaire.
    """
    
    def __init__(self, text):
        self.text = text
        self.lettres = compte(self.text).keys()
        
    def construction(self):
        larbre = []
        frequences = compte(self.text)
        lembranchements = []
        
        #feuilles_temp est la liste de couple (lettre,freq) rangée dans l'ordre croissant des freq
        feuilles_temp = sorted(frequences.items(), key = lambda t:t[1]) 
        lfeuilles = []
        for lettre,freq in feuilles_temp:
            lfeuilles.append(Feuille(lettre, freq)) 
        
        while len(lfeuilles) + len(lembranchements) > 1:
            n1, n2 = deux_faibles(lfeuilles, lembranchements)
            larbre.append(n1)
            larbre.append(n2)
            lembranchements.append(Embranchement(n1, n2))
        
        larbre.append(Embranchement(n1, n2)) #on rajoute la racine
        return larbre
    
    def tree(self): #convertit l'arbre en arbre binaire
        Node = {}
        larbre = TreeBuilder.construction(self) 
        for lettre in self.lettres:
            code = ""
            noeud = larbre[-1] #on part de la racine
            while type(noeud) == Embranchement:#tant qu'on a pas atteint la Feuille
                if lettre in noeud.fils_gauche.text:
                    code += "0"
                    noeud = noeud.fils_gauche
                else:
                    code += "1"
                    noeud = noeud.fils_droite
            Node[lettre] = code
        return Node
    
    
class Codec:
    """
    La classe Codec code un texte (encode) à partir d'un arbre binaire 
    ou décode un message codée (decode).
    """
    def __init__(self, tree):
        self.tree = tree
        
    def encode(self,text):
        code = ""
        for lettre in text:
            code += self.tree[lettre]
        return code
    
    def decode(self, encoded):
        decoded = ""
        temp = ""
        arbre_inverse = dict(zip(self.tree.values(), self.tree.keys())) 
        #on inverse les cles et les valeurs pour decoder plus facilement
        for chiffre in encoded:
            temp += chiffre
            if temp in arbre_inverse.keys():
                decoded += arbre_inverse[temp]
                temp = ""
        return decoded
        
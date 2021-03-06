#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Box_manager import Box_manager
from Scheduling import Scheduling
from Commande import Commande
from Type_produit import Type_produit
from Ligne import Ligne
from Type_box import Type_box
from Produit import Produit


#Classe centrale du projet:  gestion de l'ensemble de la production
#attribution des ressources et traitements des demandes
class Production(object):

    #Fonction finale assurant le processus depuis la lecture du fichier jusqu'à l'écriture du fichier résultat
    def simulation_production(self,filename):
        self.Lecture_fichier(filename)                  # lecture du fichier
        self.create_Lignes()                            # creation des lignes de prod
        self.create_Type_box()                          # creation des types de box+caractéristiques
        self.create_Type_produit()                      # creation des types de produits et caractéristiques
        self.create_Commandes()                         # creation des commandes et caractérisitiques
        self._schedule.box_manager.Attribution_type()   # fonction chargée d'attribuées un type de box à chauqe produits
        self._schedule.InitialasiationTri()             # attribution des commandes aux lignes de prod de manière optimisée en temps
        self._schedule.calcul_date_prod()               # production de tous les produits (calcul de la date de prod et mise à jour)
        self._schedule.date_fin_prod()                  # calcul de la date de fin de prod de chacune des commandes
        self._schedule.recherche_date_suivante()

        self.Calcul_cout_retard()       # calcul du cout total des retard et ajout au cout total
        self.Calcul_cout_box()          # calcul du cout total des box et ajout au cout total
        self.EcritureResult(filename)   # écriture de tous les résultats calculés (cout total, dates...) dans un fichier crée



    def __init__(self):
        self._cout = 0                          # variable cout final du traitement (achat des box + pénalités)
        self._schedule = Scheduling()           # Initialisation du scheduler (qui gère la répartition de l'ensemble des données)
        """# @AssociationMultiplicity 1"""
        self._lecture_txt = None



    # Initialisation de la lecture du fichier de données
    def Lecture_fichier(self,filename):
        production_list=[]
        with open(filename, newline='') as csvfile:
            for line in csvfile:
                production_list.append(line.strip().split())
            self._lecture_txt=production_list


    # creation du fichier réponse au nom demandé + remplissage sous la forme demandée
    def EcritureResult(self, filename):
        # Création du fichier solution
        file_name = filename
        print(file_name)
        index = file_name.index('.txt')
        file_name = file_name[:index]
        file_name = file_name + ".sol"

        # Initialisation écriture dans le fichier solution
        f = open(file_name, "w")
        f = open(file_name, "a")
        f.write(str(self._cout))
        f.write('\n')

        # Ecriture dans le fichier sol: nombre de box par type
        for i in range(len(self._schedule.box_manager._listes_types_box)):
            f.write(str(self._schedule.box_manager._listes_types_box[i].type)+" "+str(self._schedule.box_manager._compteur_box[i]))
            f.write('\n')

        # Ecriture dans le fichier sol: id de chaque commande et date reelle de sortie d'usine
        for element in self._schedule._liste_commandes:
            f.write(str(element._id) + " " + str(element._dateReel))
            f.write('\n')

        # Ecriture dans le fichier sol: liste des produits finis + caractéristiques
        for elt in self._schedule._liste_commandes:
            for elt2 in elt._liste_produits_afaire :
                f.write(str(elt._id) + " " +str(elt2._type.id)+" "+str(elt2._numligne)+" "+str(elt2._dateDebutProd)+" "+str(elt2._type.type_box.type))
                if elt2._box!=None:
                    f.write(" "+str(elt2._box._numero))
                f.write('\n')






    #Lecture de l'ensemble des types de produits à partir du fichier de données
    #Les types de produits sont créés et placés dans la liste de type produit du box manager (lui même dans le scheduler)
    def create_Type_produit(self):
        list_Type_produit=[]
        for i in range (int(self._lecture_txt[0][0])):
            list_Type_produit.append(Type_produit(self._lecture_txt[i+1][0], int(self._lecture_txt[i+1][1]),int(self._lecture_txt[i+1][2]),int(self._lecture_txt[i+1][3]),int(self._lecture_txt[i+1][4]), int(self._lecture_txt[i+1][5]) ))
        self._schedule.box_manager._listes_types_produit=list_Type_produit


    #Lecture de l'ensemble des commandes à partir du fichier de données
    #Les commandes sont créées et directement placées dans la liste de commande du scheduler
    def create_Commandes(self):

        # PHASE 1: création des commandes vides jusqu'ici (en terme de produit) + renseignement des caractéristiques
        list_Commande = []
        a = int(self._lecture_txt[0][0])
        b = int(self._lecture_txt[0][1])
        for i in range(a, a + b):
            list_produit=[]
            for j in range(4,len(self._lecture_txt[i+1])):
                list_produit.append(int(self._lecture_txt[i+1][j]))
            list_Commande.append(Commande(self._lecture_txt[i + 1][0], int(self._lecture_txt[i + 1][1]),
                                          int(self._lecture_txt[i + 1][2]), int(self._lecture_txt[i + 1][3]), list_produit))

        self._schedule._liste_commandes = list_Commande


        # commandes remplies ci-dessous (grâce à la création de l'ensemble des produits qui les composent)
        # Pour une commande donnée : 1. création des  entitées produits attendues (type, taille...)
        # 2. ajoue des entitées créées à la liste des produits à faire de la commande en question
        for cc in range(len(self._schedule._liste_commandes)):
            for aa in range(len(self._schedule.box_manager._listes_types_produit)) :
                for bb in range(self._schedule._liste_commandes[cc]._list_prod[aa]) :
                    self._schedule._liste_commandes[cc]._liste_produits_afaire.append(Produit(self._schedule._liste_commandes[cc]._id,(self._schedule.box_manager._listes_types_produit[aa])))


    #Lecture de l'ensemble des types de box à partir du fichier de données
    #Les types de box sont créés et directement placés dans la liste de type de box du box manager dans le scheduler
    def create_Type_box(self):
        list_Type_box=[]
        a=int(self._lecture_txt[0][0])
        b=int(self._lecture_txt[0][1])
        c=int(self._lecture_txt[0][3])
        for i in range(a+b,a+b+c):
            list_Type_box.append(Type_box(self._lecture_txt[i+1][0], int(self._lecture_txt[i+1][1]),int(self._lecture_txt[i+1][2]),int(self._lecture_txt[i+1][3]) ))
        self._schedule.box_manager._listes_types_box=list_Type_box
        self._schedule.box_manager._compteur_box=[0]*len(self._schedule.box_manager._listes_types_box)




    #Lecture de l'ensemble des lignes de productions à partir du fichier de données
    #Les lignes sont créées et directement placées dans la liste de lignes du scheduler
    def create_Lignes(self):
        list_Lignes = []
        c = int(self._lecture_txt[0][2])
        for i in range(c):
            list_Lignes.append(Ligne(i))
        self._schedule._liste_lignes=list_Lignes





    # Calcul après traitement de toutes les commandes du cout des retards de commandes
    # + ajout au cout total
    def Calcul_cout_retard(self):
        k=0
        m=self._schedule._liste_commandes
        for i in m:
            k=k+abs(i._dateReel-i._datePrevue)*i._penalite
        self._cout+=k

    # Calcul après traitement de toutes les commandes du cout d'achat de toutes les boxs necessaires
    # + ajout au cout total

    def Calcul_cout_box(self):
        k=0
        for i in range(len(self._schedule.box_manager._compteur_box)):
            k+=self._schedule.box_manager._compteur_box[i]*self._schedule.box_manager._listes_types_box[i].prix_box

        self._cout+=k

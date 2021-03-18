#!/usr/bin/python
# -*- coding: UTF-8 -*-


class Scheduling(object):

	def __init__(self):
		self._liste_commandes = []
		"""# @AssociationMultiplicity 1..*"""
		self._listes_types_produit = []
		"""# @AssociationMultiplicity 1..*"""
		self._liste_lignes = []
		"""# @AssociationMultiplicity 1..*"""

	def TriCommande(self,ListCommande):
		# ENSEMBLE DES COMMANDES A AJOUTER CONSIDEREE
		LigneReference = self._liste_lignes[0]

		for LocalCom in ListCommande:
			BestDelayLine=-1

		# ENSSEMBLE DES LIGNES DE PROD DU SCHEDULER CONSIDEREES
			for LocalLigne in self._liste_lignes:
				LocalDelayLine = 0

		# ETAPE 1: CALCUL DU DELAIS EN FONCTION DE TOUTES LES COMMANDES DEJA PLACEE SUR LA LIGNE
				for LocalCommande in LocalLigne._listes_commandes:
					for LocalProduit in  LocalCommande._liste_produits_afaire :
						LocalDelayLine = LocalDelayLine + LocalProduit._type.p


		# ETAPE 2: CHOIX DE LA LIGNE OU LE DELAI EST LE PLUS FAIBLE
				if(LocalDelayLine<BestDelayLine) or (BestDelayLine==-1):
					BestDelayLine=LocalDelayLine
					LigneReference=LocalLigne

			LigneReference._listes_commandes.append(LocalCom)

	def InitialasiationTri(self):
		self.TriCommande(self._liste_commandes)

	def AffichageEtatCommande(self):
		for element in self._liste_commandes:
			element.affichage()
	def AffichageEtatLignes(self):
		for element in self._liste_lignes:
			element.affichage()

""" 	def DelayLine(self,ligne):
		LocalDelayLine=0
		LocalVarm = 0
		LocalVaro = 0
		for LocalVarm in  range(len(ligne._listes_commandes)):
			for LocalVaro in range(len(ligne._listes_commandes[LocalVarm]._liste_produits_afaire)):
				LocalDelayLine=LocalDelayLine+Ligne._listes_commandes[LocalVarm]._liste_produits_afaire[LocalVaro]._type.p

		return


	def tri_commande(self):
		# gives us the fastest line
		IndexFastestLine = 0
		LocalDelayReference = self.DelayLine(self._liste_lignes[0])
		LocalVaru =0
		localDelay = 0
		for LocalVaru in range(len(self._liste_lignes)):
			localDelay = self.DelayLine(self._liste_lignes[LocalVaru])

			if(LocalDelayReference >localDelay):
				LocalDelayReference=localDelay
				IndexFastestLine=LocalVaru

"""






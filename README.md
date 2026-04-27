# SCOPIONS---TIC-TAC-TOE
Morpion arithmétique : le joueur joue les chiffres pairs, l’IA joue les chiffres impairs. Le but est d’aligner trois cases en 120s sur des points precis en utilisant la logique numérique..

#  SCOPIONS TIC TAC TOE

SCOPIONS TIC TAC TOE est une version revisitée du jeu du morpion, basée non pas sur des X et des O, mais sur des **chiffres**.  
Le jeu repose sur une logique arithmétique simple :  
- le joueur utilise **uniquement les chiffres pairs**,  
- l’adversaire (IA) utilise **uniquement les chiffres impairs**.

Ce projet est développé en Python avec Pygame et évolue continuellement pour devenir un jeu complet, fluide et visuellement unique.

---

##  Description du jeu

SCOPIONS TIC TAC TOE reprend le principe du morpion classique (aligner trois cases), mais en y ajoutant une mécanique originale basée sur les **nombres**.

Chaque tour, le joueur choisit un chiffre dans un pavé numérique.  
Les chiffres sont divisés en deux catégories :

- jusqu'a 16**Chiffres pairs (2, 4, 6, 8, 10, …)** → Joueur  
- jusqu'a 19**Chiffres impairs (1, 3, 5, 7, 9, …)** → Adversaire (IA)

Le plateau se remplit donc avec des valeurs numériques, ce qui donne une identité unique au jeu.  
Les chiffres impairs sont affichés avec un symbole visuel (losange) pour indiquer qu’ils sont **réservés à l’IA** et **inutilisables par le joueur**.

Le jeu mélange ainsi :
- stratégie du morpion  
- réflexion arithmétique  
- gestion des chiffres disponibles  
- prise de décision rapide  
- et logique visuel
Le tout dans un univers visuel personnalisé, inspiré du thème “Scorpion”.

---

##  Règles détaillées

###  1. Objectif du jeu
Comme dans un morpion classique, le but est d’**aligner trois cases** :
- horizontalement  
- verticalement  
- ou en diagonale  

Le premier à réaliser un alignement gagne la partie et il devra si il veut continuer avec point cible plus elever a l'infini.

---

###  2. Le pavé numérique
Le jeu utilise un pavé numérique contenant plusieurs chiffres.  
Chaque chiffre peut être utilisé **une seule fois**.

- Les **chiffres pairs** sont jouables par le joueur.  
- Les **chiffres impairs** sont réservés au bot et ne peuvent pas être sélectionnés par le joueur.

Les chiffres impairs sont marqués visuellement pour éviter toute confusion, si possible je pourrait ls enlever si sa derange vraiment les joueurs.

---

###  3. Fonctionnement des tours
Le jeu se déroule en alternance :

1. **Le joueur** choisit un chiffre pair et le place sur une case vide.  
2. **L’IA** choisit automatiquement un chiffre impair et joue son tour.  
3. Le cycle continue jusqu’à ce qu’un alignement soit formé ou que le plateau soit rempli.

---

###  4. Chiffres impairs : rôle de l’adversaire
Les chiffres impairs ne sont **jamais jouables par le joueur**.  
Ils représentent les coups possibles de l’IA.

Pour éviter toute erreur, ils sont affichés avec :
- un symbole (losange)  
- une couleur différente  
- une luminosité ajustée  

Cela permet au joueur de se repérer facilement.

---

###  5. Fin de partie
La partie se termine lorsque :
- un joueur aligne trois cases  
- ou que le plateau est rempli (égalité)

Un message de victoire ou d’égalité apparaît, et une nouvelle partie peut être lancée.

---

##  Technologies utilisées
- Python 3  
- Pygame  
- Interface graphique personnalisée  
- Système de rendu et d’effets visuels  
- IA simple ou (possibilite de ajouter des conditions dans le programe de l'ia pour qu'il soit plus inteligent) basée sur les chiffres impairs  

---

##  Développeur
Projet créé par **Ahmed Yassine SAidi**, lycéen passionné de développement et de création de jeux vidéo.  
Objectif : apprendre, progresser, et construire un jeu complet sur le long terme.

---

##  Évolution du projet
Le jeu est en développement continu(actuellement au tout debut).  
Améliorations prévues :
- animations  
- effets lumineux  
- IA plus intelligente  
- sons  
- transitions  
- menus avancés  
- système de niveaux  
- choix pour le consommateurde affronter un humain au lieu d'une ia
- choix entre etre team pair ou impere -


# Optimisation-Lin-aire
There are method to resolve optimisation linear in python

Afin de pouvoir découvrir mon interface graphique, il faut lancer le fichier “Interface_graphique.py”, qui est couplé au programme “Simplex_finale.py”. Il y a un dernier programme appelé "Big_M.py" qui correspond à la résolution des problèmes que mon programme simplex rencontre cependant, ce programme là n’est pas entièrement de moi est à grandement était inspiré d’un dépôt git.

Voici la syntaxe à adopter afin de manipuler mon interface

Dans la ligne fonction objective : 
ax + by + cz 

Pour la fenêtre des contraintes, il faut ajouter des contraintes du types :

ax + by + cz <= t
fx + vy + nz <= w 
...

Ensuite appuyer sur Calculer et le programme vous fournira la solution optimiale ainsi que les coefficients optimaux

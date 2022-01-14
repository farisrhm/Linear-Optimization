import re
import string
import sys

"""Ce programme correspond à mon algorithme du simplexe, cependant
il n'est pas capable de résoudre des équations avec des contraintes du type >= c'est donc pour 
cela que le second programme appelé BigM existe, or c'est ce programme là qui est implémenté dans mon
intérface graphique"""

# Dans cette première étape, on vient créer la table qui va nous permettre de mettre en place l'algorithme du simplexe

class Table:

    @classmethod
    def valeur_z(cls, table: list) -> int:
        for ligne in table:
            if ligne[0] == 1:
                return ligne[-1]
        return 0

    @classmethod
    def voir_table(cls, table: list):
        for i in range(len(table)):
            for j in range(len(table[i])):
                print(f"{table[i][j]}\t", end="")
            print()

    @classmethod
    def variables_basiques(cls, table: list) -> list:
        basics = []
        for i in range(len(table[0])):
            basic = 0
            for j in range(len(table)):
                basic += abs(table[j][i])

            if basic == 1:
                basics.append(i)

        return basics

    @classmethod
    def resultat_final(cls, table: list, coefficients: list) -> (dict, dict):
        basics = cls.variables_basiques(table)

        val_f = {
            "solution": cls.valeur_z(table),
        }

        basics.remove(0)

        try:
            for index in basics:
                var = coefficients[index - 1]
                for j in range(len(table)):
                    value = table[j][index]
                    if value == 1:
                        val_f[var] = table[j][-1]
                        break
        except Exception as e:
            pass

        for var in coefficients:
            if not var in val_f:
                val_f[var] = 0

        return val_f


class Simplex:

    pivot_column_index = 0
    inserted = 0
    coefficients = []

    def __init__(self, fo: str, objective):
        self.table = []
        self.coefficients = re.findall("[a-z]", fo)
        ligne = list(map(lambda x: x * (-1), self.conversion_expr(fo)))
        self.fo = [1] + ligne
        self.column_b = [0]
        self.objective = objective
        self.variables = list(string.ascii_lowercase)


    def coefficient_correct(self, expr: str):
        # Vérification d'une non répétition des coefficients 
        
        expr = expr.replace(" ", "")

        coefficients = re.findall("[a-z]", expr)
        # Ici cette ligne nous permet de récuperer uniquement les coefficients dans la liste
        data = re.split("\\+|\\-|<=", expr)
        is_duplicated = lambda x: len(x) != len(set(x))


        return True

    def conversion_expr(self, expr: str):
        # Ici on modifie l'expression de la fo afin qu'elle soit cohérente pour l'algorithme 
        
        if self.coefficient_correct(expr):
            expr = expr.replace(" ", "")

            coefficients = re.findall("[a-z]", expr)

            if coefficients != sorted(coefficients):
                raise ValueError("Utiliser les variables dans un ordre ordonné")

            pattern = ">=|\\+|\\-|<="
            separated_data = re.split(pattern, expr)

            values = []

            for coefficient in self.coefficients:
                contains = False
                for var in separated_data:
                    if coefficient in var:
                        value = re.findall(r"-?\d+", var)
                        values.append(value[0] if value else 1)
                        contains = True

                if not contains:
                    values.append(0)

            return list(map(int, values))

    def normalisation_t(self):
        #Définir les variables pour chaques ligne du tableau 
        
        self.table.insert(0, self.fo)
        normal_size = len(self.fo)
        for ligne in self.table:
            if len(ligne) < normal_size:
                addition = normal_size - len(ligne)
                for i in range(addition):
                    ligne.append(0)
        self.table = list(map(lambda x, y: x + [y], self.table, self.column_b))

    def ajout_contrainte(self, expr: str):
        # Ajout d'une restriction
        
        delimiter = "<="
        default_format = True

        expr_list = expr.split(delimiter)
        sa = [0] + self.conversion_expr(expr_list[0])

        if not default_format:
            self.fo = self.fo + [0]

        sa = self.variable_ecart(sa, default_format)
        self.column_b.append(int(expr_list[1]))
        self.table.append(sa)

    def variable_ecart(self, ligne: list, default_format=True):
        # On ajoute ici une variable d'écart dans la contrainte 
        
        self.fo.append(0)

        if not self.table:
            ligne.append(1)
            self.inserted += 1
            return ligne

        loop = len(self.table[self.inserted - 1]) - len(ligne)
        for i in range(loop):
            ligne.append(0)

        if not default_format:
            ligne = ligne + [-1, 1]
        else:
            ligne.append(1)

        self.inserted += 1

        return ligne

    def simplex_standard(self, sa: str):
        # On fait ici une vérification afin de voir si la syntaxe de la contrainte est correcte 
        
        return "<=" in sa and self.objective == 0

    def optimisation(self):
        # On vérifie ici s'il reste des valeurs négatifs dans la première ligne du tableau
        
        ocurrence = list(filter(lambda x: x < 0, self.table[0]))

        return False if ocurrence else True

    def colonne_pivot(self):
        # On définit ici la colonne du pivot 
        
        pivot_fo = min(self.table[0])  
        self.pivot_column_index = self.table[0].index(pivot_fo)

        column = []
        for i in range(len(self.table)):
            column.append(self.table[i][self.pivot_column_index])

        return column

    def ligne_pivot(self, entry_column: list):
        # On identifie ici la ligne en sortie
        
        val_f = {}

        for i, ligne in enumerate(self.table):
            if i > 0:
                if entry_column[i] > 0:
                    val_f[i] = ligne[-1] / entry_column[i]

        return min(val_f, key=val_f.get)

    def nouvelle_l(self, ligne: list, pivot_line: list):
        
        #On calcule ici la nouvelle ligne qui vas être remplacé dans le tableau

        pivot = ligne[self.pivot_column_index] * -1

        result_line = [pivot * value for value in pivot_line]

        new_line = list(map(lambda x, y: x + y, result_line, ligne))

        return new_line

    def calculate(self):
        column = self.colonne_pivot()
        first_exit_line = self.ligne_pivot(column)
        line = self.table[first_exit_line]
        pivot = line[self.pivot_column_index]

        pivot_line = list(map(lambda x: x / pivot, line))

        self.table[first_exit_line] = pivot_line

        stack = self.table.copy()

        line_reference = len(stack) - 1

        while stack:

            ligne = stack.pop()

            if line_reference != first_exit_line:

                new_line = self.nouvelle_l(ligne, pivot_line)

                self.table[line_reference] = new_line

            line_reference -= 1

    def solve(self):
        self.normalisation_t()
        self.calculate()

        while not self.optimisation():
            self.calculate()

        return Table.resultat_final(self.table, self.coefficients)
    
    


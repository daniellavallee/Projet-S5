## Calcul ta route!

##### Description #####
# Calcul de la trajectoire d'un parcours passant par des points
# de référence à l'aide d'un polynôme d'interpolation.

# Auteur: Daniel Lavallée, Mathieu Sévégny, Tristan Lafontaine, Émile Bois, Vincent Kilanowski
# Date: 2024-09-19

# Utilisation: Ajouter les points de référence X et Y et exécuter le script.

import numpy as np
import matplotlib.pyplot as plt

# Définition des points de référence (ajouter les points de référence ICI!)
X = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])
Y = np.array([0, 0, 1, 4, 3, 4, 8, 3, 6])

lenXY = len(X) if len(X) == len(Y) else 0   # Nombre de couples

X = X.reshape((lenXY, 1))       # Matrice X verticale
Y = Y.reshape((lenXY, 1))       # Matrice Y verticale


# Définition des phi (ex: phi_0 = X^0, phi_1 = X^1, ...)
phi = [X**i for i in range(lenXY)]


# Séparation des phi dans un tableau (phi_0, phi_1, phi_2, ...)
phi_list = []
[phi_list.append(phi[i]) for i in range(len(phi))]
    
print("\nLes valeurs de phi sont:\n")
for i in range(len(phi_list)):
    print("phi_", i, ": \n", phi_list[i], "\n", sep = "")


# Matrice P
P = np.hstack(phi_list)


# Matrice de coefficients A
A = np.linalg.inv(P) @ Y


# Coefficients a(i) de l'équation (ex: a0, a1, a2, ...)
coeff_list = []
[coeff_list.append(A[i]) for i in range(len(A))]

print("\nLes coefficient de A sont: \n")
for i in range(len(A)):
    print("a", i, ": ", A[i], sep = "")


# Équation de la trajectoire
dx = 0.1  # Incrément
x = np.arange(0, X.max() + dx, dx)  # Tableau de valeurs sur x


# Fonction du parcours
f = 0
f_print = ""        # String de l'équation
for i in range(len(A)):
    f += A[i] * x**i
    f_print += f"+ { coeff_list[i]} * x^{i} "

print("\n\nL'équation du polynôme est: \n\nf(x) = ", f_print)

# Affichage du parcours
plt.figure(1)
plt.plot(X, Y, 'o', label='Points de référence')
plt.plot(x, f, label='Polynôme du parcours')
plt.title("Trajectoire du parcours")
plt.xlabel("Axe des x (m)")
plt.ylabel("Axe des y (m)")
plt.legend()
plt.show()

%% Calcul ta route!

% Description: Calcul de la trajectoire d'un parcours en fonction de points
% de référence fourni.
% Auteur: Daniel Lavallée, Mathieu Sévigny, Tristan Lafontaine, Émile Bois, Vincent
% Kilanowski.
% Date: 2024-09-19

%% Configuration du fichier
clear all;
close all;
clc;

%% Calcul du parcours par la méthode de la projection orthogonale

% Définition des points de référence
X = [0; 1; 2; 3; 4; 5; 6; 7; 8; 9; 10];
Y = [0; 0; 1; 4; 3; 4; 8; 3; 6; 9; 9];

% Définition des phi
phi_0 = X.^0
phi_1 = X.^1
phi_2 = X.^2
phi_3 = X.^3
phi_4 = X.^4
phi_5 = X.^5
phi_6 = X.^6
phi_7 = X.^7
phi_8 = X.^8
phi_9 = X.^9
phi_10 = X.^10

% Matrice P
P = [phi_0, phi_1, phi_2, phi_3, phi_4, phi_5, phi_6, phi_7, phi_8, phi_9, phi_10];

% Matrice de coefficients A
A = inv(P)*Y;

% Coefficients de l'équation
a0 = A(1);
a1 = A(2);
a2 = A(3);
a3 = A(4);
a4 = A(5);
a5 = A(6);
a6 = A(7);
a7 = A(8);
a8 = A(9);
a9 = A(10);
a10 = A(11);

% Équation de la trajectoire
dx = 0.1;       % Incrément
x = [0:dx:10];  % Tableau de valeurs sur x

% Fonction du parcours
f = a0*x.^0 + a1*x.^1 + a2*x.^2 + a3*x.^3 + a4*x.^4 + a5*x.^5 + a6*x.^6 + a7*x.^7 + a8*x.^8 + a9*x.^9 + a10*x.^10;

% Affichage du parcours
figure(1);
plot(X, Y, "o");
hold on;
plot(x, f);
title("Trajectoire du parcours");
xlabel("Axe des x");
ylabel("Axe des y");
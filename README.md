# TPI-DeepBridge 23-24

Ce projet comprend plusieurs classes conçues pour traiter et manipuler des images. Voici une présentation de chaque classe :

## Pixel

La classe `Pixel` a été créée pour encapsuler les données d'un pixel que nous souhaitons sauvegarder. Elle est composée des éléments suivants :
- Coordonnées (x, y)
- Couleur

## Donati

La classe `Donati` est utilisée pour mettre en œuvre le concept de M. Donati.

## Utility

Cet espace regroupe des fonctions utilitaires générales, notamment :
- `compression_coefficient`: Calcule le coefficient de compression pour une liste de pixels.
- `merge_pixel`: Fusionne une liste de pixels avec des coefficients donnés.
- `map_coef_list`: Applique une stratégie de coefficients à une liste de pixels.

## Slice

La classe `Slice` gère les images morceau par morceau, en utilisant des informations de découpe.

## CoeffStrategy

La classe CoeffStrategy offre différentes stratégies pour évaluer les coefficients utilisés lors du traitement d'une liste de pixels. Ces stratégies comprennent l'évaluation en fonction de la distance maximale, minimale, moyenne, ou l'assignation de coefficients égaux à toutes les distances.

## Main

Le module Main joue le rôle principal dans l'exécution du programme. Il utilise la classe Slice pour générer une image modifiée à partir d'une source donnée. La fonction run prend en charge la configuration de la découpe de l'image en utilisant des informations telles que p et q, et elle sauvegarde le résultat à l'emplacement spécifié.


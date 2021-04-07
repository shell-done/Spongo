# Plan rapport de projet

- ### Page de garde (1 page)

- ### Sommaire (1 page)

- ### Glossaire (1 page)

- ### Remerciements (1 page)

- ### Introduction (1 page -> reprise 1er page du CDC)
    - Présentation de l'Ifremer et du LEP
    - Description du problème

- ### Cahier des charges (6 pages -> reprise du CDC)

- ### Données fournies (3 pages)
    - Description du format des données (csv, annot en cercle)
    - Lister les annotations, trier les données, supprimer les annotations non exploitable
    - Problèmes liées aux annotations : taille, nombre, pas toutes annotées -> completion nous même

- ### Réseau de neurones (16 pages)
    - Présentation vision par ordinateur, historique du CNN, comment ça marche, pourquoi utile dans notre situation

    - Intro/Recherches : Yolo, darknet, FasterRCNN
    
    - Choix : Yolo et FasterRCNN, puis uniquement Yolo à cause du temps
    
    - Finalement : YoloV4 et différentes variantes de YoloV5 car format d'entrée identique (plus rapide à faire), résultat comparable. Yolov4 : apprentissage sur darknet et test avec OpenCV. Yolov5 : apprentissage et test avec pytorch
    
    - Explication du format d'annotation Yolo. Création de scripts pour générer les annotations Yolo à partir du fichier de données + vérification de cette génération
    
    - Apprentissage : sur colab, explication de la mAP, IoU, avg loss, precision/recall. Architecture du réseau, transfer learning
    
    - Mesure "à la main" car annotations pas fiable, choix du ratio test set/training set
    
    - Explication de notre protocole d'expérimentation
    
    - Comparaison résultats YoloV4, v5s, v5m, v5l -> v5 apprentissage + rapide, détection + rapide, meilleur détection dans l'ensemble, au détriment des petits morphotypes
    
    - Comparaison résultats paramètres d'entrées : taille des annotations, découpage et entrée du réseau
    
    - Performance CUDA : avantages, inconvénients
    
    - Finalement : yolov4, x1.5, 416, /1

- ### IHM (8 pages)
    - Intro/Objectif de l'IHM : claire, épurée et utilisable par n'importe qui. Explication de nos choix (graphiques, historique, etc..). Dire qu'on leur avait présenté une maquette (à mettre en annexe). Techno utilisé : python et Qt car simple

    - Paramètres : Explication des paramètres, pourquoi on a laissé le choix du seuil de confiance, du processeur à utiliser, des images à sauvegarder, etc...

    - Analyse :
        - Explication du visuel
        - Implémentation du NN: au début OpenCV mais pas utilisable avec simplement avec CUDA (il aurait fallut recompiler). On s'est tourné vers pytorch car support CUDA inclu -> pas besoin d'installer CUDA à la main. On a trouvé une implémentation de Yolov4 en pytorch
        - Utilisation de thread pour ne pas bloquer l'interface

    - Historique :
        - Objectifs de l'historique, pour ça : sérialisation des données de l'analyse
        - Aperçu du compte rendu de l'analyse en HTML
        - Possibilité d'exporter les données

- ### Export des données (2 pages)
    - Objectifs de l'export, des différents types de rapports
    - Possibilité de continuer l'apprentissage à partir des détections

- ### Gestion de projet (3 pages)
    - Fonctionnement en mode agile, par tâche atomique
    - Nous avons fait des choix : pas testé faster RCNN, etc ... -> nous sommes dans les temps
    - Réunion régulière avec l'encadrant
    - Problèmes rencontrés : beaucoup de temps perdu sur les annotations, ...
    - Préparation de la livraison : déploiement, exec, manuels d'utilisation, ...

- ### Conclusion (2 pages)
    - Résumé de ce qu'on a fait
    - Technologies utilisées
    - Ouverture : utilisation pour d'autres tâches similaires

- ### Annexes (5 pages)
    - Architecture de YoloV4
    - Maquette proposée
    - Rapport d'une analyse en PDF

# Questions
 - Abstract ?
 - Glossaire, table des figures, etc... ?
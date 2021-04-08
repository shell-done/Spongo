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
    - Tri des données : création de scripts pour lister les annotations, supprimer les annotations non exploitables, ...
    - Problèmes liés aux annotations : taille, noms différents (majuscules), nombre, pas toutes annotées -> complétion nous-mêmes

- ### Réseau de neurones (16 pages)
    - Qu'est-ce qu'un réseau de neurones ?
        - Présentation principes NN, deep learning, etc...
        - Historique du CNN, comment ça marche
        - Dans notre cas : traitement d'images, vision par ordinateur

    - Nos recherches sur les réseaux
        - Découverte de réseaux qui correspondent à nos besoins en traitement d'images :     
            - Yolo
            - Darknet
            - FasterRCNN
        - Procédés d'élimination : Yolo et FasterRCNN, puis uniquement Yolo à cause du temps
        - Réseaux que nous avons conservés pour nos tests : YoloV4 et différentes variantes de YoloV5 car format d'entrée identique (plus rapide à mettre en place), résultats comparables. Yolov4 : apprentissage sur darknet et test avec OpenCV. Yolov5 : apprentissage et test avec pytorch
    
    - Mise en place de nos tests
        - Explication du format d'annotations Yolo. Création de scripts pour générer les annotations Yolo à partir du fichier de données + vérification de cette génération
        - Explication de notre protocole d'expérimentation
        - Apprentissage : sur colab, explication de la mAP, IoU, avg loss, precision/recall. Architecture du réseau, transfer learning
        - Mesure "à la main" car annotations pas fiables, choix du ratio test set/training set
    
    - Résultats des tests
        - Comparaison résultats YoloV4, V5s, V5m, V5l -> V5 apprentissage + rapide, détection + rapide, meilleure détection dans l'ensemble, au détriment des petits morphotypes (avec matrices de confusion)
        - Comparaison résultats paramètres d'entrées : taille des annotations, découpage et entrée du réseau (avec matrices de confusion)
        - Performances CUDA : avantages, inconvénients
        - Finalement : YoloV4 avec x1.5, 416px, /1

- ### IHM (8 pages)
    - Introduction
        - Objectif de l'IHM : claire, épurée et utilisable par n'importe qui. Explication de nos choix (graphique, historique, etc..). Dire qu'on leur avait présenté une maquette (à mettre en annexe).
        - Technos utilisées : Python et Qt car simple et on les maîtrise

    - Paramètres
        - Explication des paramètres, pourquoi on a laissé le choix du seuil de confiance, du processeur à utiliser, des images à sauvegarder, etc...

    - Analyse
        - Explication du visuel
        - Implémentation du NN: au début OpenCV mais pas utilisable avec simplement avec CUDA (il aurait fallut recompiler). On s'est tourné vers pytorch car support CUDA inclu -> pas besoin d'installer CUDA à la main. On a trouvé une implémentation de YoloV4 en pytorch
        - Utilisation de threads pour ne pas bloquer l'interface
        - Optimisations pour ne pas ralentir l'appli : points du chart, affichage des images, etc...

    - Historique
        - Objectifs de l'historique
        - Sérialisation des données pour sauvegarder les analyses
        - Aperçu du compte rendu de l'analyse en HTML
        - Possibilité d'exporter les données

- ### Export des données (2 pages)
    - Objectifs de l'export
    - Explication des différents types/formats de rapports
    - Possibilité de continuer l'apprentissage à partir des détections

- ### Gestion de projet (3 pages)
    - Organisation
        - Fonctionnement en mode Agile, par tâches atomiques
        - Réunions régulières avec l'encadrant
        - Nous avons fait des choix : pas testé faster RCNN, etc ... -> nous sommes dans les temps

    - Problèmes rencontrés : beaucoup de temps perdu sur les annotations, ...

    - Préparation de la livraison : déploiement, exec, manuels d'utilisation, ...

- ### Conclusion (2 pages)
    - Résumé de ce qu'on a fait
    - Technologies utilisées
    - Ouverture : évolutivité de l'application, utilisation pour d'autres tâches similaires

- ### Bibliographie (1 page)

- ### Annexes (5 pages)
    - Architecture de YoloV4
    - Maquette proposée
    - Rapport d'une analyse en PDF

# Questions
 - Abstract ?
 - Glossaire, table des figures, etc... ?
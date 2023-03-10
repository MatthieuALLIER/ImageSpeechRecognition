# Challenge Web Mining - ImageSpeechRecognition

### Key words 
Voice recognition - Face recognition - Emotion, gender, age detection - Deep Learning

### Summary
We had 2 days to create a streamlit app. The goal is to control the webcam of our computer by voice (start/stop the webcam and/or the recording). Once the camera is activated, it is able to identify the people in our database, as well as detect their gender, age, and emotions in real time.


## Objectif de ce repository

Ce repository présente comment utiliser l'image Docker pour accéder à l'application Streamlit, et coment utiliser cette dernière

## Comment utiliser ce repository :

Vous avez deux moyens d'utiliser ce repository :

## 1. Obtenir l'image par Docker Hub

Pour récupérer les images par le Docker Hub voici les étapes

### Requis

* Avoir Docker Desktop et un compte Docker Hub

Lancer un terminal et faire les commandes insérées ci-dessous : 

```
$ # Le username est le mot de passe concerne celui de votre compte Docker Hub
$ docker login --username=your_username --password=your_password
$ docker pull htitouan/chall-secu
$ docker run -p 8501:8501 htitouan/chall-secu
```

Après avoir lancé ces commandes vous pouvez ouvrir l'application sur : localhost:8501

## 2. Construire l'image à partir du Git

Pour construire l'image Docker à partir des fichiers voici les étapes : 

### Requis 

* Avoir téléchargé le git et au minima avoir le dossier Streamlit dans son ordinateur
* Télécharger le dossier data dans le drive et l'insérer dans le dossier "streamlit"

Lancer un terminal et faire les commandes insérées ci-dessous : 

```
$ cd 'path/to/your/repository/folder/streamlit'
$ docker build -t "nom_image_de_votre_choix" .
$ docker run -p 8501:8501 "nom_image_de_votre_choix"
```
Après avoir lancé ces commandes vous pouvez ouvrir l'application sur : localhost:8501

## 3. Présentation de l'application streamlit

Lorsque nous arrivons sur l'application, vous pouvez appuyer sur "Lancer la reconnaissance vocale" afin de démarrer celle-ci. Afin d'activement la webcam il faut prononcer le mot "Démarrer" (vous pouvez prononcer une phrase qui contient le mot "démarrer", cela fonctionne aussi). Celle-ci met plusieurs seconde avant de s'activer, il faut un peu de patience.  Afin d'arrêter la webcam il faut prononcer le mot "arrêter". Lorsque la webcam est active, vous pouvez lancer un enregistrement en prononçant le mot "enregistrer", et stopper celui-ci avec le mot "stopper". A gauche de l'écran s'affiche les mots que l'appareil a entendu, ainsi que ses réponses (par exemple, si il a entendu le mot démarrer, il va répondre "la caméra s'allume")
Vous pouvez consulter directement consulter vos vidéos enregistrées dans l'onglet "Recordings".








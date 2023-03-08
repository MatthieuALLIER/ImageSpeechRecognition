import cv2
import numpy as np
from keras_vggface.vggface import VGGFace
from keras_vggface.utils import preprocess_input*

### CHARGER LE MODELE DE DETECTION DE VISAGE
face_model_path = "./model/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(face_model_path)

### CHARGER LE MODELE DE RECONNAISSANCE DE PERSONNE
model = VGGFace(model='vgg16')
input_shape = model.layers[0].input_shape[1:3]

### CHARGER LES DONNEES DE REFERENCE
reference_data = np.load('./extract_features/reference_data.npy', allow_pickle=True)
reference_names = np.load('./extract_features/reference_names.npy', allow_pickle=True)

### CONFIGURER LA CAMERA
video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detecter les visages dans l'image en niveaux de gris
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Extraire les vecteurs de caractéristiques de chaque visage détecté
    for (x, y, w, h) in faces:
        # Récupérer le visage de l'image
        face = frame[y:y+h, x:x+w]

        # Redimensionner le visage pour la reconnaissance faciale
        face = cv2.resize(face, input_shape)

        # Prétraiter l'image
        face = preprocess_input(face.astype('float32'))

        # Transférer le visage dans le modèle VGGFace pour extraire les vecteurs de caractéristiques
        features = model.predict(np.expand_dims(face, axis=0))[0]

        # Comparer les vecteurs de caractéristiques extraits avec les vecteurs de caractéristiques stockés
        distances = np.linalg.norm(reference_data - features, axis=1)
        min_distance_index = np.argmin(distances)
        min_distance = distances[min_distance_index]

        # Afficher le nom de la personne correspondante si la distance est inférieure à un certain seuil
        if min_distance < 0.6:
            name = reference_names[min_distance_index]
            cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
        else:
            cv2.putText(frame, "Inconnu", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # Dessiner un rectangle autour du visage
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Afficher l'image résultante
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

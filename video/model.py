import cv2
import numpy as np

### CHARGER LE MODELE DE DETECTION DE VISAGE
face_model_path = "./model/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(face_model_path)


### CHARGER LES DONNEES DE REFERENCE
reference_data = np.load('./extract_features/reference_data.npy', allow_pickle=True)
reference_labels = np.load('./extract_features/reference_labels.npy', allow_pickle=True)

print(reference_labels)
print(type(reference_labels))
### CHARGER LE MODELE DE RECONNAISSANCE DE PERSONNE
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(reference_data, np.array(reference_labels))

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
        face = gray[y:y+h, x:x+w]

        # Redimensionner le visage pour la reconnaissance faciale
        face = cv2.resize(face, (200, 200))

        # Transférer le visage dans le modèle Eigenfaces pour extraire les vecteurs de caractéristiques
        label, confidence = recognizer.predict(face)

        # Afficher le nom de la personne correspondante si la distance est inférieure à un certain seuil
        if confidence < 3000:
            name = reference_labels[label]
            cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
        else:
            cv2.putText(frame, "Inconnu", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # Dessiner un rectangle autour du visage
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Afficher l'image résultante
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer la capture de la caméra et fermer les fenêtres d'affichage
video_capture.release()
cv2.destroyAllWindows()

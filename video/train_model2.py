import cv2
import os
import numpy as np

dataset_path = './photos/'
face_cascade = cv2.CascadeClassifier('./model/haarcascade_frontalface_default.xml')

face_data = []
labels = []

for subdir, dirs, files in os.walk(dataset_path):
    for file in files:
        if file.endswith('.jpg') or file.endswith('.jpeg'):
            path = os.path.join(subdir, file)
            label_str = os.path.basename(subdir)
            try:
                label = int(label_str)
            except ValueError:
                continue
            img = cv2.imread(path, 0)
            faces = face_cascade.detectMultiScale(img, 1.3, 5)
            for (x, y, w, h) in faces:
                face = img[y:y+h, x:x+w]
                face_data.append(face)
                labels.append(label)

### CHARGER LES DONNEES DE REFERENCE
# reference_data = np.load('./extract_features/reference_data.npy', allow_pickle=True)
# reference_labels = np.load('./extract_features/reference_labels.npy', allow_pickle=True)

print(face_data)
# print(len(reference_data))
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

# Train the model
face_recognizer.train(face_data, np.array(labels))

# Save the trained model
face_recognizer.save('trained_model.yml')

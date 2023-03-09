import os
import shutil
import numpy as np
from video_detection import getImagesAndLabels
import json

try:
    # Ouvrir les anciennes features
    known_face_encodings_to_concat = np.load("./photos_featured/known_face_encodings.npy")
    # Feature sur les nouvelles photos
    known_face_encodings, known_face_names = getImagesAndLabels("./photos_to_train/")
    # Assembler les deux
    known_face_encodings = np.concatenate((known_face_encodings_to_concat, known_face_encodings))

except:
    known_face_encodings, known_face_names = getImagesAndLabels("./photos_to_train/")

# Enregistrer les features en .npy
np.save("./photos_featured/known_face_encodings.npy", known_face_encodings)
# Enregistrer les labels en .txt
with open('./photos_featured/known_face_names.json', 'w') as f:
    json.dump(known_face_names, f)

# Chemin du dossier source
source_folder = './photos_to_train/'

# Chemin du dossier destination
destination_folder = './photos_trained/'

# Liste des fichiers dans le dossier source
files = os.listdir(source_folder)

# Parcourir la liste des fichiers et les déplacer vers le dossier destination
for f in files:
    # Chemin complet du fichier source
    source_path = os.path.join(source_folder, f)
    
    # Chemin complet du fichier destination
    destination_path = os.path.join(destination_folder, f)
    
    # Déplacer le fichier
    shutil.move(source_path, destination_path)
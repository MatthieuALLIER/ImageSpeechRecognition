import cv2
import os
import face_recognition
import re
import warnings
import json

# Supprimer le warning "Décompression bomb DOS"
warnings.filterwarnings("ignore", message="Image size.*")

known_face_encodings = []

def getImagesAndLabels(path):

    try:
        # Ouvrir les labels pour étendre la liste
        with open('./photos_featured/known_face_names.json', 'r') as f:
            known_face_names = json.load(f)
    except:
        known_face_names = []

    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]  
    for imagePath in imagePaths:
        
        image = face_recognition.load_image_file(imagePath)
        image_face_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(image_face_encoding)   

        name = os.path.splitext(os.path.basename(imagePath))[0]
        pattern = re.compile(r"[\d._]+")
        name = pattern.sub("", name)

        known_face_names.append(name)

    return known_face_encodings, known_face_names

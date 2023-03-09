import cv2
import os
import face_recognition
import re
import warnings
import json

# Supprimer le warning "Décompression bomb DOS"
warnings.filterwarnings("ignore", message="Image size.*")

known_face_encodings = []

def pretrained_age():

    ageProto = "./model/age_deploy.prototxt"
    ageModel = "./model/age_net.caffemodel"

    genderProto = "./model/gender_deploy.prototxt"
    genderModel = "./model/gender_net.caffemodel"

    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
    ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    genderList = ['Male', 'Female']

    ageNet = cv2.dnn.readNet(ageModel,ageProto)
    genderNet = cv2.dnn.readNet(genderModel, genderProto)

    return ageNet,genderNet,ageList,genderList,MODEL_MEAN_VALUES

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

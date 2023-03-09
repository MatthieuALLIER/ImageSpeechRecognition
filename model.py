import face_recognition
import cv2
import numpy as np
from video_detection import pretrained_age
import json

# Listes
face_locations = []
face_encodings = []
face_names = []
genders = []
ages = []

# Ouvrir les features
known_face_encodings = np.load("./photos_featured/known_face_encodings.npy")
# Ouvrir les labels
with open('./photos_featured/known_face_names.json', 'r') as f:
    known_face_names = json.load(f)

# A enregistrer dans des listes
ageNet,genderNet,ageList,genderList,MODEL_MEAN_VALUES = pretrained_age()

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Only process every other frame of video to save time
    if process_this_frame:
        # Resize frame of video to 1/4 size for faster face recognition processing

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

            blob = cv2.dnn.blobFromImage(small_frame, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)

            #Pass the face through the age and gender nets
            genderNet.setInput(blob)
            genderPreds = genderNet.forward()
            gender = genderList[genderPreds[0].argmax()]

            ageNet.setInput(blob)
            agePreds = ageNet.forward()
            age = ageList[agePreds[0].argmax()]

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Box
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        # Cadre
        cv2.rectangle(frame, (left, bottom - 20), (right+1, bottom + 60), (0, 0, 255), cv2.FILLED)

        font = cv2.FONT_HERSHEY_DUPLEX
        # Prenom
        cv2.putText(frame, name, (left + 6, bottom +10), font, 1.0, (255, 255, 255), 1)
        
        # # Draw age and gender labels on the frame
        label = "{}, {}".format(gender, age)
        # Age - Sexe
        cv2.putText(frame, label, (left + 6, bottom + 50), font, 1.0, (255, 255, 255), 1)


    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()


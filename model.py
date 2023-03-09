import face_recognition
import cv2
import numpy as np
import json
from deepface import DeepFace

# Listes
face_locations = []
face_encodings = []
face_names = []

# Ouvrir les features
known_face_encodings = np.load("./photos_featured/known_face_encodings.npy")
# Ouvrir les labels
with open('./photos_featured/known_face_names.json', 'r') as f:
    known_face_names = json.load(f)

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

        detections = DeepFace.analyze(frame, actions = ['emotion', 'age', 'gender'], enforce_detection=False, silent=True)
        
        sexes = []
        emotions = []
        ages = []
        for detection in detections:
            age = detection['age']
            gender = detection['gender']
            emotion = detection['emotion']

            sexes.append(max(gender, key=gender.get))
            emotions.append(max(emotion, key=emotion.get))
            ages.append(age)

        #     sorted_emotion = sorted(emotion.items(), key=lambda x: x[1], reverse=True)

        #     emo_pers = []
        #     emo_total = []
        #     for k, v in sorted_emotion:
        #         emo_pers.append((k, round(v/sum(emotion.values())*100, 2)))
        # emo_total.append(emo_pers)

    process_this_frame = not process_this_frame

    # Display the results #emo_pers , emo_total
    for (top, right, bottom, left), name, age,gender,emotion in zip(face_locations, face_names, ages, sexes, emotions):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Box
        cv2.rectangle(frame, (left, top), (right, bottom), (0,89,255), 2)
        # Cadre
        cv2.rectangle(frame, (left, bottom - 20), (right+1, bottom + 70), (0,89,255), cv2.FILLED)

        font = cv2.FONT_HERSHEY_DUPLEX
        # Informations
        labels = "{}, {}, {}".format(name, age, gender)
        
        # Get the size of the text in pixels
        text_size, _ = cv2.getTextSize(labels, font, 1.1, 1)
        # Calculate the width of the rectangle
        rect_width = right - left
        
        # Adapt the size of the text to the width of the rectangle
        if text_size[0] > rect_width:
            font_scale = rect_width / text_size[0]
        else:
            font_scale = 1.1
            
        # Draw the text with the adapted font size
        cv2.putText(frame, labels, (left + 6, bottom +10), font, font_scale, (0, 0, 0), 1)

        # Adapt the size of the emotion text to the width of the rectangle
        text_size, _ = cv2.getTextSize(emotion, font, 1.1, 1)
        
        if text_size[0] > rect_width:
            font_scale = rect_width / text_size[0]
        else:
            font_scale = 1.1
        
        cv2.putText(frame, emotion, (left + 6, bottom +45), font, font_scale, (0, 0, 0), 1)



        # sorted_emo = sorted(emo_pers, key=lambda x: x[1], reverse=True)[:3]
        # for i, (emo, percent) in enumerate(sorted_emo):
        #     e = "{}, {}%".format(emo, percent)
        #     cv2.putText(frame, e, (left + 6, bottom + (i*30) + 90), font, 0.8, (0, 0, 0), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()


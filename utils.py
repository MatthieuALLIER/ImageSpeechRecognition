import threading
import speech_recognition as sr
import face_recognition
import io
import contextlib
from pynput.keyboard import Controller
import cv2
import datetime
import streamlit as st
import numpy as np
import json
from deepface import DeepFace

class listenThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.text = []
        self.app = app
        self.keyboard = Controller()
        self.r = sr.Recognizer()
        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source, 3)
        self.text.append('On vous écoute')
        self.app.updateText()
        
    def run(self):       
        while True:
            with sr.Microphone() as source:
                audio = self.r.listen(source, phrase_time_limit=3)           
            try:
                sortie = io.StringIO() 
                with contextlib.redirect_stdout(sortie):
                    dest=self.r.recognize_google(audio, language="fr-FR")
                
                dest = dest.lower()
                self.text.append(dest)     
                
                if ("démarrer" in dest):
                    self.text.append('La caméra démarre')
                    self.app.start_webcam() 
                       
                elif ("enregistrer" in dest):
                    self.text.append("Enregistrement")
                    self.keyboard.press('r')
                    self.keyboard.release('r') 
                           
                elif ("stopper" in dest):
                    self.text.append("Fin de l'enregistrement")
                    self.keyboard.press('s')
                    self.keyboard.release('s') 
                       
                elif ("arrêter" in dest):
                    self.text.append("La caméra se ferme")
                    self.app.stop_webcam()
                    
                elif ("quoi" in dest):
                    self.text.append("feur") 
                    
                elif ("finir" in dest):
                    self.stop()
                    
                else:
                    pass                
                self.app.updateText()
                
            except:
                pass
            
            self.app.islistening()
                
    def stop(self):
        raise SystemExit
      
          
class cameraThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.frame = None
        self.stop_event = threading.Event()


    def run(self):

        # Listes
        face_locations = []
        face_encodings = []
        face_names = []

        # Ouvrir les features
        known_face_encodings = np.load("./photos_featured/known_face_encodings.npy")
        # Ouvrir les labels
        with open('./photos_featured/known_face_names.json', 'r') as f:
            known_face_names = json.load(f)

        video_capture = cv2.VideoCapture(0)    
        process_this_frame = True 

        frame_width = int(video_capture.get(3))
        frame_height = int(video_capture.get(4))
        size = (frame_width, frame_height)
        record=False
        out= None        
        
        while not self.stop_event.is_set():          
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
                
            frame = frame[:, :, ::-1]
                

            #write video
            if record:
                if out is None:
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    filename = f"{current_time}.avi"                
                    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
                    out = cv2.VideoWriter(filename, fourcc, 10, size)
                out.write(frame)                
            key = cv2.waitKey(1) & 0xFF
            
            # Check if the 'r' key was pressed to start recording
            if key == ord('r'):
                record = True
            
            # Check if the 's' key was pressed to stop recording
            if key == ord('s'):
                record = False
                if out is not None:
                    out.release()
                    out = None                
            
            if ret:
                self.frame = frame
            
    def stop(self):
        self.stop_event.set()
        

class StreamlitThread():
    def __init__(self):
        self.opencamT = None
        self.listenReactT = listenThread(self)
        self.listening = False
        self.textUpdated = False
        st.set_page_config(page_title='SL', page_icon=':guardsman:', layout='wide')
        st.title('Challenge')
        
    def start_webcam(self):
        self.opencamT = cameraThread()
        self.opencamT.start()
        
    def stop_webcam(self):
        if self.opencamT is not None:
            self.opencamT.stop()
            self.webcam_thread.join()
            self.opencamT = None
    
    def islistening(self):
        self.listening = True
    
    def stoplistening(self):
        self.listening = False
        
    def updateText(self):
        self.textUpdate = True
        
    def run(self):  
        if not self.listening:
            self.listenReactT.start()
            
        col1, col2 = st.columns([3, 1])
        with col1:
            placeholder = st.empty()
        with col2:
            placetext = st.empty()
            
        while True:
            while self.textUpdate:
                text = " / ".join(self.listenReactT.text[-15:])
                placetext.write(text)
                self.textUpdate = False
                
            while self.opencamT is not None and self.opencamT.frame is not None:
                text = " / ".join(self.listenReactT.text[-15:])
                placetext.write(text)
                placeholder.image(self.opencamT.frame, use_column_width=True)
                
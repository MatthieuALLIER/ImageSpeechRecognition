import threading
import speech_recognition as sr
import io
import contextlib
from pynput.keyboard import Controller
import cv2
import streamlit as st

st.set_page_config(page_title='SL', page_icon=':guardsman:', layout='wide')
st.title('Challenge')

class listenReact(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.is_running = False
        
    def run(self):
        if not self.is_running:
            self.is_running = True
            keyboard = Controller()
            r = sr.Recognizer()
            print("Ecoute")
            with sr.Microphone(device_index=1) as source:
                r.adjust_for_ambient_noise(source, duration=3)
                print("Ecoute")
                while True:
                    audio = r.listen(source, phrase_time_limit=2)            
                    try:
                        sortie = io.StringIO() 
                        with contextlib.redirect_stdout(sortie):
                            dest=r.recognize_google(audio)
                        dest = dest.lower()
                        print(dest)                    
                        if (dest=="open"):
                            print('La caméra démarre')
                            stream = opencam()
                            stream.start()
                        
                        if (dest=="launch"):
                            print("Enregistrement")
                            keyboard.press('r')
                            keyboard.release('r')
                            
                        if (dest=="stop"):
                            print("Fin de l'enregistrement")
                            keyboard.press('s')
                            keyboard.release('s')
                        
                        if (dest=="close"):
                            print("La caméra se ferme")
                            stream.stop()
                            
                        if (dest=="finish"):
                            self.stop()
                    except:
                        pass
                
    def stop(self):
        self.is_running = False
        st.stop()
                
class opencam(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.video = cv2.VideoCapture(0)
        self.frame = None
        self.is_running = True
        model = "video/model/haarcascade_frontalface_default.xml"
        self.faceCascade = cv2.CascadeClassifier(model)

    def run(self):
        while self.is_running:
            ret, frame = self.video.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = self.faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            if ret:
                self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def stop(self):
        self.is_running = False
        self.video.release()

col1, col2 = st.columns([3, 1])

stream = opencam()

listen_react = listenReact()
listen_react.start()

while stream.frame is None:
    pass

image_placeholder = st.empty()

while True:
    with col1:
        image_placeholder.image(stream.frame, channels="RGB")
    

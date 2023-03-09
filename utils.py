import threading
import speech_recognition as sr
import io
import contextlib
from pynput.keyboard import Controller
import cv2
import datetime
import streamlit as st

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
                
                if (dest=="démarrer"):
                    self.text.append('La caméra démarre')
                    self.app.start_webcam() 
                       
                elif (dest=="enregistrer"):
                    self.text.append("Enregistrement")
                    self.keyboard.press('r')
                    self.keyboard.release('r') 
                           
                elif (dest=="stopper"):
                    self.text.append("Fin de l'enregistrement")
                    self.keyboard.press('s')
                    self.keyboard.release('s') 
                       
                elif (dest=="arrêter"):
                    self.text.append("La caméra se ferme")
                    self.app.stop_webcam()
                    
                elif (dest=="quoi"):
                    self.text.append("feur") 
                    
                elif (dest=="finir"):
                    self.stop()
                    
                else:
                    pass                
                self.app.updateText()
                
            except:
                pass
            
            self.app.islistening()
                
    def stop(self):
        print("Le micro est coupé")
        self.is_running = False
        self.app.stoplistening()
        st.stop()
      
          
class cameraThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.frame = None
        self.stop_event = threading.Event()
        model = "haarcascade_frontalface_default.xml"
        self.faceCascade = cv2.CascadeClassifier(model)

    def run(self):
        video = cv2.VideoCapture(0)       
        frame_width = int(video.get(3))
        frame_height = int(video.get(4))
        size = (frame_width, frame_height)
        record=False
        out= None        
        
        while not self.stop_event.is_set():          
            ret, frame = video.read()
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
                self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
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
                
    
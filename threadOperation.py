import threading
import speech_recognition as sr
import io
import contextlib
from pynput.keyboard import Controller
from video.recognition_fct import opencam

def listenReact():    
    keyboard = Controller()
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            r.adjust_for_ambient_noise(source, duration=0.2)
            audio=r.listen(source)
            try:
                sortie = io.StringIO()
                with contextlib.redirect_stdout(sortie):
                    dest=r.recognize_google(audio)
                dest = dest.lower()
                print(dest)
                
                if (dest=="open webcam"):
                    t = threading.Thread(target=opencam)
                    t.start()
                    print('La caméra démarre')
                
                if (dest=="launch record"):
                    print("La caméra se ferme")
                    keyboard.press('r')
                    keyboard.release('r')
                    
                if (dest=="stop record"):
                    print("La caméra se ferme")
                    keyboard.press('s')
                    keyboard.release('s')
                
                if (dest=="close webcam"):
                    print("La caméra se ferme")
                    keyboard.press('q')
                    keyboard.release('q')
                    
                if (dest=="stop"):
                    print("Fermeture")
                    break
            except Exception as e:
                e
    
listenReact()

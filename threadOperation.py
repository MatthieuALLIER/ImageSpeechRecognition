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
        r.adjust_for_ambient_noise(source, duration=3)
        while True:
            audio = r.listen(source, phrase_time_limit=2)
            try:
                sortie = io.StringIO()
                with contextlib.redirect_stdout(sortie):
                    dest=r.recognize_google(audio)
                dest = dest.lower()
                print(dest)
                
                if (dest=="open"):
                    t = threading.Thread(target=opencam)
                    t.start()
                    print('La caméra démarre')
                
                if (dest=="record"):
                    print("Enregistrement")
                    keyboard.press('r')
                    keyboard.release('r')
                    
                if (dest=="stop"):
                    print("Fin de l'enregistrement")
                    keyboard.press('s')
                    keyboard.release('s')
                
                if (dest=="close"):
                    print("La caméra se ferme")
                    keyboard.press('q')
                    keyboard.release('q')
                    
                if (dest=="finish"):
                    print("Fermeture")
                    break
            except Exception as e:
                e

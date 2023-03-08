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
<<<<<<< Updated upstream
            audio = r.listen(source, phrase_time_limit=2)
=======
            
            audio=r.listen(source,phrase_time_limit=2)
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
                    print("Enregistrement")
=======
                    print("L'enregistrement démarre")
>>>>>>> Stashed changes
                    keyboard.press('r')
                    keyboard.release('r')
                    
                if (dest=="stop"):
<<<<<<< Updated upstream
                    print("Fin de l'enregistrement")
=======
                    print("L'enregistrement s'arrête")
>>>>>>> Stashed changes
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

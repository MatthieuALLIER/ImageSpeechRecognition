import speech_recognition as sr
import pyttsx3
import webbrowser as web

''' speech recognotion to open webcam'''
#r = sr.Recognizer()

def Speaktext(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

def main():    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            r.adjust_for_ambient_noise(source, duration=0.2)
            audio=r.listen(source)
            try:
                dest=r.recognize_google(audio)
                
            except Exception as e:
                e
dest = main()

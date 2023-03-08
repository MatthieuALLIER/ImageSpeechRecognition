import speech_recognition as sr
import pyttsx3
import webbrowser as web
from recognition_fct import opencam

def recognition_voice():
    with sr.Microphone() as source:
        r = sr.Recognizer()
        r.adjust_for_ambient_noise(source, duration=0.2)
        print("Say something!")
        audio=r.listen(source)
        MyText=r.recognize_google(audio)
        MyText=MyText.lower()
        print(MyText)
        #if MyText=="hello":
        #    print('hello')


recognition_voice()





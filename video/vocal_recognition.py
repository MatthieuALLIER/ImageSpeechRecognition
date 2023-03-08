import speech_recognition as sr
import pyttsx3
import webbrowser as web
from recognition_fct import opencam

with sr.Microphone() as source:
    r = sr.Recognizer()
    r.adjust_for_ambient_noise(source, duration=0.2)
    print("Say something!")
    audio=r.listen(source)
    MyText=r.recognize_google(audio)
    MyText=MyText.lower()
    if (MyText=="open webcam"):
        opencam()
        
    #print("Did you say "+MyText)
    #Speaktext(MyText)






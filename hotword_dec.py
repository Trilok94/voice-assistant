# this is the main file to run, run this 
import os
import speech_recognition as sr 
from speak import speak
def takecommand():
    r = sr.Recognizer()  # recognise the voice
    with sr.Microphone() as source:  # listning for voice from microphone
        print("listning...")
        r.pause_threshold = 1  # you can change this
        audio = r.listen(source,0,10)
    try:
        print("recognizing ...")
        query = r.recognize_google(
            audio, language='en-in')  # trying to understand
        print(f"user said : {query}\n")
    except Exception as e:
        # print(e)
        print("try again please ")
        return "none"
    return query.lower()
    #hello

while True:
    hotword = takecommand()
    
    if "wake up" in hotword:
        speak("please enter the security key before accessing virtual assistant :")
        entered_pass = input("enter the security key: ")
        if entered_pass=="python":
            # import subprocess
            # subprocess.Popen("dodoui1.exe")
            os.system("python main.py") 
        else:
            print("Access Denied! Please try again")
            speak("Access Denied! Please try again")
    else:
        pass

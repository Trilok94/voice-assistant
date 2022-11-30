import pyttsx3
engine = pyttsx3.init('sapi5')

voices = engine.getProperty('voices')  # get voices
# print(voices[0].id)  # print types of voices available

print(voices)

engine.setProperty('voices', voices[0].id)  # set voices


# speak the text
def speak(text):
    engine.say(text)
    engine.runAndWait()
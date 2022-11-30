import speech_recognition as sr 
def takecommand():
    '''
    takes audio from microphone as a input from the user , convert it into string and returns that string or none string if there is problem in recognizing
    '''
    r = sr.Recognizer()  # recognise the voice
    with sr.Microphone() as source:  # listning for voice from microphone
        print("listening...")
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
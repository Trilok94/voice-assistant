# prediction libs
from email import message
import random
import json
import pickle
from tkinter import colorchooser
import numpy as np 

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model

# my speak and listen files
from listen import takecommand
from speak import speak

# common lib
import datetime
from datetime import date
import PyPDF2
import sys
import wikipedia
import webbrowser
import pywhatkit as kit 
import os
# import subprocess
import requests

from pyautogui import click
import pyautogui
import time
import keyboard
import pyjokes
import psutil
from PIL import Image
from bs4 import BeautifulSoup
from notifypy import Notify
from pywikihow import search_wikihow
from PyDictionary import PyDictionary as Diction
from googletrans import Translator
import speech_recognition as sr 
import instaloader

# email libs
# please enter your email and password in from_email.txt file before sending mail
# please enter the email_id of those people you want to send mail in email.txt file
import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# gui 
import tkinter
import threading
import pywin
speak("initializing DODO..")
    
url = "https://www.youtube.com/channel/UC9zY_E8mcAo_Oq772LEZq8Q"
timeout = 5
try:
	request = requests.get(url, timeout=timeout)
	print("Connected to the Internet")
	speak("INTERNET connection detected")
	speak("all systems have been activated")
except (requests.ConnectionError, requests.Timeout) as exception:
	print("No internet connection  ")
	speak("No internet connection detected .")
	speak("Shutting down the program.")
	print('you are not connected to internet , please make sure you connected to wi-fi or internet to start jarvis program', 'ALERT !')
	speak("Thanks for giving me your time")
	sys.exit()

lemmitizer = WordNetLemmatizer()
with open('intents.json','r') as f:
    intents = json.load(f)

# load words, classes and model 
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))
model = load_model('va_model.h5')


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmitizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word==w :
                bag[i] = 1
    
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence) # convert into array 
    res = model.predict(np.array([bow]))[0] # predict convert 
    # print(f"this is result of model.predict : {res}")
    ERROR_THRESHOLD = 0.25

    # for i, r in enumerate(res):
    #     print(f"enum r is {r}")
    #     print(f"enum i is {i}")

    results = [[i,r ] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    
    # print(f"value of result before sort : {results}")
    results.sort(key= lambda x: x[1],reverse=True)
    # print(f"value of result after sort : {results}")
    return_list = []
    for r in results:
        # print(f"the value of r in results : {r}")
        return_list.append({'intent': classes[r[0]], "probability": str(r[1])})
    # print(f"this is return list from predict_class func : {return_list}")
    return return_list
# bag = [] *6
# print(bag)


def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    
    return result


# functions
def wishme():
    '''
    wish you at starting 
    '''
    hour = int(datetime.datetime.now().hour)
    # print(hour)

    if hour >= 0 and hour < 12:
        speak("good morning")
    elif hour >= 12 and hour < 18:
        speak("good afternoon")
    else:
        speak("good eveaning")

    print("Hello sir, I am Dodo. Please tell me how may i help you ?")
    speak("Hello sir, I am Dodo. Please tell me how may i help you ?")

def get_time():
    strtime = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"sir the time is {strtime}")
    speak(f"sir the time is {strtime}")

def get_date():
    today = date.today()
    print(f"Today's date: {today}")
    speak(f"Today's date: {today}")

def convertTime(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "%d:%02d:%02d" % (hours, minutes, seconds)

def pdf_reader(path_of_file):
    book = open(path_of_file, "rb")
    reader = PyPDF2.PdfFileReader(book)

    total_pages = reader.numPages
    print(f"the total pages in this pdf is : {total_pages} ")
    speak(f"the total pages in this pdf is : {total_pages} ")

    speak("please enter the page number you want to listen")
    # get the page no. you want to listen and store it on variable
    page_no = int(input("enter page no. here : ")) - 1

    # get the page not that content which value stored in variable "pg"
    one_page = reader.getPage(page_no)

    text = one_page.extractText()  # get the page content
    print(text)
    speak(text)

    while page_no < total_pages:
        speak("do you want to listen next page : ")
        cond = takecommand()
        if "yes" in cond:
            page_no = page_no + 1
            # speak(f"this page no. is : {page_no}")
            one_page = reader.getPage(page_no)
            text = one_page.extractText()
            speak(text)
            # print(text)
            if page_no == total_pages-1:
                speak(
                    "This was last page of this pdf. there is no other page after that ")
                break
        else:
            break

def whatsapp(number,message):
    numb = '+91' + number
    open_chat = "https://web.whatsapp.com/send?text=" + message
    webbrowser.open(open_chat)
    time.sleep(15)
    keyboard.press('enter')

def Whatspp_Grp(group_id , message):
    open_chat = "https://web.whatsapp.com/accept?code=" + group_id
    webbrowser.open(open_chat)
    time.sleep(15)
    keyboard.write(message)
    keyboard.press('enter')

def takehindi():
    r = sr.Recognizer()  # recognise the voice
    with sr.Microphone() as source:  # listning for voice from microphone
        print("listning...")
        r.pause_threshold = 1  # you can change this
        audio = r.listen(source,0,10)

    try:
        print("recognizing ...")
        query = r.recognize_google(
            audio, language='hi')  # trying to understand
        print(f"user said : {query}\n")
    except Exception as e:
        # print(e)
        print("try again please ")
        return "none"
    return query.lower()

def trans():
    print("translator activated!")
    speak("translator activated!")
    print("tell me the line ")
    speak("tell me the line !")
    line = takehindi()
    translate = Translator()
    transresult = translate.translate(line)
    text = transresult.text
    print(text)
    speak(text)
    print("translator exited")
    speak("translator exited")

msg = MIMEMultipart()
def send_email(to_email, message):

    with open("from_email.txt", "r") as my_mail: # please enter your email and password 
        from_email = my_mail.readlines()
        msg['From'] = from_email[0]
        password = from_email[1]
    my_mail.close()
    text = msg.as_string()
    server = smtplib.SMTP("smtp.gmail.com", 587)  # instance of smtp server"
    # make a tls(transport layer security) connection with my server
    server.starttls()  
    # make login to the server using email and password
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], text)  # send message
    server.quit()  # quit the server


# for speed test 
def SpeedTest(message):
    import speedtest
    print("Checking speed.....")
    speak("Checking speed.....")
    speed = speedtest.Speedtest()

    downloading = speed.download()
    correctDown =int(downloading/800000)

    uploading = speed.upload()
    correctUpload = int(uploading/800000)

    if 'uploading' in message:
        print(f"The Uploading Speed Is {correctUpload} mbp s")
        speak(f"The Uploading Speed Is {correctUpload} mbp s")
    elif 'downloading' in message:
        print(f"The Downloading Speed Is {correctDown} mbp s")
        speak(f"The Downloading Speed Is {correctDown} mbp s")
    else:
        print(f"The Downloading is {correctDown} and The Uploading Speed is {correctUpload} mbp s")
        speak(f"The Downloading is {correctDown} and The Uploading Speed is {correctUpload} mbp s")


# for tempreature using bs4
def Temp():
    search = "temperature in delhi"
    url = f"https://www.google.com/search?q={search}"
    r = requests.get(url)
    data = BeautifulSoup(r.text,"html.parser")
    temperature = data.find("div",class_ = "BNeawe").text
    print(f"The Temperature Outside is {temperature} ")
    speak(f"The Temperature Outside is {temperature} ")

# for nasa news 
def today_date():
    today = date.today()
    return today

api_key = "938HU7yXAcvihra5W9DzFNyL1fOkKgTueqCczN4x"

def NasaNews(Date):
    print("extracting data from nasa")
    speak("extracting data from nasa")
    Url = 'https://api.nasa.gov/planetary/apod?api_key=' + str(api_key)
    Params = {"date":str(Date)}
    r= requests. get(Url,params = Params)
    Data = r.json()
    Info = Data['explanation']
    Title = Data['title']
    Image_Url = Data['url']
    Image_r = requests.get(Image_Url)
    FileName = str(Date) + '.jpg'
    os.chdir('C:\\Users\\don\\Desktop\\neuralva\\nnewsdata')
    with open(FileName, 'wb') as f:
        f.write(Image_r.content)

    img = Image.open(FileName)
    img.show()
    os.chdir('..')
    print(f'title : {Title}')
    speak(f'title : {Title}')
    print(f"According To Nasa : {Info}")
    speak(f"According To Nasa : {Info}")
    click(x=1890, y=16)


def Dict():
    print ("Dictionary Activated !")
    speak ("Dictionary Activated !")
    print ("Tell Me The problem!")
    speak ("Tell Me The problem!")
    probl = takecommand()

    if 'meaning' in probl:
        probl = probl.replace("what is the","")
        probl = probl.replace("dodo","")
        probl = probl.replace("of","")
        probl = probl.replace("meaning","")
        probl = probl.replace("of","")
        probl = probl.replace("tell","")
        probl = probl.replace("show","")
        probl = probl.replace("me","")
        probl = probl.replace("the","")
        probl = probl.replace(" ","")
        result = Diction.meaning(probl)
        print (f"The Meaning For {probl} is {result}")
        speak (f"The Meaning For {probl} is {result}")

    elif "synonym" in probl:
        probl = probl.replace("what is the","")
        probl = probl.replace("dodo","")
        probl = probl.replace("of","")
        probl = probl.replace("synonym","")
        probl = probl.replace("of","")
        probl = probl.replace(" ","")
        result = Diction.synonym(probl)
        print (f"The synonym For {probl} is {result}")
        speak (f"The synonym For {probl} is {result}")

    elif 'antonym' in probl:
        probl = probl.replace("what is the","")
        probl = probl.replace("dodo","")
        probl = probl.replace("of","")
        probl = probl.replace("antonym","")
        probl = probl.replace("of","")
        probl = probl.replace(" ","")
        result = Diction.antonym(probl)
        print(f"The Antonym For {probl} is {result}")
        speak(f"The Antonym For {probl} is {result}")

    speak("Exited Dictonary")
def exit():
    sys.exit()




def main_exe():
    clear = lambda:os.system('cls')
    clear()
    if __name__ == '__main__':
        wishme()
        try:
            while True:
                clear = lambda:os.system('cls')
                clear()
                # message = takecommand()
                speak("listening mode is on, ready for your command !")
                message = takecommand()
                ints = predict_class(message) # greeting 
                # print(f"--------------------the value of ints in while loop is {ints}") # ints = [{'intent': 'greeting', 'probability': '0.9995921'}]
                res = get_response(ints,intents) # get_response(predicted , json file)





                if res == 'time':
                    get_time()

                elif res == 'date':
                    get_date()

                elif res == 'reading':
                    speak("please enter the path of pdf you want to listen ")
                    pdf_path = input("enter the path here :")
                    pdf_reader(pdf_path)

                elif res=='exit':
                    result_exit = random.choice(["bye sir", "ok sir , i am going", "thanks for using me", "see you next time","it will be nice to meet you again"])
                    speak(result_exit)
                    speak("you can call me anytime just say wakeup dodo")
                    exit()

                elif res == 'wikipedia':
                    message = message.replace("tell me about"," ")
                    message = message.replace("wikipedia"," ")
                    message = message.replace("search in wikipedia"," ")
                    message = message.replace("wikipedia about"," ")
                    message = message.replace("show me wikipedia of"," ")
                    # message = message.replace(" ","")
                    # print(message)

                    # speak('what do you want to search in wikipedia, sir ?')
                    query = message
                    speak("searching wikipedia... ")
                    # remove "wikipedia" string from query
                    query = query.replace("wikipedia", "")
                    # return 2 sentences from wikipedia
                    results = wikipedia.summary(query, sentences=2)
                    speak("according to wikipedia")
                    print(results)
                    speak(results)

                elif res == 'open':  # open the websites in browser using webbrowser
                    message = message.replace("open","") # message = application_name , site.com
                    message = message.replace("dodo","")
                    message = message.replace("website","")
                    message = message.replace("open","")
                    message = message.replace("application","")
                    message = message.replace("app","")
                    message = message.replace("launch","")
                    message = message.replace(" ","")
                    x = 'com'
                    if x in message:
                        # message = message.replace(".com ","")
                        speak ("Ok Sir , Launching.....")
                        link = 'https://www.' + message
                        # print(web2)
                        webbrowser.open(link)
                        speak("Launched!")
                    else:
                        # speak("what do you want to search")
                        # print("what do you want to search")
                        # search_query = takecommand()
                        # webbrowser.open(f"{search_query}")

                            # webbrowser.open("stackoverflow.com")

                            # speak("which song do you want to play :")
                            # song_name = takecommand()
                            # kit.playonyt(song_name)

                        speak("Ok Sir, wait A second!")

                        if 'code' in message:
                            os.startfile("C:\\Users\\don\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")
                            speak("the visual studio code has been opened")
                        elif 'chrome' in message:
                            os.startfile("C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe")
                            speak("the chrome browser has been opened")
                        else:
                            click(x=59, y=1078)
                            time.sleep(1)
                            keyboard.write(message)
                            time.sleep(1)
                            click(x=225, y=378)
                            speak("the "+message+" has been opened")
                    speak("Your Command Has Been Completed")


                elif res=='remember':
                    print(message)
                    remembermsg = message.replace("remember that","")
                    remembermsg = remembermsg.replace("dodo remember my data","")
                    remembermsg = remembermsg.replace("remind me that","")
                    remembermsg = remembermsg.replace("dodo","")

                    speak("You Tell Me To Remind You That :"+ remembermsg)  
                    remember = open('remember_data.txt','w')
                    remember.write(remembermsg)
                    remember.close()

                elif res=='remembered data':
                    remembered = open('remember_data.txt','r')
                    print("You Tell Me That"+remembered.read())
                    speak("You Tell Me That"+remembered.read())

                elif res =='close':
                    message = message.replace("close","") # message = application_name , site.com
                    message = message.replace("dodo","")
                    message = message.replace("website","")
                    message = message.replace("close","")
                    message = message.replace("application","")
                    message = message.replace("app","")
                    message = message.replace("this","")
                    message = message.replace(" ","")
                    speak("Ok Sir, wait A second!")

                    if 'chrome' in message:
                        os.system('TASKKILL /F /im brave.exe')
                    elif "code" in message:
                        os. system("TASKKILL /F /im code.exe")
                    else:
                        speak("please maximize the window size before closing the "+ message)
                        time.sleep(5)
                        click(x=1890, y=16)

                        speak("the "+message+" has been closed")

                    speak("Your Command Has Been Succesfully Completed!")

                elif res=="playsong":
                        speak("which song do you want to play :")
                        song_name = takecommand()
                        kit.playonyt(song_name)

                elif res=="switchthewindow":
                        pyautogui.keyDown('alt')
                        pyautogui.press("tab")
                        pyautogui.sleep(1)
                        pyautogui.keyUp('alt')

                elif res=="screenshot":
                    speak("sir , please tell me the name of this screenshot pic ")
                    sc_name = takecommand().lower()
                    speak("sir , hold the screen for few second , i am taking screenshot")
                    pyautogui.screenshot(
                        f'C:\\Users\\don\\Desktop\\neuralva\\scrshot\\{sc_name}.png')
                    speak("sir screen has been taken and stored in sub directory")

                elif res=="battery":
                        battery = psutil.sensors_battery()

                        print(f"your current Battery percentage is {battery.percent} % ")
                        speak(f"your current Battery percentage is {battery.percent} % ")

                        # print(f"Power plugged in : { battery.power_plugged}")
                        # converting seconds to hh:mm:ss
                        print(
                            f"your current Battery left status is {convertTime(battery.secsleft)}")
                        speak(
                            f"your current Battery left status is {convertTime(battery.secsleft)}")

                        if battery.power_plugged == False:
                            print("your laptop is Not plugged into power")
                            speak("your laptop is Not plugged into power")

                        else:
                            print("your laptop is plugged into power")
                            speak("your laptop is plugged into power")

                        if battery.percent <= 20 and battery.power_plugged == False:
                            print(
                                "your battery is less then 20 % , i would highly reccomand to plugged into power ")
                            speak(
                                "your battery is less then 20 % , i would highly reccomand to plugged into power ")

                elif res=='googlesearch':
                    import wikipedia as googlesearch
                    message = message.replace("dodo","")
                    message = message.replace("google","")
                    message = message.replace("search","")
                    message = message.replace("about","")
                    message = message.replace("on","")
                    # message = message.replace(" ","")
                    speak("This Is what I Found On The web!")
                    kit.search(message)
                    try:
                        result = googlesearch.summary(message, 3)
                        speak(result)
                    except:
                        speak("Done Sir!")
                        speak("No speakable Data Availablel")

                elif res=='ipaddress':
                    ip = requests.get("https://api.ipify.org").text
                    print(f"your ip address is : {ip}")
                    speak(f"your ip address is : {ip}")

                elif res=='send email':
                    try:
                        speak("sir could you please tell me to whom do you want to send email ")
                        name = takecommand()
                        # name = input("enter name : " )

                        # opening a text file

                        with open('email.txt', 'r') as mail_file: # please enter the email_id of those people you want to send mail in email.txt file
                            for each_line in mail_file:
                                splitted_each_line = each_line.split("=")
                                if name.lower() in splitted_each_line[0].lower():
                                    # print(splitted_each_line[1])
                                    msg['To'] = splitted_each_line[1]
                                    mail_file.close()  # close the file
                                    break

                        if msg['To'] != "":
                            print(f"i got this email from your document : {msg['To']}")

                            speak("what sould be the suject sir : ")
                            msg['Subject'] = takecommand()

                            speak("what should i say :")
                            body = takecommand()
                            msg.attach(MIMEText(body, 'plain'))
                            send_email(msg['To'], body)
                            print("email has been sent")
                            speak("email has been sent")
                        else:
                            print("mail not found")
                            speak("mail not found")

                    except Exception as e:
                        print(e)
                        print("sorry i am not able to send this email")

                elif res=="joke":
                        joke = pyjokes.get_joke()
                        print(joke)
                        speak(joke)

                # sleep ,shutdown , restart os
                elif res=="shutdown system":
                    print("the system will be shutdown in 10 second")
                    time.sleep(10)
                    os.system("shutdown /s /t 5")

                elif res=="restart system":
                    print("the system will be restart in 10 second")
                    time.sleep(10)
                    os.system("shutdown /r /t 5")

                elif res=="sleep system":
                    print("the system will be sleep in 10 second")
                    time.sleep(10)
                    os.system("rundll32.exe powrprof.dll,SetSuspendState Sleep")

                elif res=='nasanews':
                    NasaNews(date.today())

                elif res=='temperature':
                    Temp() # current dalna hai intents file me 

                elif res=='speedtest':
                    SpeedTest(message)

                elif res=='timetable':
                    from timetable import timetable
                    value = timetable()
                    noti = Notify()
                    noti.message(value)
                    noti.send()
                    speak("anything else sir ? ")

                elif res=='whatsapp':
                    message = message.replace("dodo","")
                    message = message.replace("send","")
                    message = message.replace("whatsapp","")
                    message = message.replace("message","")
                    message = message.replace("to","")
                    message = message.replace(" ","")
                    name = message
                    print(name)
                    if 'neeraj' in name:
                        numb = "9654599309"
                        speak(f"What's The Message For {name}")
                        mess = takecommand()
                        whatsapp(numb,mess)

                    elif 'extra' in name:
                        grp_id = "FZ7PxIqDzFp5MxpfgeYgEx"
                        speak(f"What's The Message For {name}")
                        mess = takecommand()
                        Whatspp_Grp(grp_id,mess)
                    else:
                        numb = input(f"please enter {name}'s number here: ")
                        speak(f"What's The Message For {name}")
                        mess = takecommand()
                        whatsapp(numb,mess)

                elif res=='how to':
                    speak("Getting Data From The Internet !")
                    op = message.replace("dodo","")
                    max_result = 1
                    how_to_func = search_wikihow(op,max_result)
                    assert len(how_to_func) == 1
                    how_to_func[0].print()
                    speak(how_to_func[0].summary)
                    search_wikihow(op,max_result)

                elif res=='yttoolkit':
                    speak("Whats Your Command ?")
                    com= takecommand()
                    if "pause" in com:
                        keyboard.press("space bar")
                    elif "pause" in com:
                        keyboard.press("space bar")
                    elif 'restart' in com:
                        keyboard.press("&")
                    elif "mute" in com:
                        keyboard.press('n')
                    elif "skip" in com:
                        keyboard. press("1")
                    elif "back" in com:
                        keyboard.press('1')
                    elif "full screen" in com:
                        keyboard.press('f')
                    elif "film mode" in com:
                        keyboard.press('t')

                    speak("done")

                elif res == 'dict':
                    Dict()

                elif res=='finspro':
                    speak("sir , please enter the username")
                    profile_name = input("enter profile username : ")
                    webbrowser.open(f"https://www.instagram.com/{profile_name}")
                    speak("this is the instagram profile you are looking for")
                    speak("sir , would you like to download the profile pic ")
                    cond = takecommand().lower()

                    if "yes" in cond:
                        mod = instaloader.Instaloader()
                        mod.download_profile(profile_name, profile_pic_only=True)
                        speak("picture has been downloaded on your current directory")

                    else:
                        pass

                elif res=='translator':
                    trans()
                elif res=='none':
                    speak("i didn't hear you, please try again!")
                else:
                    print(res)
                    speak(res)

        except Exception as e:
            speak("there is any exception in your program")
            main_exe()







 
main_exe()


# gui code 
# screen_main = tkinter.Tk()
# screen_main.configure(background='black')
# screen_main.attributes('-fullscreen',True)


# def color_changer():
#     color = ['red','Gold','silver','cyan','magenta']
#     actual_color = random.choice(color)
#     label.configure(foreground=actual_color)
#     label.after(1000,color_changer)

# label = tkinter.Label(screen_main,font=('courier new',35),text='created by vipul', background='black')
# color_changer()
# label.place(x=1300,y=43)













# for terminal in tkinter
# class Redirect():
#     def __init__(self,widget,autoscrool=True):
#         self.widget = widget
#         self.autoscrool = autoscrool
    
#     def write(self,text):
#         self.widget.insert('end',text)
#         if self.autoscrool:
#             self.widget.see('end') # for autoscrool terminal in tkinter



# class RedirectText(object):
#     def __init__(self, text_ctrl):
#         """Constructor"""
#         self.output = text_ctrl

#     def write(self, string):
#         self.output.insert(tkinter.END, string)



# def run():
#     threading.Thread(target=speak("hello")).start()
#     def flush(slef):
#         pass

# def guide_task(): # printed text in terminal 
#     print(" ")
#     print('Hey! there i am dodo')
#     print("please press initiate system to start")
#     print('i can help you with variety of tasks')
#     print(" ")

# def guide_run(text):
#     threading.Thread(target=guide_task).start()


# terminal = tkinter.Text(screen_main)
# terminal.configure(background='black',foreground='white')
# terminal.configure(width=60,height=30)
# terminal.configure(font=('courier new',10))
# terminal.place(x=5,y=100)

# guide_run()

# old_stdout = sys.stdout
# sys.stdout = Redirect(terminal)


# initiate_btn = tkinter.Button(screen_main,font=('courier new',25),foreground='cyan',background='black',text='initiate',command=main_exe)
# initiate_btn.place(x=1130,y=250)


# screen_main.mainloop()
# sys.stdout = old_stdout

# bow = bag_of_words('hello')
# bow = np.array(bow)
# bow = bow.flatten()
# print(f"shape of bow : {bow.shape}")
# print(f"ndim of bow : {bow.ndim}")
# print(bow)
# print(f"this is len of bow {len(bow)}")
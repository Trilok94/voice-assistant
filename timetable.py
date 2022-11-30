from datetime import datetime
from speak import speak

fiveto6 = '''
in this time you have to get up and listen something positivly
5:00 AM to 6:00 AM
THANKS.'''

sixto9 = '''
in this time you have to study 
6:00 am to 9:00 am
thanks.'''

nineto12 = '''in this time you have to make a video and have to upload it on youtube
9:00 am to 12:00 pm
thanks.'''

twelveto15 = '''in this time you have to gain some knowledge from internet or from books 
12:00 pm to 3:00 pm 
thanks.'''

fifteento21 = '''in this time you have to code 
3:00 pm to 9:00 pm 
thanks. '''

twentyoneto22 = '''in this time you have to sleep 
9:00 pm to 10 pm 
thanks.'''


def timetable():
    hour = int(datetime.now().strftime("%H")) 
    if hour >= 5 and hour < 6: 
        # print(fiveto6) 
        speak(fiveto6)
        return fiveto6 
    elif hour >= 6 and hour < 9: 
        # print(sixto9)
        speak(sixto9) 
        return sixto9
    elif hour >= 9 and hour < 12: 
        # print(nineto12)
        speak(nineto12) 
        return nineto12
    elif hour >= 12 and hour < 15: 
        # print(twelveto15)
        speak(twelveto15) 
        return twelveto15
    elif hour >= 15 and hour < 21: 
        # print(fifteento21)
        speak(fifteento21)
        return fifteento21
    elif hour >= 21 and hour < 22:
        # print(twentyoneto22)
        speak(twentyoneto22) 
        return twentyoneto22
    else:
        return 'in this time, you have to sleep '

timetable()
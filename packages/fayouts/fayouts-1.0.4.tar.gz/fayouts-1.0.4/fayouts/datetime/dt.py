from datetime import datetime as dt

class Date():
    data = dt.now()
    day = data.day
    month = data.month
    year = data.year
    hour = data.hour
    minute = data.minute
    second = data.second
    dateRu = None
    dateUs = None
    weekday = None

    def __init__(self, lang = 'en'):
        if(self.day < 9):
            self.day = f'0{self.day}'
        if(self.month < 9):
            self.month = f'0{self.month}'
        if(self.hour < 9):
            self.hour = f'0{self.hour}'
        if(self.minute < 9):
            self.minute = f'0{self.minute}'
        if(self.second < 9):
            self.second = f'0{self.second}'
        self.dateRu = f'{self.day}.{self.month}.{self.year}'
        self.dateUs = f'{self.month}.{self.day}.{self.year}'

        if(dt.today().isoweekday() == 1):
            if(lang == "en"):
                self.weekday = "Monday"
            elif(lang == "ru"):
                self.weekday = "Понедельник"
        elif(dt.today().isoweekday() == 2):
            if(lang == "en"):
                self.weekday = "Tuesday"
            elif(lang == "ru"):
                self.weekday = "Вторник"
        elif(dt.today().isoweekday() == 3):
            if(lang == "en"):
                self.weekday = "Wednesday"
            elif(lang == "ru"):
                self.weekday = "Среда"
        elif(dt.today().isoweekday() == 4):
            if(lang == "en"):
                self.weekday = "Thursday"
            elif(lang == "ru"):
                self.weekday = "Четверг"
        elif(dt.today().isoweekday() == 5):
            if(lang == "en"):
                self.weekday = "Friday"
            elif(lang == "ru"):
                self.weekday = "Пятница"
        elif(dt.today().isoweekday() == 6):
            if(lang == "en"):
                self.weekday = "Saturday"
            elif(lang == "ru"):
                self.weekday = "Суббота"
        elif(dt.today().isoweekday() == 7):
            if(lang == "en"):
                self.weekday = "Sunday"
            elif(lang == "ru"):
                self.weekday = "Воскресенье"

def getDate(lang = 'en'):
    date = Date(lang)
    return date
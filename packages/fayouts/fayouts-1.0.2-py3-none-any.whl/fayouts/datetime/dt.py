from datetime import datetime as dt

def getData(lang = 'en'):
    data = dt.now()
    
    dy = data.year
    dm = data.month
    dd = data.day
    dh = data.hour
    dM = data.minute
    ds = data.second

    if(data.day < 10):
        dd = f'0{data.day}'
    if(data.month < 10):
        dm = f'0{data.month}'
    dy = data.year

    wd = "none"

    if(dt.today().isoweekday() == 1):
        if(lang == "en"):
            wd = "Monday"
        elif(lang == "ru"):
            wd = "Понедельник"
    elif(dt.today().isoweekday() == 2):
        if(lang == "en"):
            wd = "Tuesday"
        elif(lang == "ru"):
            wd = "Вторник"
    elif(dt.today().isoweekday() == 3):
        if(lang == "en"):
            wd = "Wednesday"
        elif(lang == "ru"):
            wd = "Среда"
    elif(dt.today().isoweekday() == 4):
        if(lang == "en"):
            wd = "Thursday"
        elif(lang == "ru"):
            wd = "Четверг"
    elif(dt.today().isoweekday() == 5):
        if(lang == "en"):
            wd = "Friday"
        elif(lang == "ru"):
            wd = "Пятница"
    elif(dt.today().isoweekday() == 6):
        if(lang == "en"):
            wd = "Saturday"
        elif(lang == "ru"):
            wd = "Суббота"
    elif(dt.today().isoweekday() == 7):
        if(lang == "en"):
            wd = "Sunday"
        elif(lang == "ru"):
            wd = "Воскресенье"

    return {
        "day": dd,
        "month": dm,
        "year": dy,
        "hour": dh,
        "minute": dM,
        "second": ds,
        "dateRu": f'{dd}.{dm}.{dy}',
        "dateUs": f'{dm}.{dd}.{dy}',
        "weekday": f'{wd}'
    }
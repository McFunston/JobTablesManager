from datetime import datetime

def PrintSalutation():
    now = datetime.now()
    salutation = str()
    currentTime = now.time()
    if currentTime.hour < 12:
        salutation = "Good morning,"
    if currentTime.hour >= 12:
        salutation = "Good afternoon,"
    if currentTime.hour >= 18:
        salutation = "Good evening,"
    print(salutation)

PrintSalutation()

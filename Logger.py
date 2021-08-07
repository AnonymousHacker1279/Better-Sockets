import time
from datetime import date

state = False

# Log a message to console.
def log(message: str):
    if state:
	    print(getDateAndTime() + " [INFO] " + message)

def logError(message: str):
    if state:
	    print(getDateAndTime() + " [ERROR] " + message)

def logWarning(message: str):
    if state:
	    print(getDateAndTime() + " [WARN] " + message)

def getDateAndTime():
    return "[" + str(date.today()) + " " + time.strftime("%H.%M.%S", time.localtime()) + "]"
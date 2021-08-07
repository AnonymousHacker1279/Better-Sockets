import time
from datetime import date

state = False

# Log a message to console.
def log(message: str):
	if state:
		print(getDateAndTime() + " [INFO] " + message)
		with open("SimpleSockets.log", 'a') as logger:
			logger.write(getDateAndTime() + " [INFO] " + message + "\n")
			logger.close()

def logError(message: str):
	if state:
		print(getDateAndTime() + " [ERROR] " + message)
		with open("SimpleSockets.log", 'a') as logger:
			logger.write(getDateAndTime() + " [ERROR] " + message + "\n")
			logger.close()

def logWarning(message: str):
	if state:
		print(getDateAndTime() + " [WARN] " + message)
		with open("SimpleSockets.log", 'a') as logger:
			logger.write(getDateAndTime() + " [WARN] " + message + "\n")
			logger.close()

def logDebug(message: str):
	if state:
		print(getDateAndTime() + " [DEBUG] " + message)
		with open("SimpleSockets.log", 'a') as logger:
			logger.write(getDateAndTime() + " [DEBUG] " + message + "\n")
			logger.close()

def getDateAndTime():
	return "[" + str(date.today()) + " " + time.strftime("%H.%M.%S", time.localtime()) + "]"
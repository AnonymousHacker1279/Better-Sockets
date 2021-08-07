import socket
import threading
import Logger

# Define Variables
connections = []
destinationAddress = None
hostIP = socket.gethostbyname(socket.gethostname())
hostPort = None
packetEncoding = "UTF-8"
socketHandler = None
packetQueue = []
clientConnection = None

# Initialize the software with host information. For sending as a client.
def initializeClient(port: int):
	global hostPort
	hostPort = port
	startSocket()
	
# Set the destination IP/hostname and port.
def setDestination(addr):
	global destinationAddress
	destinationAddress = addr

def setEncoding(encoding: str):
	global packetEncoding
	packetEncoding = encoding

def setLoggerState(state: bool):
	Logger.state = state

# Start the socket handler.
def startSocket():
	global socketHandler
	try:
		Logger.log("Socket starting...")
		socketHandler = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socketHandler.bind((hostIP, hostPort))
		
	except Exception as Error:
		Logger.logError("An exception occurred while starting the socket: " + str(Error))

def startIncomingConnection():
	try:
		global socketHandler
		global connections
		global clientConnection
		socketHandler.listen()
		conn,addr = socketHandler.accept()
		connection = conn,addr
		clientConnection = conn
		connections.append(addr[0])
		threading.Thread(target=handleClient, args=(conn,)).start()
		Logger.log("New connection from: " + str({connection}))
		
	except Exception as Error:
		Logger.logError("Error occurred while starting the connection handler: " + str(Error))

def connectClient(addr):
	socketHandler = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socketHandler.connect(addr)
	return socketHandler

def threadIncomingConnection():
	threading.Thread(target=startIncomingConnection).start()

def getBuffer(data):
	global packetEncoding
	encodedMessage = str(data).encode(packetEncoding)
	messageLength = len(encodedMessage)
	sendLength = str(messageLength).encode(packetEncoding)
	sendLength += b' ' * (64-len(sendLength))
	data = (sendLength, encodedMessage)
	return data

def checkConnected():
	global destinationAddress
	global connections
	if destinationAddress[0] in connections:
		return True
	else:
		return False

def handleClient(Connection):
	while True:
		global packetEncoding
		bufferLen = len(Connection.recv(64).decode(packetEncoding))
		if bufferLen:
			data = Connection.recv(int(bufferLen))
			# Convert received string back to a tuple
			convertedData = eval(data)
			Logger.logDebug("Received Data (type " + str(convertedData[0]) + "): " + str(convertedData[1].decode(packetEncoding)))

def disconnectClient(connection):
	try:
		Logger.log("Disconnecting client...")
		connection.close()
	except Exception as Error:
		Logger.log("Failed to disconnect client: " + str(Error))

def addPacketToQueue(data):
	global packetQueue
	try:
		Logger.log("Adding new packet to queue.")
		length, encodedData = getBuffer(data)
		packetQueue.append((length, encodedData))
	except Exception as Error:
		Logger.logError("Failed to add new packet to queue. " + str(Error))

def sendQueuedPackets():
	global packetQueue
	for object in packetQueue:
		length = packetQueue[object][0]
		encodedData = packetQueue[object][1]
		socketHandler.send(length)
		socketHandler.send(encodedData)

# Send a packet to the destination server containing an integer.
def sendPacketInt(server, data: int):
	global socketHandler
	global destinationAddress
	global clientConnection

	try:
		Logger.log("Sending packet with a data type of integer...")
		if destinationAddress == None:
			Logger.logError("No destination host/port specified.")
			raise ValueError
		if not checkConnected():
			Logger.logError("Not connected to a socket.")
			raise ValueError
		length, encodedData = getBuffer(data)
		server.send(length)
		server.send(bytearray(str(("int", encodedData)), 'utf-8'))
	except Exception as Error:
		Logger.logError("Sending packet failed (data type of integer). " + str(Error))

# Send a packet to the destination server containing a boolean.
def sendPacketBool(server, data: bool):
	global socketHandler
	global destinationAddress
	global clientConnection

	try:
		Logger.log("Sending packet with a data type of boolean...")
		if destinationAddress == None:
			Logger.logError("No destination host/port specified.")
			raise ValueError
		if not checkConnected():
			Logger.logError("Not connected to a socket.")
			raise ValueError
		length, encodedData = getBuffer(data)
		server.send(length)
		server.send(bytearray(str(("bool", encodedData)), 'utf-8'))
	except Exception as Error:
		Logger.logError("Sending packet failed (data type of boolean). " + str(Error))

# Send a packet to the destination server containing a string.
def sendPacketStr(server, data: str):
	global socketHandler
	global destinationAddress
	global clientConnection

	try:
		Logger.log("Sending packet with a data type of string...")
		if destinationAddress == None:
			Logger.logError("No destination host/port specified.")
			raise ValueError
		if not checkConnected():
			Logger.logError("Not connected to a socket.")
			raise ValueError
		length, encodedData = getBuffer(data)
		server.send(length)
		server.send(bytearray(str(("str", encodedData)), 'utf-8'))
	except Exception as Error:
		Logger.logError("Sending packet failed (data type of string). " + str(Error))
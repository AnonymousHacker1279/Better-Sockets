import socket
import threading
import Logger

# Define Variables
connections = []
destinationIP = None
destinationPort = None
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
def setDestination(ip: str, port: int):
	global destinationIP
	global destinationPort
	destinationIP = ip
	destinationPort = port

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
		Logger.log("New connection from: " + str({connection}) + "\n")
		
	except Exception as Error:
		Logger.logError("Error occurred while starting the connection handler: " + str(Error))

def getBuffer(data):
	global packetEncoding
	encodedMessage = str(data).encode(packetEncoding)
	messageLength = len(encodedMessage)
	sendLength = str(messageLength).encode(packetEncoding)
	sendLength += b' ' * (64-len(sendLength))
	data = (sendLength, encodedMessage)
	return data

def checkConnected():
	global destinationPort
	global destinationIP
	global connections
	if destinationIP in connections:
		return True
	else:
		return False

def handleClient(Connection):
	while True:
		global packetEncoding
		bufferLen = Connection.recv(64).decode(packetEncoding)
		if bufferLen:
			data = Connection.recv(int(bufferLen)).decode(packetEncoding)
			print("Data:",data)

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
	global destinationIP
	global destinationPort
	global clientConnection

	try:
		Logger.log("Sending packet with a data type of integer...")
		if destinationPort == None:
			Logger.logError("No destination port specified.")
			raise ValueError
		if destinationIP == None:
			Logger.logError("No destination IP/hostname specified.")
			raise ValueError
		if not checkConnected():
			Logger.logError("Not connected to a socket.")
			raise ValueError
		length, encodedData = getBuffer(data)
		server.send(length)
		server.send(encodedData)
		# socketHandler.send(bytes(("length", length), ("type", "int"), ("data", encodedData)))
	except Exception as Error:
		Logger.logError("Sending packet failed (data type of integer). " + str(Error))
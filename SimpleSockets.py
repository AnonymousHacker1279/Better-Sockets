import socket
import threading
import Logger
import time

# Define Variables
connections = []
destinationAddress = None
hostIP = socket.gethostbyname(socket.gethostname())
hostPort = None
packetEncoding = "UTF-8"
socketHandler = None
packetQueue = []
stopHandlingClient = None

# Initialize the software with host information. For sending as a client.
def initializeClient(port: int):
	global hostPort
	hostPort = port
	startSocket()
	
# Set the destination IP/hostname and port.
def setDestination(addr):
	global destinationAddress
	destinationAddress = addr

# Set the packet encoding. Defaults to UTF-8.
def setEncoding(encoding: str):
	global packetEncoding
	packetEncoding = encoding

# Get the packet encoding.
def getEncoding():
	return packetEncoding

# Set the logger state. Defaults to disabled.
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

class QueuePriorities():
	LOWEST = -2
	LOW = -1
	NORMAL = 0
	HIGH = 1
	HIGHEST = 2

# Start an incoming connection. This MUST be threaded!
def startIncomingConnection():
	try:
		global socketHandler
		global connections
		global stopHandlingClient
		stopHandlingClient = False
		socketHandler.listen()
		conn,addr = socketHandler.accept()
		connection = conn,addr
		connections.append(addr[0])
		threading.Thread(target=handleClient, args=(conn,)).start()
		Logger.log("New connection from: " + str({connection}))
		
	except Exception as Error:
		Logger.logError("Error occurred while starting the connection handler: " + str(Error))

# Handle a connecting client. Returns the socket handler.
def connectClient(addr):
	socketHandler = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		Logger.log("Client connecting...")
		socketHandler.connect(addr)
	except Exception as Error:
		Logger.logError("Error occurred while connecting a client: " + str(Error))
	return socketHandler

# Thread an incoming connection.
def threadIncomingConnection():
	threading.Thread(target=startIncomingConnection).start()

# Get buffer information from data.
def getBuffer(data):
	global packetEncoding
	encodedMessage = str(data).encode(packetEncoding)
	messageLength = len(encodedMessage)
	sendLength = str(messageLength).encode(packetEncoding)
	sendLength += b' ' * (64-len(sendLength))
	data = (sendLength, encodedMessage)
	return data

# Check if a client is connected.
def checkConnected():
	global destinationAddress
	global connections
	if destinationAddress[0] in connections:
		return True
	else:
		return False

# Handle a client connection.
def handleClient(Connection):
	while stopHandlingClient == False:
		global packetEncoding
		bufferLen = len(Connection.recv(64).decode(packetEncoding))
		if bufferLen:
			handleReceivedData(eval(Connection.recv(int(bufferLen))))

# Handle received data. Should be "monkey patched" to implement your own behavior with received data.
def handleReceivedData(data):
	Logger.logDebug("Received data on channel " + str(data[0]) + " (type " + str(data[1]) + "): " + str(data[2].decode(packetEncoding)))

# Disconnect a client.
def disconnectClient(connection):
	global connections
	global stopHandlingClient
	try:
		Logger.log("Disconnecting client...")
		connection.close()
		if destinationAddress[0] in connections:
			connections.remove(hostIP)
		stopHandlingClient = True
	except Exception as Error:
		Logger.log("Failed to disconnect client: " + str(Error))

# Add a packet to the queue.
def addPacketToQueue(type: str, data, channel = 0, priority = QueuePriorities.NORMAL):
	global packetQueue
	try:
		Logger.log("Adding new packet to queue.")
		length, encodedData = getBuffer(data)
		packetQueue.append((length, channel, type, encodedData, priority))
	except Exception as Error:
		Logger.logError("Failed to add new packet to queue. " + str(Error))

# Send queued packets.
def sendQueuedPackets(server):
	global packetQueue
	iteration = 0
	sortedQueue = []
	Logger.log("Sending queued packets...")

	for _ in packetQueue:
		if packetQueue[iteration][4] == 2:
			sortedQueue.append(packetQueue[iteration])
		iteration = iteration + 1
	iteration = 0
	for _ in packetQueue:
		if packetQueue[iteration][4] == 1:
			sortedQueue.append(packetQueue[iteration])
		iteration = iteration + 1
	iteration = 0
	for _ in packetQueue:
		if packetQueue[iteration][4] == 0:
			sortedQueue.append(packetQueue[iteration])
		iteration = iteration + 1
	iteration = 0
	for _ in packetQueue:
		if packetQueue[iteration][4] == -1:
			sortedQueue.append(packetQueue[iteration])
		iteration = iteration + 1
	iteration = 0
	for _ in packetQueue:
		if packetQueue[iteration][4] == -2:
			sortedQueue.append(packetQueue[iteration])
		iteration = iteration + 1

	iteration = 0
	
	for _ in sortedQueue:
		length = sortedQueue[iteration][0]
		encodedData = sortedQueue[iteration][3]
		Logger.log("Sending queued packet with type of '" + sortedQueue[iteration][2] + "'")
		server.send(length)
		server.send(bytearray(str((sortedQueue[iteration][1], sortedQueue[iteration][2], encodedData)), getEncoding()))
		iteration = iteration + 1
		# Add a slight delay so the packets arrive in order
		time.sleep(0.0000000000000000000000001)

# Send a packet to the destination server containing an integer.
def sendPacketInt(server, data: int, channel = 0):
	global socketHandler
	global destinationAddress

	try:
		Logger.log("Sending packet with a data type of integer...")
		if destinationAddress == None:
			Logger.logError("No destination host/port specified.")
			raise ValueError
		if not checkConnected():
			Logger.logError("Not connected to a socket.")
			raise ConnectionError
		length, encodedData = getBuffer(data)
		server.send(length)
		server.send(bytearray(str((channel, "int", encodedData)), getEncoding()))
	except Exception as Error:
		Logger.logError("Sending packet failed (data type of integer). " + str(Error))

# Send a packet to the destination server containing a boolean.
def sendPacketBool(server, data: bool, channel = 0):
	global socketHandler
	global destinationAddress

	try:
		Logger.log("Sending packet with a data type of boolean...")
		if destinationAddress == None:
			Logger.logError("No destination host/port specified.")
			raise ValueError
		if not checkConnected():
			Logger.logError("Not connected to a socket.")
			raise ConnectionError
		length, encodedData = getBuffer(data)
		server.send(length)
		server.send(bytearray(str((channel, "bool", encodedData)), getEncoding()))
	except Exception as Error:
		Logger.logError("Sending packet failed (data type of boolean). " + str(Error))

# Send a packet to the destination server containing a string.
def sendPacketStr(server, data: str, channel = 0):
	global socketHandler
	global destinationAddress

	try:
		Logger.log("Sending packet with a data type of string...")
		if destinationAddress == None:
			Logger.logError("No destination host/port specified.")
			raise ValueError
		if not checkConnected():
			Logger.logError("Not connected to a socket.")
			raise ConnectionError
		length, encodedData = getBuffer(data)
		server.send(length)
		server.send(bytearray(str((channel, "str", encodedData)), getEncoding()))
	except Exception as Error:
		Logger.logError("Sending packet failed (data type of string). " + str(Error))
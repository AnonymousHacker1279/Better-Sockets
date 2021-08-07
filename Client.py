import SimpleSockets
import time
import Logger

# Set the logger state: Defaults to disabled.
SimpleSockets.setLoggerState(True)

# Initialize the client by specifying the port packets will be sent from.
SimpleSockets.initializeClient(1234)

# Set the destination address.
ADDR = ("192.168.1.9", 1234)
SimpleSockets.setDestination(ADDR)

# Start an incoming connection: This MUST be threaded!
SimpleSockets.threadIncomingConnection()

# Connect to the destination address, and save our connection information
connection = SimpleSockets.connectClient(ADDR)

# Implement our own behavior for receiving data
# Also known as "monkey patching"
def handleData(data):
	# Only log items on channel 3
	if data[0] == 3:
		Logger.log("Received data (type " + str(data[1]) + "): " + str(data[2].decode(SimpleSockets.getEncoding())))

# SimpleSockets.handleReceivedData = handleData

# Send packets with varying data types
time.sleep(0.0000000000000000000000001)
SimpleSockets.sendPacketInt(connection, 9999)
time.sleep(0.0000000000000000000000001)
SimpleSockets.sendPacketBool(connection, True)
time.sleep(0.0000000000000000000000001)
SimpleSockets.sendPacketStr(connection, "Hello World!")
time.sleep(0.0000000000000000000000001)

# Add packets to a queue
SimpleSockets.addPacketToQueue("int", 1234)
SimpleSockets.addPacketToQueue("bool", False, 5, SimpleSockets.QueuePriorities.LOWEST)
SimpleSockets.addPacketToQueue("str", "Hello! This packet was queued!", 16)
SimpleSockets.addPacketToQueue("str", "This is an important packet!", 36, SimpleSockets.QueuePriorities.HIGHEST)
SimpleSockets.addPacketToQueue("int", 69420, 8, SimpleSockets.QueuePriorities.HIGH)

# Send some packets on different channels
SimpleSockets.sendPacketInt(connection, 1234, 3)
time.sleep(0.0000000000000000000000001)
SimpleSockets.sendPacketBool(connection, False, 15)
time.sleep(0.0000000000000000000000001)
SimpleSockets.sendPacketStr(connection, "Hello World! I'm on channel 32!", 32)
time.sleep(0.0000000000000000000000001)

# Use the packet queue system
SimpleSockets.sendQueuedPackets(connection)

# Disconnect the client
time.sleep(0.1)
SimpleSockets.disconnectClient(connection)
import socket
import BetterSockets
import threading
import time

# Set the logger state: Defaults to disabled.
BetterSockets.setLoggerState(True)

# Initialize the client by specifying the port packets will be sent from.
BetterSockets.initializeClient(443)

# Set the destination address.
ADDR = ("192.168.1.9", 443)
BetterSockets.setDestination(ADDR)

# Start an incoming connection: This MUST be threaded!
BetterSockets.threadIncomingConnection()

# Connect to the destination address, and save our connection information
connection = BetterSockets.connectClient(ADDR)

# Send packets with varying data types
time.sleep(0.1)
BetterSockets.sendPacketInt(connection, 9999)
time.sleep(0.1)
BetterSockets.sendPacketBool(connection, True)
time.sleep(0.1)
BetterSockets.sendPacketStr(connection, "Hello World!")
time.sleep(0.1)

# Send some packets on different channels
BetterSockets.sendPacketInt(connection, 1234, 3)
time.sleep(0.1)
BetterSockets.sendPacketBool(connection, False, 15)
time.sleep(0.1)
BetterSockets.sendPacketStr(connection, "Hello World! I'm on channel 32!", 32)
time.sleep(0.1)

# Disconnect the client
time.sleep(0.1)
BetterSockets.disconnectClient(connection)
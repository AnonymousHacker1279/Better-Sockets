import socket
import BetterSockets
import threading

betterSockets = BetterSockets
betterSockets.initializeClient(443)
betterSockets.setDestination("192.168.1.9", 443)
connectionThread = threading.Thread(target=betterSockets.startIncomingConnection)
connectionThread.start()
ADDR = ("192.168.1.9", 443)
socketHandler = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketHandler.connect(ADDR)
connectionThread.join()
betterSockets.sendPacketInt(socketHandler, 9999)
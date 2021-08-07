# SimpleSockets, by AnonymousHacker1279 and BlackApple769
Project for the XHacks Hackathon: 6/6/21-6/8/21. Aims to improve the Python 3 Socket library.

SimpleSockets aims to make it easier to send packets between programs. It acts as a wrapper for the built in ``socket`` library. 

## It's quite easy to start using SimpleSockets:

First, import the library:
```python
import SimpleSockets
```

Next, initialize your client and specify the port you want to send from (this needs to match your server port):
```python
SimpleSockets.initializeClient(1234)
```

Now set your destination address:
```python
address = ("192.168.1.9", 1234)
SimpleSockets.setDestination(address)
```

Then let the server know a client is going to connect, then connect:
```python
SimpleSockets.threadIncomingConnection()
connection = SimpleSockets.connectClient(address)
```

Last, you'll actually send your packet. You don't need to repeat the setup process each time you send a packet.
```python
SimpleSockets.sendPacketInt(connection, 9999)
SimpleSockets.sendPacketBool(connection, True)
SimpleSockets.sendPacketStr(connection, "Hello World!")
```

There are built in packet types for integers, booleans, and strings. An incoming packet looks like this: ``(3, 'int', b'1234')``.  
- The first item in the tuple is the channel number.
- The second item in the tuple is the data type (can be 'int', 'bool', or 'string')
- The third item in the tuple is the byte data (decode this using UTF-8, or another encryption set using ``SimpleSockets.setEncoding("<your encoding>")``


You'll probably want to setup your own functions for dealing with packet data. By default, SimpleSockets will print this to the terminal if you have logging enabled (``SimpleSockets.setLoggerState(True)``). To set your own handler, use "monkey patching":
```python
def handleData(data):
	# Only log items on channel 3
	if data[0] == 3:
		Logger.log("Received data (type " + str(data[1]) + "): " + str(data[2].decode(SimpleSockets.getEncoding())))

SimpleSockets.handleReceivedData = handleData
```

When you're done, disconnect the client:
```python
SimpleSockets.disconnectClient(connection)
```

## Want a demonstration?
Run ``Client.py``. It demonstrates the functions of this project. 

You can run the file from your terminal: ```python Client.py```.

#### Written with Python 3.9.6.

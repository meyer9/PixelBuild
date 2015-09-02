import sys
from time import sleep, localtime
from weakref import WeakKeyDictionary

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

class ClientChannel(Channel):
	"""
	This is the server representation of a single connected client.
	"""
	def __init__(self, *args, **kwargs):
		self.nickname = []
		Channel.__init__(self, *args, **kwargs)
	
	def Close(self):
		self._server.DelPlayer(self)
	
	##################################
	### Network specific callbacks ###
	##################################
	
	def Network_placeblock(self, data):
		print "blocks!"
		self._server.SendToAll({"action": "placedblock", "data":data["data"]})
	
	def Network_nicknamerequest(self, data):
		print "receive"
		if len(self.nickname)!=0:
			self.nickname.append(int(self.nickname[-1])+1)
			self.Send({"action":"nicknamereceive"})
		else:
			self.nickname.append(0)

class ChatServer(Server):
	channelClass = ClientChannel
	
	def __init__(self, *args, **kwargs):
		Server.__init__(self, *args, **kwargs)
		self.players = WeakKeyDictionary()
		print 'Server launched'
	
	def Connected(self, channel, addr):
		self.AddPlayer(channel)
	
	def AddPlayer(self, player):
		print "New Player" + str(player.addr)
		self.players[player] = True
		self.SendPlayers()
		print "players", [p for p in self.players]
	
	def DelPlayer(self, player):
		print "Deleting Player" + str(player.addr)
		del self.players[player]
		self.SendPlayers()
	
	def SendPlayers(self):
		self.SendToAll({"action": "players", "players": [p.nickname for p in self.players]})
	
	def SendToAll(self, data):
		[p.Send(data) for p in self.players]
	
	def Launch(self):
		while True:
			self.Pump()
			sleep(0.0001)

s = ChatServer(localaddr=("localhost", 25565))
s.Launch()


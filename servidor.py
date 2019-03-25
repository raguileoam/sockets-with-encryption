# -*- coding: utf-8 -*-
import threading
import socket
import ssl
from ssl import PROTOCOL_TLS

keyFile = "priv.pem"  # provide full path to the private key file location
certFile = "cert.crt"  # provide full path to the Certificate file location

class Server():
	def __init__(self):
		self.host = 'localhost'
		self.port = 8880
		self.maxcon = 1

	def start(self):
		self.s = socket.socket()
		self.s.bind((self.host, self.port))
		self.s.listen(self.maxcon)
		s_ssl = ssl.wrap_socket(self.s, ssl_version="TLSv1",keyfile=keyFile, certfile=certFile, server_side=True)
		while True:
			sc, addr = s_ssl.accept()
			client = Client(sc, addr)
			client.start()

class Client(threading.Thread):
	def __init__(self, sc, addr):
		threading.Thread.__init__(self)
		self.sc = sc
		self.addr = addr
		
	def run(self):
		nombre = self.sc.read(1024).decode()
		print("*** El usuario "+nombre +" se ha conectado desde" + str(self.addr))
		while True:
			recibido = self.sc.read(1024)
			if recibido.decode()=="quit":
				break
			print("[" + nombre + "]" + recibido.decode())
	  
		self.sc.send(recibido)
		print('Conexion cerrada')
		self.sc.close()

if __name__=="__main__":
	server=Server()
	server.start()


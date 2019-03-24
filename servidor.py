
import threading
import socket
from socket import AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET, SHUT_RDWR
import hashlib
from Crypto.Cipher import AES
import ssl
from ssl import PROTOCOL_TLS

keyFile = "priv.pem"  # provide full path to the private key file location
certFile = "cert.crt"  # provide full path to the Certificate file location

KEY = hashlib.sha256(str("adasd").encode('utf-8')).digest()
IV = "abcdefghijklmnop"  # Initialization vector should always be 16 bit
# creating an object to encrypt our data with
obj = AES.new(KEY, AES.MODE_CFB, IV)


class Server():
	def __init__(self):
		self.host = 'localhost'
		self.port = 8888
		self.maxcon = 1

	def start(self):
		self.s = socket.socket()
		self.s.bind((self.host, self.port))
		self.s.listen(self.maxcon)
		self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		s_ssl = ssl.wrap_socket(
		    self.s, keyfile=keyFile, certfile=certFile, server_side=True)
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
		print("*** El usuario "+nombre +"se ha conectado desde" + str(self.addr))
		while True:
			recibido = self.sc.read(1024).decode()
			if recibido=="quit":
				break
			print("[" + nombre + "]" + recibido)
			encrypted = obj.encrypt(recibido)
			print("encrypted data: "+str(encrypted))
	  
		self.sc.send(encrypted)
		print('Conexion cerrada')
		self.sc.close()


if __name__=="__main__":
	server=Server()
	server.start()


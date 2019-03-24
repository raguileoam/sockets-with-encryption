# -*- coding: utf-8 -*-
import socket
import hashlib
from Crypto.Cipher import AES
import ssl
host = "127.0.0.1"
port = 8888
s=socket.socket()
ssl_sock = ssl.wrap_socket(s, cert_reqs=ssl.CERT_REQUIRED, ca_certs='cert.crt')
ssl_sock.connect((host,port))
while True:
	mensaje=input('> ')
	if mensaje == 'quit':
		break
	mensaje=mensaje.encode() if len(mensaje)>0 else b' '
	ssl_sock.write(mensaje)
print('Conexion cerrada')
ssl_sock.close()
s.close()

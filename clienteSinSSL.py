# -*- coding: utf-8 -*-
import socket
s=socket.socket()
s.connect(('localhost',8886))
while True:
	mensaje=input('> ').encode()
	s.send(mensaje)
	if mensaje == 'quit':
		break
print('Conexion cerrada')
s.close()

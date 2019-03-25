# -*- coding: utf-8 -*-
import threading
import socket


class Server():
    def __init__(self):
        self.host = 'localhost'
        self.port = 8886
        self.maxcon = 1

    def start(self):
        self.s = socket.socket()
        self.s.bind((self.host, self.port))
        self.s.listen(self.maxcon)
        while True:
            sc, addr = self.s.accept()
            client = Client(sc, addr)
            client.start()


class Client(threading.Thread):
    def __init__(self, sc, addr):
        threading.Thread.__init__(self)
        self.sc = sc
        self.addr = addr

    def run(self):
        nombre = self.sc.recv(1024).decode()
        print('*** El usuario '+nombre+' se ha conectado desde ' + str(self.addr))
        while True:
            recibido = self.sc.recv(1024).decode()
            if recibido == 'quit':
                break
            print('[' + nombre + ']'+recibido)
            self.sc.send(recibido.encode())
        print('Conexion cerrada')
        self.sc.close()


if __name__ == "__main__":
    server = Server()
    server.start()

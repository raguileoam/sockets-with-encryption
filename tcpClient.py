import socket
import hashlib
from Crypto.Cipher import AES
import ssl

KEY = hashlib.sha256(str("asdas").encode('utf-8')).digest() #this will convert any pnemonic string which the user wants to choose as password to a 32 bit encrypted object
IV = "abcdefghijklmnop"		#Initialization vector should always be 16 bit
obj = AES.new(KEY, AES.MODE_CFB, IV)	#creating an object to encrypt our data with

def main():
	host = "127.0.0.1"
	port = 5001

	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)	#specifying TCP and IPv4
	ssl_sock = ssl.wrap_socket(s, cert_reqs=ssl.CERT_REQUIRED, ca_certs='cert.crt')	#provide full path to the certificate file location
	#the above function "wraps" the socket created with the security layer of signed certificate

	ssl_sock.connect((host,port))

	message = input("-> ")
	while message != 'q':
		message=message.encode() if len(message)>0 else b' '
		ssl_sock.write(message)	#instead of the .send() we use .write() for ssl
		data = ssl_sock.read(1024)
		print("received data: "+str(data))
		print("decrypting...")
		decrypted = obj.decrypt(data)	#using the object we created to decrypt the incoming data
		print("received from server "+str(decrypted))
		message = input("-> ")
	ssl_sock.close()

if __name__ == "__main__":
	main()

import os

ls = os.listdir()
def mk():
	if "server" not in ls:
		import socket

		os.makedirs("server/coord")
		os.makedirs("server/speed")
		os.makedirs("server/apple")
		open("server/apple/apple.txt","w")
		open("server/status.txt","w")
		open(f"server/speed/{socket.gethostbyname(socket.gethostname())}.txt","w")
		open(f"server/coord/{socket.gethostbyname(socket.gethostname())}.txt","w")
def rm():
	import shutil
	path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'server')
	shutil.rmtree(path)

# Python3 ESP32RET client
# hostile@me.com
# Tesla-rev Slack group

import sys
import sqlite3
import pathlib
import threading
import time
import logging
import socket
import binascii
#import cantools 

# Setup CAN log database
def setup():
	dbfile = pathlib.Path('model3-vehicle-bus.db')
	if not dbfile.exists():
		conn = sqlite3.connect('model3-vehicle-bus.db')
		conn.execute("CREATE TABLE CAN (TIMESTAMP INT PRIMARY KEY NOT NULL, FRAMEID TEXT NOT NULL, \
			FRAMETYPE CHAR(1) , BUS CHAR(10),  LEN CHAR(10), FRAMEDATA CHAR(256) );")
		conn.commit()
		conn.close()

logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) %(message)s',)

def heartbeat():
	# wifiUDPServer.beginPacket(broadcastAddr, 17222);
	# https://github.com/collin80/ESP32RET/blob/fe60aae17cf177ff5e287669fafc483b8ed541b9/ESP32RET.ino#L1125
	#
	# $ sudo tcpdump -i en1 port 17222
	# tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
	# listening on en1, link-type EN10MB (Ethernet), capture size 262144 bytes
	# 10:44:38.398986 IP 192.168.4.1.52403 > broadcasthost.17222: UDP, length 4
	# 10:44:39.423305 IP 192.168.4.1.52403 > broadcasthost.17222: UDP, length 4
	# 10:44:40.447630 IP 192.168.4.1.52403 > broadcasthost.17222: UDP, length 4
	# 10:44:41.471047 IP 192.168.4.1.52403 > broadcasthost.17222: UDP, length 4
	# 10:44:42.495576 IP 192.168.4.1.52403 > broadcasthost.17222: UDP, length 4

	logging.debug('Processing Heartbeat') # "//every second send out a broadcast ping"
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(("0.0.0.0", 17222))
	while True:
		data, addr = sock.recvfrom(4)	
		logging.debug( binascii.hexlify(data).decode('utf-8'))
		# (heartbeat ) b'1cefaced'

# Kick off the heartbeat listener
d = threading.Thread(name='heartbeat', target=heartbeat)
d.setDaemon(True)

def canlogger():
	# WiFiServer wifiServer(23); //Register as a telnet server
	# https://github.com/collin80/ESP32RET/blob/fe60aae17cf177ff5e287669fafc483b8ed541b9/ESP32RET.ino#L67
	#
	# Service listens on Telnet port
	#
	# $ nc 192.168.4.1 23
	# (enter)
	# -127176568 - 20c S 0 7 0 e0 45 6e 0 0 0
	# -127175125 - 201 S 0 8 b8 25 18 0 70 23 3 0
	# -127174929 - 262 S 0 6 b 0 a7 ce 0 30
	# -127174422 - 39a S 0 8 ff fe fe fe fe 0 0

#	db = cantools.database.load_file('Model3CAN.dbc')

	conn = sqlite3.connect('model3-vehicle-bus.db')
	logging.debug('Starting')
	while True:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(5)
		s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) # stop delays (?)
		s.connect(('192.168.4.1', 23))
		s.sendall(b'\n')
		sfile = s.makefile("r", buffering=1) # unbuffered streams MUST be binary. 
		for data in sfile:
			data = data.rstrip().split(" ")
			logging.debug(data)
			# (CanLogger ) ['622016298', '-', '439', 'S', '0', '8', '0', '0', '0', '1', '0', '0', '18', '3']

			packetdata = ' '.join(data[6:])
			conn.execute("INSERT INTO CAN (TIMESTAMP,FRAMEID,FRAMETYPE,BUS,LEN,FRAMEDATA) VALUES (?,?,?,?,?,?)", (data[0], data[2], data[3], data[4], data[5], packetdata ) )
			conn.commit()

			#db.decode_message(data[2], data[6:])

# Make sure DB is setup 
setup()
# Start the Can Logging program! 
t = threading.Thread(name='CanLogger', target=canlogger)

d.start()
t.start()

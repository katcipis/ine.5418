require 'socket'

SERVER_IP = 'localhost'
SERVER_PORT = 3000

MULTICAST_ADDRESS = '224.0.1.0'
MULTICAST_PORT    = 7777

MAX_UDP_PACKET_SIZE = 65536

action = 'enter'
separator = '|'

server_connection = TCPSocket.open(SERVER_IP, SERVER_PORT)  # Connect to server

puts 'Connected to the server, lets do some multicasting at: ' + MULTICAST_ADDRESS

multicast_sender = UDPSocket.open
multicast_sender.setsockopt(Socket::IPPROTO_IP, Socket::IP_TTL, [1].pack('i'))
multicast_sender.send('ping', 0, MULTICAST_ADDRESS, MULTICAST_PORT)


require 'socket'

SERVER_IP              = 'localhost'
SERVER_PORT            = 3000
MULTICAST_ADDRESS      = '224.0.1.0'
MULTICAST_PORT         = 7777
CAR_COMMUNICATION_PORT = 7000
MAX_UDP_PACKET_SIZE    = 65536 #bytes
UDP_RECV_TIMEOUT       = 5     #seconds
ENTERING_CAR           = 'enter'
EXITING_CAR            = 'exit'
MSG_SEPARATOR          = '|'

server_connection = TCPSocket.open(SERVER_IP, SERVER_PORT)  # Connect to server

puts 'connected to the server'

multicast_sender = UDPSocket.open
multicast_sender.setsockopt(Socket::IPPROTO_IP, Socket::IP_TTL, [1].pack('i'))

car_data_receiver = UDPSocket.new
#FIXME isso aqui ta ruim, se deixar nil ou localhost nao funciona =/
car_data_receiver.bind '192.168.10.3', CAR_COMMUNICATION_PORT

loop {
    puts 'searching for cars at multicast address: ' + MULTICAST_ADDRESS    
    multicast_sender.send('ping', 0, MULTICAST_ADDRESS, MULTICAST_PORT)

    puts 'vamos ver se algum carro respondeu'
    if select([car_data_receiver], nil, nil, UDP_RECV_TIMEOUT)
        plate, sender = car_data_receiver.recvfrom(MAX_UDP_PACKET_SIZE)
        puts 'carro com a placa: ' + plate + ' respondeu, vamos abrir a cancela'
        server_connection.send plate + MSG_SEPARATOR + ENTERING_CAR, 0
    else
        puts 'nenhum carro respondeu !!!'
    end 
}

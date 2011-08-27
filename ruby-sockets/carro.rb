require 'socket'
require 'ipaddr'

CAR_COMMUNICATION_PORT = 7000
MULTICAST_RECEIVE_PORT = 7777
MULTICAST_ADDRESS      = '224.0.1.0'
MAX_UDP_PACKET_SIZE    = 65536 # bytes
UDP_RECV_TIMEOUT       = 5     # seconds

if ARGV[0].nil? then
    puts "id do carro nao especificado. abortando"
    exit -1
end

car_id = ARGV[0]

ip =  IPAddr.new(MULTICAST_ADDRESS).hton + IPAddr.new("0.0.0.0").hton

receive_socket = UDPSocket.new
receive_socket.setsockopt(Socket::IPPROTO_IP, Socket::IP_ADD_MEMBERSHIP, ip)
receive_socket.bind(Socket::INADDR_ANY, MULTICAST_RECEIVE_PORT)

sender_socket = UDPSocket.open


# TODO arrumar para loop infinito
loop {
    if select([receive_socket], nil, nil, UDP_RECV_TIMEOUT)
        text, sender = receive_socket.recvfrom MAX_UDP_PACKET_SIZE
        sender_ip = sender[3]
        puts 'recebido: ' + text + ' da cancela ip: ' + sender_ip
        puts 'mandando placa[' + car_id + '] para a cancela'
        sender_socket.send(car_id, 0, sender_ip, CAR_COMMUNICATION_PORT)
        break
    end
}

require 'socket'


if ARGV[0].nil? then
    puts "id do carro nao especificado. abortando"
    exit -1
end
car_id = ARGV[0]
action = 'enter'
separator = '|';

socket = TCPSocket.open('localhost',3000)  # Connect to server
socket.send car_id+separator+action , 0
sleep(2)
response = socket.read              # Read complete response
puts response.to_s

require 'socket'

@conn = TCPServer.open(3000)   # Socket to listen on port 3000
@plates = Hash.new

ENTERING_CAR     = 'enter'
EXITING_CAR      = 'exit'
MSG_SEPARATOR    = '|'
MAX_TCP_MSG_SIZE = 1024
TCP_RECV_TIMEOUT = 5

loop {                          # Servers run forever
  Thread.start(@conn.accept) do |client|

    loop {
  
        if select([client], nil, nil, TCP_RECV_TIMEOUT)
            msg = (client.recv MAX_TCP_MSG_SIZE).split MSG_SEPARATOR
            if msg[1] == ENTERING_CAR then
                puts 'Carro com placa[' + msg[0] + '] esta entrando.'
                @plates[msg[0]] = true
            else
                puts 'Carro com placa[' + msg[0] + '] esta saindo.'
                @plates[msg[0]] = false
            end
        end
    }

  end
}

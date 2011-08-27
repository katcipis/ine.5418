require 'socket'

@conn = TCPServer.open(3000)   # Socket to listen on port 3000
@plates = Hash.new

entering_action = 'enter'
exiting_action  = 'exit'
msg_separator = '|'

loop {                          # Servers run forever
  Thread.start(@conn.accept) do |client|
    client.puts(Time.now.ctime) # Send the time to the client
    msg = (client.recv 50).split msg_separator
    if msg[1] == entering_action then
      @plates[msg[0]] = true
    else 
      @plates[msg[0]] = false
    end
    client.puts "Closing the connection. Bye!"
    client.close                # Disconnect from the client
  end
}

require 'socket'

@con = TCPServer.open(3000)   # Socket to listen on port 2000
@plates = Hash.new
loop {                          # Servers run forever
  Thread.start(@conn.accept) do |client|
    client.puts(Time.now.ctime) # Send the time to the client
    msg = (client.recv 50).split '|'
    if msg[1] == 'enter' then
      @plates[msg[0]] = true
    else 
      @plates[msg[0]] = false
    end
    client.puts "Closing the connection. Bye!"
    client.close                # Disconnect from the client
  end
}

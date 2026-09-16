import socket
import threading
#list of all clients
clients = []

#instead of only accepting 1 it will accpet and go to another client
def handle_client(connection, address): 
    #says address connected at
    print("Connected by: ", address)

    while True:
        #data that was recieved (up to 1024 bytes)
        data = connection.recv(1024)
        if not data:
            break
        #prints data
        print(f"Recieved: {data}    from {address}")
        
        for client in clients:
            #sends message to all
            client.sendall(data)
            
    connection.close()
    client.remove(connection)
    print("Disconnected: ", address)


#create sockets 
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#tells where socket wikll belong to and port to
server_socket.bind(('127.0.0.1', 65432))

#waits for a connection
server_socket.listen()
print("Waiting for connection!")


#use while loop so it doesnt only accept 1 client 
#accept -> create thread -> accept -> create thread -> repeat
while True:
     #accepts the client at a connection and address   
    connection, address = server_socket.accept()
    clients.append(connection)
    
    #create thread, will run handle_client and give in connection and address
    thread = threading.Thread(
        target = handle_client,
        args = (connection, address)
    )
    #after creating the thread, start it
    thread.start()
    
    
  


import socket
import threading


#recieves messages so you do not have to send a message to see a message
def recieve_message():
    while True:
        try:
            #data that was recieved (up to 1024 bytes)
            data = client_socket.recv(1024)
        except ConnectionAbortedError:
            break
        if not data:
            break
        #prints data on new line
        print("\nRecieved: ", data.decode())

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(("127.0.0.1", 65432))
print("Connected to server")

#creates thread for receieivn and sending message
recieve_thread = threading.Thread(
    target=recieve_message
)
recieve_thread.start()


while True:
    #gets message
    message = input(">")
    
    #if exit then stop 
    if message == "exit":
        break
    
    #sends message to all clients
    client_socket.sendall(message.encode())
    #set data as recieving any data IN up to 1024 bytes
    
#if exiting closes that clients socket
client_socket.close()
    
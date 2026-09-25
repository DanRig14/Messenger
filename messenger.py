import socket
import threading
import queue

message_queue = queue.Queue()

#recieves messages so you do not have to send a message to see a message
def recieve_message():
    while True:
        try:
            data = client_socket.recv(1024)
        except ConnectionAbortedError:
            break

        if not data:
            break

        message = data.decode().strip() 
        #handles recieving message
        if message.startswith("MESSAGE"):
            #prints message (without MESSAGE)
            print("\n" + message[8:])
            print("> ", end="", flush=True)
        else:
            #if its not a MESSAGE put into queue
            message_queue.put(message)
                
            

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(("127.0.0.1", 65432))
print("Connected to server")

#creates thread for receieivn and sending message
recieve_thread = threading.Thread(
    target=recieve_message
)
recieve_thread.start()



while True:
    #input from user
    message = input("> ")
    client_socket.sendall((message + "\n").encode())

    response = message_queue.get()
    print("Server said:", response)

    #if response from server is USERNAME allow client to into username
    if response == "USERNAME":
        username = input("Username: ")
        #sends username back from client to server
        client_socket.sendall((username + "\n").encode())

        response = message_queue.get()

        #same as username
        if response == "PASSWORD":
            password = input("Password: ")
            client_socket.sendall((password + "\n").encode())

            response = message_queue.get()

            if response == "LOGIN_SUCCESS":
                print("Successful login!")
            elif response == "LOGIN_FAILED":
                print("Login failed!")

    #if client enters exit then break connection
    if message == "exit":
        break

#if exiting closes that clients socket
client_socket.close()
    
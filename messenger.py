import socket
import threading
import queue

message_queue = queue.Queue()

#recieves messages so you do not have to send a message to see a message
def recieve_message():
    buffer = ""

    while True:
        try:
            data = client_socket.recv(1024)
        except ConnectionAbortedError:
            break

        if not data:
            break

        buffer += data.decode()

        while "\n" in buffer:
            message, buffer = buffer.split("\n", 1)

            # handles receiving message
            if message.startswith("MESSAGE"):
                # prints message (without MESSAGE)
                print("\n" + message[8:])
                print("> ", end="", flush=True)
            elif message.startswith("ERROR"):
                print("\nERROR:", message[6:])
                print("> ", end="", flush=True)

            else:
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
    # input from user
    message = input("> ")
    client_socket.sendall((message + "\n").encode())

    # LOGIN process
    if message == "LOGIN":
        response = message_queue.get()
        print("Server said:", response)

        # if response from server is USERNAME allow client to enter username
        if response == "USERNAME":
            username = input("Username: ")

            # sends username back from client to server
            client_socket.sendall((username + "\n").encode())

            response = message_queue.get()

            # same as username
            if response == "PASSWORD":
                password = input("Password: ")

                client_socket.sendall((password + "\n").encode())

                response = message_queue.get()

                if response == "LOGIN_SUCCESS":
                    print("Successful login!")
                elif response == "LOGIN_FAILED":
                    print("Login failed!")

    elif message.startswith("HISTORY"):
        while True:
            response = message_queue.get()
            if response == "HISTORY_END":
                break
            print(response)
    # if client enters exit then break connection
    if message == "exit":
        break
#if exiting closes that clients socket
client_socket.close()
    
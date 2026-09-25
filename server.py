import socket
import threading
import psycopg
from dotenv import load_dotenv
import os
from argon2 import PasswordHasher

load_dotenv()
#connects to PostgresSQL
password_hasher = PasswordHasher()
connection = psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = connection.cursor()
print("Connected to Database!")
cursor.execute(
    "SELECT username, password_hash FROM users WHERE username = %s;",
    ("bob",)
)

user = cursor.fetchone()

print(user)
#list of all clients
clients = []

logged_in_users = {}

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#instead of only accepting 1 it will accpet and go to another client
def handle_client(connection, address):
    #what stage of the login proccess the client is int
    login_stage = None
    #if they are logged in
    logged_in_user = None
    print("Connected by:", address)

    buffer = ""

    while True:
        try:
            data = connection.recv(1024)
        except ConnectionResetError:
            break

        if not data:
            break


        buffer += data.decode()


        while "\n" in buffer:
            message, buffer = buffer.split("\n", 1)
            print("MESSAGE:", repr(message))
            
            
            #LOGIN PROCESS
            if message == "LOGIN":
                login_stage = "username"
                print("Client wants login")
                connection.sendall(b"USERNAME\n")

            elif login_stage == "username":
                username = message
                print("Username:", username)
                login_stage = "password"
                connection.sendall(b"PASSWORD\n")

            elif login_stage == "password":
                password = message
                print("Password:", password)
                cursor.execute(
                    "SELECT password_hash FROM users WHERE username = %s", (username,)
                    )
                user = cursor.fetchone()
                
                if user is None:
                    connection.sendall(b"LOGIN_FAILED\n")
                else:
                    password_hash = user[0]

                    #check if password is correct
                    try:
                        password_hasher.verify(password_hash, password)
                        logged_in_user = username
                        logged_in_users[username] = connection
                        print(logged_in_users)
                        connection.sendall(b"LOGIN_SUCCESS\n")
                    except:
                        connection.sendall(b"LOGIN_FAILED\n")
                login_stage = None
                #if user tries to send message then send a message if they are logged in
            elif logged_in_user is not None and message.startswith("MESSAGE"):
                handle_message(message,logged_in_user)           
            

    connection.close()
    clients.remove(connection)
    print("Disconnected:", address)


#handles sending messages
def handle_message(message, sender):
    #gets message and prints it
    print("Message Command: ", message)
    #takes message and splits it into 3 parts
    parts = message.split(" ", 2)
    #who the reciever is
    reciever = parts[1]
    #what the message is
    msg = parts[2]
    
    #because PostgresSQL uses user_id for storing, must grab the id from the user
    cursor.execute(
        "SELECT id FROM users WHERE username = %s",(sender,)
    )
    #sets variable id for user_id
    sender_id = cursor.fetchone()[0]
    #prints sender's id
    print("SENDER ID: ", sender_id)
    #gets connection where the message will go / the recievers connection
    reciever_connection = logged_in_users.get(reciever)
    print(reciever_connection)
    #if there is no connection then there is no user or they are offline
    if reciever_connection is None:
        print("User not online or not available")
    #if connection prints reciever
    else:
        print("Sending message to", reciever)
        #sends message
        reciever_connection.sendall(
            ("MESSAGE " + sender + ": " + msg + "\n").encode()
        )
        print("Message sent!")
    

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
    
    
  


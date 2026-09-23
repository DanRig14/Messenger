import socket
import threading
import psycopg
from dotenv import load_dotenv
import os
from argon2 import PasswordHasher

load_dotenv()

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
    login_stage = None
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

                    try:
                        password_hasher.verify(password_hash, password)
                        logged_in_user = username
                        connection.sendall(b"LOGIN_SUCCESS\n")
                    except:
                        connection.sendall(b"LOGIN_FAILED\n")
                login_stage = None
            
            
            

    connection.close()
    clients.remove(connection)
    print("Disconnected:", address)


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
    
    
  


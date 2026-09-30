# Messenger Protocol

## Overview

The Messenger application uses TCP sockets for communication between the client and server.

Messages are separated using newline characters (`\n`). Each message sent between the client and server must end with a newline.

The client communicates with the server using predefined commands and responses.

## Authentication

The client begins authentication by sending:

LOGIN

----
Client → Server: LOGIN
Server → Client: USERNAME
Client → Server: <username>
Server → Client: PASSWORD
Client → Server: <password>
Server → Client: LOGIN_SUCCESS or LOGIN_FAILED
----

## Messaging

After successfully logging in, the client can send a message using:

MESSAGE <username> <message>

Example:

MESSAGE alice Hello Alice!

The server:
1. Identifies the logged-in sender.
2. Finds the receiver using the username.
3. Stores the message in the database.
4. Sends the message to the receiver if they are connected.

----
Client → Server: MESSAGE alice Hello Alice!
Server → Database: Store message
Server → Receiver: MESSAGE bob Hello Alice!
----



## History

After succesfully loggin in, client can see message history with another user:

HISTORY <username>

Example:

HISTORY alice

The server retrieves messages exchanged between the logged-in user and the requested user from the database.

The server sends each message to the requesting client and then sends:

HISTORY_END

The client continues receiving history messages until it receives `HISTORY_END`.

Example flow:

Client → Server: HISTORY alice
Server → Client: bob: Hello Alice! ...
Server → Client: alice: Hey Bob! ...
Server → Client: HISTORY_END



## Protocol Rules

### Message Framing

All messages sent between the client and server use newline-delimited framing.

Each message must end with `\n`.

Example:

MESSAGE alice Hello Alice!\n

The receiver buffers incoming data and processes each complete message when a newline is received.

### Authentication Requirement

The client must successfully log in before accessing authenticated features such as messaging and message history.

### Usernames

Usernames are used to identify message recipients and must correspond to an existing user in the database.

### Server Authority

The server is responsible for:
- Authenticating users
- Determining the logged-in user's identity
- Checking permissions
- Storing messages
- Retrieving message history
- Delivering messages to connected users

The client does not directly access the database.

### Connection

Each client maintains a TCP connection to the server while using the application.
# Worker Messaging System
A role based messaging system built from scratch to learn networking, user authentication, databases, concurrency, threading, and systems programming.

Tech: Python, PostgresSQL, TCP, Argon2, Git

## Overview

* Built a multi-client threaded TCP server to allow real-time communciation between users
* Implemented Postgres backend user authentication with Argon2 password hashing for security
* Implementing private and group messaging based on role of users


# Conventions

### Bug Naming
* Formatting (Looks) as Fx0001
* Messages (Message not going through, not being displayed, etc) Mx0001
* Database (Messages/User not connecting to Postgres or anything related) DBx0001
* Functional (not being able to send message, type, login) FNx0001

# Known Bugs

## ID    |Status |Priority   |Date added |Date fixed |Description
- Fx0001    open    low     09/24/2026       xxx        There is an unnesecary space betwen last text and incoming message
- FNx0001   open    high    09/24/2026       xxx        After you send a message you are put on a newline and unable to type or "crtl + c"



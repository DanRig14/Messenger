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

<table>
<tr>
<td width="50%" valign="top">

### F0001 - Message Spacing

**Status:** Open  
**Priority:** Low  
**Date Added:** 09/24/2026  
**Date Fixed:** —  

**Description** There is an unnecessary space between the last text and an incoming message.

</td>

<td width="50%" valign="top">

### FN0001 - Message Input

**Status:** Open  
**Priority:** High  
**Date Added:** 09/24/2026  
**Date Fixed:** —  

**Description** After sending a message, the client moves to a new line and becomes unable to accept input or `Ctrl+C`.

</td>

</tr>
</table>

-------

<table>
<tr>
<td width="50%" valign="top">

### xxx -

**Status:**    
**Priority:**    
**Date Added:**  
**Date Fixed:** —  

**Description**

</td>

<td width="50%" valign="top">

### xxx -

**Status:**   
**Priority:**   
**Date Added:** 
**Date Fixed:** —  

**Description**

</td>
</tr>
</table>

<table>
<tr>
<td width="50%" valign="top">

### xxx -

**Status:**    
**Priority:**    
**Date Added:**  
**Date Fixed:** —  

**Description**

</td>

<td width="50%" valign="top">

### xxx -

**Status:**   
**Priority:**   
**Date Added:** 
**Date Fixed:** —  

**Description**

</td>
</tr>
</table>
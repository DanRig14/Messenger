#TEST AND LEARNING
import psycopg
from argon2 import PasswordHasher
from dotenv import load_dotenv
import os
load_dotenv()


password_hasher = PasswordHasher()

#connects to Postgres
connection = psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

print("Connected to PostgreSQL!")

#cursor is what sends teh data between
cursor = connection.cursor()

choice = input("Create User or Login? (c/l): ").lower().strip()

if choice == "c":
    try:
        username = input("Enter username: ")
        password = input("Enter password: ")

        password_hash = password_hasher.hash(password)

        cursor.execute(
            "INSERT INTO users (username, role, password_hash) "
            "VALUES (%s, %s, %s);",
            (username, "user", password_hash)
        )

        connection.commit()

    except psycopg.errors.UniqueViolation:
        connection.rollback()
        print("Username already exists!")

    else:
        print("User created!")
            
elif choice == "l":
    username = input("Enter username: ")
    cursor.execute(
    "SELECT username, password_hash FROM users WHERE username = %s;",
        (username,))
    
    user = cursor.fetchone()
    
    if user is None:
        print("User does not exist")

    else:
        password = input("Enter password: ")

        try:
            password_hasher.verify(user[1], password)
            print("Login successful!")
            print("Username:", user[0])

        except:
            print("Incorrect password")
       

#checks if user in in database

   

#close connection to Postgres
connection.close()
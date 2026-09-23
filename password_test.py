from argon2 import PasswordHasher

#creates pwHash object
password_hasher = PasswordHasher()

#user input
password = input("Enter Password: ")

#puts password into hasher and asigns the new password to the hasher
password_hash = password_hasher.hash(password)

print("\nHash:")
print(password_hash)

try:
    password_hasher.verify(password_hash, password)
    print("Password is Correct!")   
    
except:
    print("Password is Incorrect!")
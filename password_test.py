from argon2 import PasswordHasher

#creates pwHash object
password_hasher = PasswordHasher()


password_hasher = PasswordHasher()

password_hash = password_hasher.hash("bye")

print(password_hash)

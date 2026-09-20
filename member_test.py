import sqlite3

connection = sqlite3.connect("makerspace.db")
cursor = connection.cursor()

name = input("Enter your name: ")
email = input("Enter your email: ")

cursor.execute("""
INSERT INTO members (member_name, email)
VALUES (?, ?)
""", (name, email))

connection.commit()

print("Member registered successfully!")

connection.close()
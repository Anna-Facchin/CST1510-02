import bcrypt
from pathlib import Path

USERS_FILE = Path(__file__).parent / "DATA" / "users.txt"

def hash_password(password):
    #Hash the password
        binary_password = password.encode('utf-8') #convert the password to bytes
        salt = bcrypt.gensalt() #generate 
        hashed_password = bcrypt.hashpw(binary_password, salt)
        return(hashed_password.decode('utf-8')) # return the hased password as a string

def register(username,password):
      #log the username and hashed password
        with open(USERS_FILE, "a") as f: #open file in append mode 
            hashed_password = hash_password(password) # hash password
            f.write(f"{username},{hashed_password}\n")
        print(f"User {username} Registered successfully.")

def is_valid_password(password, hashed_password):
      return bcrypt.checkpw(password.encode('utf-8'),hashed_password.encode('utf-8'))

def login(username,password):
      with open(USERS_FILE, "r") as f:
            for line in f:
                  stored_username, stored_hashed_password = line.strip().split(",")
                  if username == stored_username:
                        if is_valid_password(password, stored_hashed_password):
                              print("Login successful!")
                              print(f"Welcome , {username}!")
                        else:
                              print("Incorrect password ")
                  


if __name__ == "__main__":

    while True:
          choice = input("Do you want to (1) Register or (2) Login (3) Exit ")
          if choice == "1":
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                register(username,password)
          elif choice == "2":
                username = input("Enter your username: ")
                password = input("Enter your username: ")
                login(username,password)

                
          elif choice == "3":
                print("Exiting the program.")
                break
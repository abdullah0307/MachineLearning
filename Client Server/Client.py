# Author: Basem Hussain and Matt Dalton
# Creation date: 15 February
# Editing date: 22 February

# Loading Library
import socket
import sys

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

# Host and the server are on the same machine so
# we use local host for and the client both
HOST = '127.0.0.1'

# Port number is for the application that is running on client side
PORT = 65457

# Initially the user is represented as unknown
user = "UNKNOWN"

# Start the socket to input
# and output the stream to the client and the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Whenever the server online the client can connect to
# the server until the client program waits
s.connect((HOST, PORT))

# Message shows now the server and client are connected
print("Welcome to the Quiz system! ")
while True:
    # Loop to input the user credentials
    while True:
        # Ask the question that the user is a student
        data_input = input(
            "Are you a Student ( " + OKGREEN + "y/yes" + ENDC + " | " + WARNING + "no/n " + ENDC + "| " + FAIL + "exit" + ENDC + ") : ").strip()
        # if yes then print message that your identification is as a student
        if data_input in ["y", "yes", "no", "n"]:
            print(" \"exit\" command can be used for exit")
            if data_input in ["y", "yes"]:
                print("[STUDENT] You are identified as a Student")
                user = OKGREEN + "STUDENT" + ENDC
                data_input = "yes"
            # if no then print message that your identification is as a teacher
            else:
                print("[INSTRUCTOR] You are identified as a Instructor")
                user = OKGREEN + "INSTRUCTOR" + ENDC
                data_input = "No"
            break
        else:
            # other wise if user enter something else then the loop will break and exit
            if data_input == "exit":
                print("Good Bye !")
                s.close()
                sys.exit(-1)
            print("Wrong input : Input should be  y/yes/no/n | exit")

    # Send the data to the server
    s.send(str.encode(data_input))
    # receive the message from the socket
    data = s.recv(1024)
    # After that decode the stream incoming from the server
    print(data.decode())
    # Now loop again for the user input
    while True:
        # Here we will input the name from the user
        data_input = input("[" + user + "] >> ")
        # Exit the loop by the 'exitS' or 'exitI' command
        if data_input == 'exitS':
            s.send(str.encode(data_input))
            break
        if data_input == 'exitI':
            s.send(str.encode(data_input))
            break
        # After inputting send it to the server
        s.send(str.encode(data_input))
        # Now again receive the response from the server
        data = s.recv(1024)
        # if the response is exit then close the socket and exit the program

        if data == b'exit':
            print("Good Bye !")
            s.close()
            sys.exit(-1)
        elif data == b"upload file":
            with open("Student list.csv", 'r') as f:
                for i in f.readlines():
                    print("Sent: ", i)
                    s.send(str.encode(i))

            s.send(str.encode("Break", "UTF-8"))
        elif data == b'upload quiz':
            with open("Quiz.csv", 'r') as f:
                for i in f.readlines():
                    print("Sent: ", i)
                    s.send(str.encode(i))
            s.send(str.encode("Break", "UTF-8"))
        else:
            # Other wise print the message received from the server other than 'exit'
            print(data.decode())

# Author: Basem Hussain and Matt Dalton
# Creation date: 15 February
# Editing date: 22 February

# Loading libraries
import datetime
import re
import socket

# Threading for the server session
import sys
from threading import Thread

# As the host and server are on the same machine so we use local host(Same IP)
import tqdm

HOST = '127.0.0.1'  # Standard loop back interface address (localhost)
# Port of the application of the client side is 65457
PORT = 65457  # Port to listen on (non-privileged ports are > 1023)

# Server side ID and Password to match
# that the instructor input correct ID and Password
instructor = {
    "ID": "012345678",
    "Password": "adminpass"
}
# Server side student credentials to match
# that the user input correct Name, Id and password
students = [
    {
        "FirstName": "Basem",
        "LastName": "Hussain",
        "ID": "023456789",
        "Password": "abc123"
    }
]
# Quiz 1,2,3 details information on the server
quiz = [
    {
        # Quiz 1 Details on server
        "QuizName": "Quiz01",
        "availableOn": datetime.datetime(2020, 5, 17),
        "deadLine": datetime.datetime(2021, 5, 17),
        "points": 10,
        "attends": [],
        # Questions for the student
        "Questions": [
            {
                "Qs": "Question1",
                "Answer": True
            },
            {
                "Qs": "Question1",
                "Answer": True
            },
            {
                "Qs": "Question1",
                "Answer": True
            }
        ],
        # The marks that are saved at each question
        "marks": {}
    },
    {
        # Quiz 2 Details on server
        "QuizName": "Quiz02",
        "availableOn": datetime.datetime(2020, 5, 17),
        "deadLine": datetime.datetime(2021, 5, 17),
        "points": 10,
        "attends": [],
        # The Questions details for the student
        "Questions": [
            {
                "Qs": "Question1",
                "Answer": True
            },
            {
                "Qs": "Question1",
                "Answer": True
            },
            {
                "Qs": "Question1",
                "Answer": True
            }
        ],
        # Marks obtain at each question
        "marks": {}
    },
    {
        # Quiz 3 Details on server
        "QuizName": "Quiz03",
        "availableOn": datetime.datetime(2020, 5, 17),
        "deadLine": datetime.datetime(2021, 5, 17),
        "points": 10,
        "attends": [],
        # Questions of the quiz 3 saved on the server
        "Questions": [
            {
                "Qs": "Question1",
                "Answer": True
            },
            {
                "Qs": "Question1",
                "Answer": True
            },
            {
                "Qs": "Question1",
                "Answer": True
            }
        ],
        "marks": {}
    }
]


# The Thread that will run for the server session for data stream in and out
class ClientThread(Thread):
    # when the object is created the ipddress ,port and the client port is initialized
    def __init__(self, ip, port, client):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.client = client
        print("[+] New server socket thread started for " + ip + ":" + str(port))

    # when the object thread is started then the server
    # will receive the input from the client using the stream function
    def run(self):
        while True:
            data = self.client.recv(2048)

            # If the client input exit then the server
            # will close with an exit message and the loop will break
            if data == b'exit':
                self.client.send(b'exit')
                self.client.close()
                print("[-] Server socket thread ended for " + self.ip + ":" + str(self.port))
                break

            # If the authentication failed then the
            auth: bool = False
            currentUserID = None
            p = re.compile('[0-9]{9}')
            date_re = re.compile('^(0[1-9]|1[012])[/](0[1-9]|[12][0-9]|3[01])[/](19|20)\d\d$')
            # After the authentication if response is yes
            if data == b'yes':
                # Start the loop of the inputting data
                while True:
                    # Send the question to the client
                    self.client.send(b'Please Insert Your ID ')
                    # Loop while the user input correct ID
                    while True:
                        userID = self.client.recv(2048)
                        # Check for the input ID is
                        # with correct Length and value after decoding the value
                        if len(userID.decode()) == 9 and p.match(userID.decode()) != None:
                            # Store the User ID
                            currentUserID = userID.decode()
                            break
                        else:
                            # Other wise loop again for the input
                            self.client.send(b'Invalid ID : Please Insert again : ')
                    # Now send the Question to enter Password to the client
                    self.client.send(b'Please Insert Your Password: ')
                    # loop for the input stream
                    while True:
                        # Receieve the password
                        password = self.client.recv(2048)
                        # Check for the password is not empty and the length
                        # is correct and password is correct
                        if (' ' in password.decode()) == False and len(password.decode()) > 0:
                            break
                        else:
                            # Loop again to input password again
                            self.client.send(b'Invalid Password : Please Insert again : ')

                    # Check for the student is in the server database
                    for student in students:
                        # Check the Password matches then set the authentication flag to True
                        if student["ID"] == userID.decode() and student["Password"] == password.decode():
                            auth = True
                            print(userID)
                            # Show the message client login successfully
                            self.client.send(b'Successfully Authenticated!.\nWaiting for student commands')
                    # If Authentication is successful then Break the inputting loop
                    if auth:
                        break
                # Now loop again to receive the command input by the client
                while True:
                    # Receive the command
                    data = self.client.recv(2048).decode()
                    # Split the command message
                    command = data.split(' ')

                    # If the user input that command "changeMyPwd" and with an argument
                    if command[0] == 'changeMyPwd' and len(command) == 2:
                        # Check the argument is non empty and no space in the argument
                        if (' ' in command[1]) == False and len(command[1]) > 0:
                            i = 0
                            # Track the student in the list
                            for student in students:
                                # Match the ID of the student
                                if student["ID"] == currentUserID:
                                    # Now replace the password
                                    students[i]["Password"] = command[1]
                                    # Display the message password has changed to the user
                                    self.client.send(b'Successfully changed password.')
                                    break
                                i += 1
                        else:
                            # If changes failed then loop again after showing the message
                            self.client.send(b'Operation Failed. [password did not meet requirement]')

                    # If the input command is 'listOpenQ' and the command without any argument
                    elif command[0] == 'listOpenQ' and len(command) == 1:
                        # Show the message to open quiz
                        message = "Open Quiz \n"
                        index = 0
                        # iterate over the quiz dictionary
                        for q in quiz:
                            # Extract the date and time of the quiz
                            # Check wether the available date is valid under the valid limit
                            if q["availableOn"] <= datetime.datetime.today() and q[
                                "deadLine"] >= datetime.datetime.today():
                                index += 1
                                quizName = q["QuizName"]
                                points = q["points"]
                                deadLine = q["deadLine"].strftime("%m-%d-%Y")
                                available = q["availableOn"].strftime("%m-%d-%Y")
                                # Show the message with the details
                                message += f"  {index} : Quiz Name: {quizName}  | Points : {points:.2f} |  Available at : {available} | Deadline : {deadLine}\n"
                        message += "There is " + str(index) + " open quiz.\n"
                        # Now show the details message over the user end machine
                        self.client.send(str.encode(message, 'UTF-8'))
                    # If the client input 'showMyGrades' without any argument

                    elif command[0] == 'showMyGrades' and len(command) == 1:
                        # Show the Report message with Student ID
                        message = f"My Report \n Student ID  : {currentUserID} \n"

                        index = 0
                        found = False
                        # Iterate over the quiz dictionary
                        for q in quiz:
                            # Extract the quiz name and marks
                            q_name = q["QuizName"]
                            marks = q["marks"]
                            # If the user ID found in the attends
                            if currentUserID in q["attends"]:
                                index += 1
                                # Extract the name, marks of the current User ID
                                m = marks[currentUserID]
                                message += f"  {index} : Quiz Name: {q_name}  | marks : {m}\n"
                                found = True
                            # Otherwise if the deadline is available then show the Quiz name, marks
                            elif q["deadLine"] < datetime.datetime.today():
                                index += 1
                                message += f"  {index} : Quiz Name: {q_name}  | marks : {0}\n"
                                found = True
                        # If not found then Show message no records found against current user
                        if not found:
                            message += f" No Records Found ! \n"
                        self.client.send(str.encode(message, 'UTF-8'))
                    # If the user input the 'takeQ' command with an argument

                    elif command[0] == 'takeQ' and len(command) == 2:
                        found = False
                        # Iterate over the quiz
                        for q in quiz:
                            # if the argument if found in the quiz name
                            if q["QuizName"] == command[1]:
                                # if the current user attended the quiz
                                if currentUserID in q["attends"]:
                                    # Show the message 'Already attended. cannot attend again!'
                                    self.client.send(b'Already attended. cannot attend again!')
                                    found = True
                                    break
                                # Check the 'available date' is available
                                if q["availableOn"] > datetime.datetime.today():
                                    # Show the message to the client that the Quiz is not opened yet
                                    self.client.send(b'Quiz is not opened yet.!')
                                    found = True
                                    break
                                # Check if the deadline is gone
                                if q["deadLine"] < datetime.datetime.today():
                                    # Show the message to the client quiz cannot attempt it
                                    self.client.send(b'Cannot attempt. Quiz In Close State')
                                    found = True
                                    break

                                # Add the user attempting record into the attempted database
                                found = True
                                q["attends"].append(currentUserID)
                                points = q["points"]
                                name = q["QuizName"]
                                index = 1
                                qsCount = len(q["Questions"])
                                mark = 0
                                correct = 0

                                # Show the Available question to send
                                print(len(q["Questions"]))
                                # Iterate over the questions
                                for question in q["Questions"]:
                                    # Store the question and answer
                                    qs = question["Qs"]
                                    qs_answer = question["Answer"]
                                    # Now send the question and ask for the answer
                                    question_line = f"  {index} / {qsCount} : Qs :{qs} \nYour Answer (T/F)"
                                    self.client.send(str.encode(question_line, 'UTF-8'))
                                    userAnwer = ""
                                    # loop to recieve the client answer response
                                    while True:
                                        # Save the answer and check it is true or false
                                        userAnwer = self.client.recv(2048)
                                        # if answer is received then break the loop
                                        if userAnwer.decode() in ["F", "T"]:
                                            break
                                        # otherwise send message input the correct answers.
                                        else:
                                            self.client.send(b'Please input answer as F or T')
                                    # Display the answer value and the question
                                    print(userAnwer, userAnwer == 'T', qs_answer)
                                    # If Answer is correct update the correct answer score
                                    if (userAnwer.decode() == 'T' and qs_answer) or (
                                            userAnwer.decode() == 'F' and not qs_answer):
                                        correct += 1
                                    # Move to the next index
                                    index += 1
                                # increase the marks percentage
                                mark += points * correct / qsCount
                                # Calculate the results
                                result = f"Mark : {mark:.2f} | Correct : {correct}"
                                q["marks"][currentUserID] = mark
                                # Now send the answer to the client side as a result
                                self.client.send(str.encode(result, 'UTF-8'))
                            # if question found then break the loop
                            if found:
                                break
                        # if question not found loop again with the message 'There is no quiz with given name'
                        if not found:
                            self.client.send(b'There is no quiz with given name')
                    # If the user enter the exit command then exit the server main loop and close the socket

                    elif command[0] == 'exit' and len(command) == 1:
                        self.client.send(b'exit')
                        self.client.close()
                        print("[-] Server socket thread ended for " + self.ip + ":" + str(self.port))
                        sys.exit(-1)
                    # Any other command outside from the option list consider as invalid command and message will shown
                    elif command[0] == 'exitS':
                        print("Student loop broken")
                        break
                    else:
                        self.client.send(b'Invalid Command')
            # Else case is for the instructor side questions
            else:
                # Loop to input the ID of the instructor
                while True:
                    self.client.send(b'Please Insert Your ID ')
                    # Loop while receive the user ID
                    while True:
                        # Store the recieved user id
                        userID = self.client.recv(2048)
                        # Check that the length is 9 and found in the ID Data
                        if len(userID.decode()) == 9 and p.match(userID.decode()) != None:
                            currentUserID = userID.decode()
                            break
                        # otherwise input the Id again if not found
                        else:
                            self.client.send(b'Invalid ID : Please Insert again : ')
                    # Now input the password of the correspnding user id
                    self.client.send(b'Please Insert Your Password: ')
                    # Loop while the user input the password
                    while True:
                        password = self.client.recv(2048)
                        # Check that the password is not empty and the length greater than zero
                        if (' ' in password.decode()) == False and len(password.decode()) > 0:
                            break
                        # If not match then show the message to input the password again
                        else:
                            self.client.send(b'Invalid Password : Please Insert again : ')
                    # Check that the instructor ID matches and Password matches
                    if instructor["ID"] == userID.decode() and instructor["Password"] == password.decode():
                        # Make the authentication to true
                        auth = True
                        print(userID)
                        self.client.send(b'Successfully Authenticated!.\nWaiting For Instructor Command')
                    # if authenticated than break the loop
                    if auth:
                        break
                # Now wait for the new command that the user input
                while True:
                    # Get the new command
                    data = self.client.recv(2048).decode()
                    command = data.split(' ')
                    # if the user input changePwd command with an argument
                    if command[0] == 'ChangePwd' and len(command) == 2:
                        # Check that the command is not empty and argument doesnot contain zero
                        if (' ' in command[1]) == False and len(command[1]) > 0:
                            # Check that the intructor ID matched
                            if instructor["ID"] == currentUserID:
                                # Store the password
                                instructor["Password"] = command[1]
                                # Now show the message that the password changed successfully
                                self.client.send(b'Successfully changed password.')
                        # If Wrong command then show the message that the "password did not meet requirement "
                        else:
                            self.client.send(b'Operation Failed. [password did not meet requirement ]')
                    # if the user input listQ command with an argument
                    elif command[0] == 'listQ' and len(command) == 1:
                        message = "Quiz List \n"
                        index = 0
                        # Iterate over all the quiz questions
                        for q in quiz:
                            index += 1
                            # Store all the question details
                            quizName = q["QuizName"]
                            points = q["points"]
                            deadLine = q["deadLine"].strftime("%m-%d-%Y")
                            available = q["availableOn"].strftime("%m-%d-%Y")
                            state = "Close"

                            # Change the state of the of the question if the time is available or not
                            if q["availableOn"] <= datetime.datetime.today() and q[
                                "deadLine"] >= datetime.datetime.today():
                                state = "Open"
                            elif q["availableOn"] >= datetime.datetime.today():
                                state = "Future"

                            # Show the question details in a message
                            message += f"  {index} : Quiz Name: {quizName}  | Points : {points:.2f}| Available at: {available} | Deadline : {deadLine} | State : {state}\n"
                        message += str(index) + " quiz found.\n"

                        # send the message to the client
                        self.client.send(str.encode(message, 'UTF-8'))
                    # If the user input the 'showQ' command with an argument
                    elif command[0] == 'showQ' and len(command) == 2:
                        # Now the message is Quiz List
                        message = "Quiz List \n"
                        found = False
                        # Iterate over the list of quiz
                        for q in quiz:
                            # if question found
                            if command[1] == q["QuizName"]:
                                # Extact the question details
                                quizName = q["QuizName"]
                                points = q["points"]
                                deadLine = q["deadLine"].strftime("%Y-%m-%d %H:%M:%S")

                                state = "Close"
                                # Check for the question time is avaliable
                                if q["availableOn"] <= datetime.datetime.today() and q["deadLine"] >= datetime.datetime.today():
                                    state = "Open"
                                elif q["availableOn"] >= datetime.datetime.today():
                                    state = "Future"
                                # Now display all the question details
                                message += f"-----------\nQuiz Name: {quizName} \nPoints : {points:.2f} \nDeadline : {deadLine} \nState : {state}\n-----------"
                                found = True
                        # Now if the question is not found here
                        if not found:
                            message = "Not Found Quiz for given name"
                        self.client.send(str.encode(message, 'UTF-8'))
                    # If the user input 'listS' commands
                    elif command[0] == 'listS' and len(command) == 1:
                        message = "Students List \n"
                        index = 0
                        # Iterate over the student lists
                        for student in students:
                            index += 1
                            firstName = student["FirstName"]
                            lastName = student["LastName"]
                            ID = student["ID"]
                            message += f"  {index} : {ID} : Name: {firstName} {lastName} \n"
                            # Check into the quiz list
                            for q in quiz:
                                quiz_name = q["QuizName"]
                                mark = "not attempt"
                                # Match the attending time
                                if ID in q["attends"]:
                                    mark = q['marks'][ID]
                                message += f"       Quiz: {quiz_name}  => Marks: {mark}\n"
                        # Complete all the list of the students
                        # found with their quiz attempted details
                        message += str(index) + " students found.\n"
                        # Show it to the message in the client side
                        self.client.send(str.encode(message, 'UTF-8'))
                    # If the user input the 'addQ' command with 4 arguments
                    elif command[0] == 'addQ' and len(command) == 5:
                        # Check that the command argument number 2 and 3 is not empty
                        if date_re.match(command[2]) == None and date_re.match(command[3]) == None:
                            # send that the date format is should be 'mm/dd/yyyy'
                            self.client.send(b'Invalid date format  : data format should be mm/dd/yyyy')
                            break
                        # input the choice of the client
                        numberMat = re.compile('^\\d+$')
                        # Check if the 4 index argument is not matched
                        if numberMat.match(command[4]) == None:
                            self.client.send(b'Point should be number ')
                            break

                        found = False
                        # Iterate into the quizzes
                        for q in quiz:
                            # Search for the Quiz the user inputted
                            if command[1] == q["QuizName"]:
                                found = True
                                break;
                        # If the quiz found then send the message that the Quiz is duplicate
                        if found:
                            self.client.send(b'Duplicate Quiz Name. ')
                            break

                        d1 = command[2].strip().split('/')
                        d2 = command[3].strip().split('/')

                        availableOn = None
                        deadLine = None

                        try:
                            # Extract the avaliabe date time and deadline
                            availableOn = datetime.datetime(int(d1[2]), int(d1[0]), int(d1[1]))
                            deadLine = datetime.datetime(int(d2[2]), int(d2[0]), int(d2[1]))
                            # append the quiz Details
                            quiz.append({
                                "QuizName": command[1],
                                "availableOn": availableOn,
                                "deadLine": deadLine,
                                "points": int(command[4].strip()),
                                "attends": [],
                                "Questions": [
                                ],
                                "marks": {}
                            })
                            # send the "quiz questions to the successfully answer" into the message
                            self.client.send(str.encode("Successfully add a quiz", 'UTF-8'))
                        # If any error occurs then send message to check the date
                        except:
                            self.client.send(b'Please Check insert date ')
                            break
                    # If the user input the 'addS' command with 4 arguments
                    elif command[0] == 'addS' and len(command) == 5:
                        # Check that the command argument is empty
                        if (' ' in command[4]) == True and len(command[4]) == 0:
                            # Send the message 'Invalid Password'
                            self.client.send(b'Invalid Password')
                            break
                        # Check that the argument is of length 9 and matched in the p (choice)
                        if len(command[3]) == 9 and p.match(command[3]) == None:
                            self.client.send(b'Invalid StudentID')
                            break

                        index = 0
                        # Add the list of the student
                        students.append({
                            "FirstName": command[1],
                            "LastName": command[2],
                            "ID": command[3],
                            "Password": command[4]
                        })
                        # Send the message Successfully added
                        self.client.send(str.encode("Successfully added student", 'UTF-8'))
                    # If the user input the 'removeS' with an argument
                    elif command[0] == 'removeS' and len(command) == 2:
                        studentId = command[1]
                        message = ""
                        index = 0
                        found = False
                        rmv_idx = 0
                        # Loop into the student list
                        for student in students:
                            # if the student ID matched
                            if student["ID"] == studentId:
                                rmv_idx = index
                                found = True
                            index += 1
                        # Found then delete the entry
                        if found:
                            del students[rmv_idx]
                            message = "Successfully removed(" + studentId + ")"
                        # otherwise send message student not message
                        else:
                            message = "No student record found for given Student ID"
                        self.client.send(str.encode(message, 'UTF-8'))
                    # If the user input the 'removeQ' command with an argument
                    elif command[0] == 'removeQ' and len(command) == 2:
                        QuizName = command[1]
                        message = ""
                        index = 0
                        found = False
                        rmv_idx = 0
                        # Iterate into the quiz list
                        for q in quiz:
                            # Check for thr Quiz found or not
                            if q["QuizName"] == QuizName:
                                rmv_idx = index
                                found = True
                            index += 1
                        # if quiz found then delete the quiz indexes
                        # display the message  Successfully removed
                        if found:
                            del quiz[rmv_idx]
                            message = "Successfully removed( Quiz Name : " + QuizName + ")"
                        else:
                            message = "No quiz record found for given Quiz Name"
                        self.client.send(str.encode(message, 'UTF-8'))
                    # If the user input 'showGrades' with an arguments
                    elif command[0] == 'showGrades' and len(command) == 2:
                        studentId = command[1]
                        message = f"Report \n Student ID  : {studentId} \n"
                        found = False
                        # Loop into the students list
                        for student in students:
                            # Check for the student ID match
                            if student["ID"] == studentId:
                                found = True
                        # If student ID found
                        if found:
                            index = 0
                            found = False
                            # Loop into the quiz
                            for q in quiz:
                                q_name = q["QuizName"]
                                marks = q["marks"]
                                # Check for the student attended the quiz
                                if studentId in q["attends"]:
                                    index += 1
                                    m = marks[studentId]
                                    message += f"  {index} : Quiz Name: {q_name}  | marks : {m}\n"
                                    found = True
                                # otherwise if the student ID not found
                                elif q["deadLine"] < datetime.datetime.today():
                                    index += 1
                                    message += f"  {index} : Quiz Name: {q_name}  | marks : {0}\n"
                                    found = True
                            # if the quiz not found than send the message that 'No Records Found'
                            if not found:
                                message += f" No Records Found ! \n"
                        # If student ID not found then send message that the student ID not matched
                        else:
                            message = "No student record found for given Student ID"
                        self.client.send(str.encode(message, 'UTF-8'))
                    # If the client input the 'editQ' command with an argument
                    elif command[0] == 'editQ' and len(command) == 2:
                        # This part in which the user will change the questions in the database
                        found = False
                        index = 0
                        # Now iterate over the the questions of the quiz
                        for q in quiz:
                            # if the argument is in the q list
                            if command[1] == q["QuizName"]:
                                # Input the updated message
                                message = "Enter to " + command[1] + " edit mode"
                                # Show the message at the client end to enter new question
                                self.client.send(str.encode(message, 'UTF-8'))
                                # Now loop input add new questions
                                while True:
                                    # receive the questions over the client side
                                    data = self.client.recv(2048).decode()
                                    # split the input question by space
                                    cmd = data.split(' ')
                                    # If the cmds argument consist 'addQues' command without any argument
                                    if cmd[0] == 'addQues' and len(cmd) == 1:
                                        question = None
                                        answer = None
                                        # Then the message will show to input the question to change
                                        message = "[" + command[1] + " Edit mode]: Please Input Question "
                                        # Send the message above
                                        self.client.send(str.encode(message, 'UTF-8'))
                                        # loop while the client input the questions
                                        while True:
                                            question = self.client.recv(2048)
                                            # Check that the received question is not empty
                                            if len(question.decode()) > 0:
                                                # Store the user ID question
                                                currentUserID = question.decode()
                                                break
                                            # If empty then the message will snd to input the question again
                                            else:
                                                self.client.send(b'Invalid Question : Please Insert again : ')
                                        # Now send the message to input the answer
                                        message = "[" + command[
                                            1] + " Edit mode]: Please Input Answer of Question (should be T or F) "
                                        # Send the message
                                        self.client.send(str.encode(message, 'UTF-8'))
                                        # loop again to receive the answer from the client
                                        while True:
                                            answer = self.client.recv(2048)
                                            # Check that the answer if T or F
                                            if answer.decode() in ["T", "F"]:
                                                # Match the answer for the T if yes then store it
                                                answer = question.decode() == "T"
                                                break
                                            # other wise send the message that the answer is invalid
                                            else:
                                                self.client.send(
                                                    b'Invalid Answer should be T or F  : Please Insert again : ')
                                        # Store the answers in the Questions list
                                        quiz[index]["Questions"].append({
                                            "Qs": question,
                                            "Answer": answer
                                        })
                                        # Now Show the message that it is added successfully
                                        message = "[" + command[1] + " Edit mode] :Successfully added a question"
                                        self.client.send(str.encode(message, 'UTF-8'))

                                    # If the user inputs the command to remove the questions
                                    elif cmd[0] == 'removeQues' and len(cmd) == 2:
                                        numberMat = re.compile('^\\d+$')
                                        # Check the choice of the Question number is not empty
                                        if numberMat.match(cmd[1]) != None:
                                            # if the id is not zero and not greater than the question list length
                                            # remove the question from the list
                                            idx = int(cmd[1])
                                            if idx > 0 and idx <= len(quiz[index]["Questions"]):
                                                del quiz[index]["Questions"][idx - 1]
                                                self.client.send(b'Successfully removed a question')
                                            # if the question is not in the list then the message is 'Invalid Question number'
                                            else:
                                                self.client.send(b'Invalid Question number')
                                        # If all the input commands condition dont matches than the
                                        # message will be the following
                                        # 'Invalid command in quiz edit mode'
                                        else:
                                            self.client.send(b'Invalid command in quiz edit mode')

                                    elif cmd[0] == 'closeQ' and len(cmd) == 1:
                                        message = "Exiting  from " + command[1] + " edit mode"
                                        self.client.send(str.encode(message, 'UTF-8'))
                                        break
                                    else:
                                        self.client.send(b'Invalid command in quiz edit mode')

                                found = True
                                break
                            index += 1
                        if not found:
                            message = "Not Found Quiz for given name"
                            self.client.send(str.encode(message, 'UTF-8'))
                    # if the client input the command 'showGradesQ' with an argument
                    elif command[0] == 'showGradesQ' and len(command) == 2:
                        message = "Grades:  "
                        found = False
                        # Iterate over the quizzes
                        for q in quiz:
                            # If the argument is in the quiz name
                            if command[1] == q["QuizName"]:
                                # Store the Quiz name
                                quizName = q["QuizName"]
                                # add into the message
                                message += quizName + "\n"
                                # Store the points
                                points = q["points"]
                                # Store the dead line date
                                deadLine = q["deadLine"].strftime("%m-%d-%Y")
                                # Store the attending times
                                attends = q["attends"]
                                # Store the marks
                                marks = q["marks"]
                                index = 0
                                # Iterate over the students list
                                for student in students:
                                    # Increment the indexes
                                    index += 1
                                    # Store the Id
                                    id = student["ID"]
                                    # message is not attended
                                    m = "Not Attend"
                                    # if the id is in the attending people list
                                    if id in attends:
                                        # Store the message with marks
                                        m = marks[id]
                                    firstName = student["FirstName"]
                                    lastName = student["LastName"]
                                    ID = student["ID"]
                                    # Now the message is with ID , Name and Marks of the found student
                                    message += f"  {index} : {ID} : Name: {firstName} {lastName} | Marks : {m} \n"
                                found = True
                        # If the found is not found then show the message and exit
                        if not found:
                            message = "Not Found Quiz for given name"
                        # send and display the message on the client side
                        self.client.send(str.encode(message, 'UTF-8'))
                    # if the client input the command 'uploadStudentL' with an argument
                    elif command[0] == 'uploadStudentL':
                        # Send the message to upload the file
                        message = 'upload file'
                        self.client.send(str.encode(message, 'UTF-8'))
                        # Create a list for the student list received
                        Student_list = []
                        while True:
                            # Receieve the student list
                            data = self.client.recv(1024)
                            # Show the message of receiving the student list
                            print("received:", data)
                            # if the input data is Break flag then break the receiving session
                            if data == b'Break':
                                break
                            # append the list of the student with the current students list after decoding
                            Student_list.append(data.decode('utf-8'))
                        # Extract all the students and append it with the data
                        for row in Student_list[1:]:
                            student = {
                                "FirstName": row.split(',')[0],
                                "LastName": row.split(',')[1],
                                "ID": row.split(',')[2],
                                "Password": row.split(',')[3][:-1]
                            }
                            # Appending the student list
                            students.append(student)
                    # If the user input the uploadQuizC with a parameter of the Quiz number
                    elif command[0] == 'uploadQuizC' and len(command) == 2:
                        # This condition will run for the command with Quiz01 parameter
                        if command[1] == 'Quiz01':
                            # Send the message to upload the file
                            message = 'upload quiz'
                            self.client.send(str.encode(message, 'UTF-8'))

                            # Create a list for the student list received
                            Questions_list = []
                            while True:
                                # Receieve the student list
                                data = self.client.recv(1024)
                                # Show the message of receiving the student list
                                print("received:", data)
                                # if the input data is Break flag then break the receiving session
                                if data == b'Break':
                                    break
                                # append the list of the student with the current students list after decoding
                                Questions_list.append(data.decode('utf-8'))

                            for i in range(len(quiz)):
                                if quiz[i]['QuizName'] == "Quiz01":
                                    for q in Questions_list[1:]:
                                        question = {
                                            'Qs': q.split(',')[0],
                                            'Answer': q.split(',')[1][:-1]
                                        }
                                        quiz[i]['Questions'].append(question)
                        # This condition will run for the command with Quiz02 parameter
                        elif command[1] == 'Quiz02':
                            # Send the message to upload the file
                            message = 'upload quiz'
                            self.client.send(str.encode(message, 'UTF-8'))

                            # Create a list for the student list received
                            Questions_list = []
                            while True:
                                # Receieve the student list
                                data = self.client.recv(1024)
                                # Show the message of receiving the student list
                                print("received:", data)
                                # if the input data is Break flag then break the receiving session
                                if data == b'Break':
                                    break
                                # append the list of the student with the current students list after decoding
                                Questions_list.append(data.decode('utf-8'))

                            for i in range(len(quiz)):
                                if quiz[i]['QuizName'] == "Quiz02":
                                    for q in Questions_list[1:]:
                                        question = {
                                            'Qs': q.split(',')[0],
                                            'Answer': q.split(',')[1][:-1]
                                        }
                                        quiz[i]['Questions'].append(question)
                        # This condition will run for the command with Quiz03 parameter
                        elif command[1] == 'Quiz03':
                            # Send the message to upload the file
                            message = 'upload quiz'
                            self.client.send(str.encode(message, 'UTF-8'))

                            # Create a list for the student list received
                            Questions_list = []
                            while True:
                                # Receieve the student list
                                data = self.client.recv(1024)
                                # Show the message of receiving the student list
                                print("received:", data)
                                # if the input data is Break flag then break the receiving session
                                if data == b'Break':
                                    break
                                # append the list of the student with the current students list after decoding
                                Questions_list.append(data.decode('utf-8'))

                            for i in range(len(quiz)):
                                if quiz[i]['QuizName'] == "Quiz03":
                                    for q in Questions_list[1:]:
                                        question = {
                                            'Qs': q.split(',')[0],
                                            'Answer': q.split(',')[1][:-1]
                                        }
                                        quiz[i]['Questions'].append(question)
                    # if the command user inputted is exit then we will initiate the exit function on the client side
                    # and stop the loop and close the socket
                    elif command[0] == 'exit' and len(command) == 1:
                        self.client.send(b'exit')
                        self.client.close()
                        print("[-] Server socket thread ended for " + self.ip + ":" + str(self.port))
                        sys.exit(-1)
                    elif command[0] == 'exitI':
                        print("Instructor loop broken")
                        break
                    else:
                        self.client.send(b'Invalid Command')


# Here we start all the server side
# session to request and response between client and the server
threads = []

# Starting the server side socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    while True:
        # wait while the client online
        s.listen()
        # began to accept data from the client
        client, (ip, port) = s.accept()
        # Start the session on the thread for the server side data receiving
        newthread = ClientThread(ip, port, client)
        newthread.start()
        # append all the threads that are working
        threads.append(newthread)

# After done work done stop the thread by joining it with main process
for t in threads:
    t.join()

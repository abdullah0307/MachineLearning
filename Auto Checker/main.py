import datetime
import time
from threading import Thread

import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox

from google.oauth2 import service_account
from googleapiclient.discovery import build

import pandas as pd
from PyQt5 import QtWidgets

from GUI import Ui_MainWindow
from Register import Ui_Dialog
import Warning


class Main:
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        SERVICE_ACCOUNT_FILE = 'Credentials/key.json'
        self.SAMPLE_SPREADSHEET_ID = '12K5HXe45CXiMnRz7Yz8fFA77VHe9w-4fnSXuV-K3tc4'
        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        self.sheet = service.spreadsheets()

        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        self.Register = QtWidgets.QMainWindow()
        self.register_obj = Ui_Dialog()
        self.register_obj.setupUi(self.Register)
        self.Register.setWindowFlag(Qt.FramelessWindowHint)
        self.register_obj.pushButton.clicked.connect(self.Register_clicked)

        self.warning = QtWidgets.QDialog()
        self.warning_obj = Warning.Ui_Dialog()
        self.warning_obj.setupUi(self.warning)
        self.warning.setWindowFlag(Qt.FramelessWindowHint)
        self.warning_obj.pushButton.clicked.connect(lambda: self.warning.close())

        self.ui.stackedWidget.setCurrentWidget(self.ui.page)
        self.ui.pushButton_2.clicked.connect(self.teacher_sign_in)
        self.ui.pushButton.clicked.connect(self.student_sign_in)

        self.ui.pushButton_3.clicked.connect(self.open_menu)
        self.ui.pushButton_11.clicked.connect(self.logout)
        self.ui.pushButton_12.clicked.connect(self.logout)

        self.ui.pushButton_13.clicked.connect(self.create_quiz_option)
        self.ui.pushButton_5.clicked.connect(self.start_create_quiz)

        self.ui.pushButton_6.clicked.connect(self.update_MCQS_preview)
        self.ui.pushButton_6.clicked.connect(self.add_option)
        self.ui.pushButton_7.clicked.connect(self.delete_option)
        self.ui.pushButton_8.clicked.connect(self.next_MCQS)
        self.ui.pushButton_14.clicked.connect(self.show_report)

        self.ui.textEdit_2.textChanged.connect(self.update_MCQS_preview)
        self.ui.comboBox.currentTextChanged.connect(self.update_MCQS_preview)

        self.ui.pushButton_16.clicked.connect(self.add_correct_option)
        self.ui.pushButton_17.clicked.connect(self.add_question)
        self.ui.pushButton_9.clicked.connect(self.open_quiz)

        self.ui.listWidget.itemClicked.connect(self.quiz_list_item_clicked)

        self.ui.pushButton_15.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_7))
        self.ui.pushButton_18.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_7))
        self.ui.pushButton_17.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page))
        self.ui.pushButton_21.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page))
        self.ui.pushButton_23.clicked.connect(self.upload_image_to_text)
        self.ui.pushButton_4.clicked.connect(self.Next_question)
        self.ui.pushButton_19.clicked.connect(self.start_quiz)
        self.ui.pushButton_20.clicked.connect(self.Next_MCQs)
        self.ui.pushButton_22.clicked.connect(self.signUp)

        self.total_MCQs = 0
        self.total_Questions = 0

        self.total_test_marks = 0
        self.total_obtained_marks = 0

        self.test_question_no = 0
        self.test_MCQs_no = 0

        self.answers = []

        self.current_user = None
        self.user_name = None

    def upload_image_to_text(self):
        # open the dialogue box to select the file
        options = QtWidgets.QFileDialog.Options()

        # open the Dialogue box to get the images paths
        image_path = QtWidgets.QFileDialog.getOpenFileName(caption="Select the images of the Answer", directory="",
                                                           filter="jpg images (*.jpg);;png images (*.png);;jpeg images ("
                                                                  "*.jpeg);;All files(*.*)",
                                                           options=options)
        image = cv2.imread(image_path[0])
        text = pytesseract.image_to_string(image)
        self.ui.textEdit.setText(self.ui.textEdit.toPlainText() + text)

    def Register_clicked(self):
        if self.register_obj.lineEdit_2.text() != self.register_obj.lineEdit_3.text() or self.register_obj.lineEdit_4.text() == "":
            self.warning_obj.label_2.setText("Something Wrong")
            self.warning.show()
            return

        result = self.sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, range="Users!A1:Z1000").execute()
        point = len(result.get('values')[1:]) + 1

        row = [self.register_obj.lineEdit_4.text(), self.register_obj.lineEdit_2.text(), self.current_user]
        self.sheet.values().update(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, range="Users!A" + str(point + 1),
                                   valueInputOption="USER_ENTERED", body={"values": [row]}).execute()

    def signUp(self):
        if self.current_user == "Student":
            self.register_obj.comboBox.setCurrentIndex(0)
        elif self.current_user == "Teacher":
            self.register_obj.comboBox.setCurrentIndex(1)
        self.Register.show()

    def Next_MCQs(self):
        result = self.sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, range="MCQs!A1:Z1000").execute()
        test_data = pd.DataFrame(result.get("values")[1:], columns=result.get("values")[0])
        correct_answer = test_data["correct option"].values[self.test_MCQs_no]

        if correct_answer == self.ui.comboBox_2.currentText():
            self.total_obtained_marks += 1

        self.test_MCQs_no += 1

        self.ui.label_39.setText("Question: " + str(self.test_MCQs_no + 1))
        self.ui.textEdit_5.setText(test_data["Question"].values[self.test_MCQs_no])

        options = []
        for op in ["option1", "option2", "option3", "option4", "option5"]:
            if test_data[op].values[0] != "NAN":
                options.append(test_data[op].values[self.test_MCQs_no])
        self.ui.comboBox_2.clear()
        self.ui.comboBox_2.addItems(options)

        if (self.test_MCQs_no + 1) >= len(test_data["Question"].values):
            result = self.sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID,range="Questions!A1:Z1000").execute()
            test_data = pd.DataFrame(result.get("values")[1:], columns=result.get("values")[0])
            self.total_test_marks += (len(test_data["Question"].values) * 10)

            result = self.sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, range="MCQs!A1:Z1000").execute()
            test_data = pd.DataFrame(result.get("values")[1:], columns=result.get("values")[0])
            self.total_test_marks += (len(test_data["Question"].values) * 1)

            result = self.sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID,
                                             range="Results!A1:Z1000").execute()
            point = len(result.get('values')[1:]) + 1

            row = [self.ui.lineEdit.text(), self.ui.label_28.text(), self.total_test_marks, self.total_obtained_marks,
                   str(datetime.date.today())]
            self.sheet.values().update(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, range="Results!A" + str(point + 1),
                                       valueInputOption="USER_ENTERED", body={"values": [row]}).execute()

            self.ui.stackedWidget.setCurrentWidget(self.ui.page_6)

    def text_match(self, to_compare, target):
        ok_count = 0
        total_count = len(target.split())
        for i in to_compare.split():
            if i in target.split():
                ok_count += 1
        return round((ok_count / total_count) * 10, 2)

    def Next_question(self):
        result = self.sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, range="Questions!A1:Z1000").execute()
        test_data = pd.DataFrame(result.get("values")[1:], columns=result.get("values")[0])
        test_data = test_data[test_data["Quiz"] == self.ui.label_28.text().split(':')[1]]
        correct_answer = test_data["Answer"].values[self.test_question_no]
        submitted_answer = self.ui.textEdit.toPlainText()
        obtained_mark = self.text_match(submitted_answer, correct_answer)

        self.total_obtained_marks += obtained_mark

        # Increment to next index
        self.test_question_no += 1

        self.ui.label_7.setText(test_data["Question"].values[self.test_question_no])
        self.ui.label_6.setText("Question: " + str(self.test_question_no + 1))

        if (self.test_question_no + 1) >= len(test_data["Question"].values):
            result = self.sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, range="MCQs!A1:Z1000").execute()
            test_data = pd.DataFrame(result.get("values")[1:], columns=result.get("values")[0])
            self.ui.label_39.setText("Question: " + str(self.test_MCQs_no + 1))
            self.ui.textEdit_5.setText(test_data["Question"].values[0])
            options = []
            for op in ["option1", "option2", "option3", "option4", "option5"]:
                if test_data[op].values[0] != "NAN":
                    options.append(test_data[op].values[0])
            self.ui.comboBox_2.addItems(options)
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_11)

    def start_test_time(self):
        t = 1800
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            self.ui.label_38.setText(timer)
            self.ui.label_34.setText(timer)
            time.sleep(1)
            t -= 1
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_6)

    def start_quiz(self):
        if self.ui.label_30.text().split(":")[1] != "Yes":
            self.warning_obj.label_2.setText("Something Wrong")
            self.warning.show()
            return

        self.ui.label_5.setText("Quiz:" + self.ui.listWidget.selectedItems()[0].text())
        self.ui.label_6.setText("Question:" + str(self.test_question_no + 1))
        result = self.sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, range="Questions!A1:Z1000").execute()
        test_data = pd.DataFrame(result.get("values")[1:], columns=result.get("values")[0])
        self.ui.label_7.setText(test_data["Question"].values[0])

        self.ui.stackedWidget.setCurrentWidget(self.ui.page_3)
        t = Thread(target=self.start_test_time)
        t.start()

    def quiz_list_item_clicked(self):
        quiz = self.ui.listWidget.selectedItems()[0].text()
        result = self.sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, range="Quiz_list!A1:Z1000").execute()

        quizs = pd.DataFrame(result.get('values')[1:], columns=result.get('values')[0])
        date = quizs[quizs["Quiz_Name"] == quiz]["Quiz_Date"].values[0]
        total_mcqs = quizs[quizs["Quiz_Name"] == quiz]["Total_MCQs"].values[0]
        total_questions = quizs[quizs["Quiz_Name"] == quiz]["Total_Questions"].values[0]

        self.ui.label_28.setText("Quiz Name:" + quiz)
        self.ui.label_29.setText("Quiz Data:" + date)
        self.ui.label_31.setText("Total MCQs:" + total_mcqs)
        self.ui.label_32.setText("Total Questions:" + total_questions)

        today = datetime.date.today()
        test = datetime.date(int(date.split("/")[0]), int(date.split("/")[1]), int(date.split("/")[2]))

        if today == test:
            self.ui.label_30.setText("Quiz Available:Yes")
        else:
            self.ui.label_30.setText("Quiz Available:No")

    def open_quiz(self):
        result = self.sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, range="Quiz_list!A1:Z100").execute()
        quizlist = pd.DataFrame(result.get('values')[1:], columns=result.get('values')[0])
        self.ui.listWidget.addItems(quizlist["Quiz_Name"].values)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_10)

    def show_report(self):
        result = self.sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, range="Results!A1:Z1000").execute()
        self.ui.tableWidget.setRowCount(0)
        for row, rd in enumerate(result.get("values")):
            self.ui.tableWidget.insertRow(row)
            for col, data in enumerate(rd):
                self.ui.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(str(data)))

        self.ui.stackedWidget.setCurrentWidget(self.ui.page_9)

    def add_correct_option(self):
        self.ui.label_22.setText("Correct option:" + self.ui.comboBox.currentText())

    def update_MCQS_preview(self):
        updated_text = ""
        updated_text = updated_text + self.ui.textEdit_2.toPlainText()
        options = [self.ui.comboBox.itemText(i) for i in range(self.ui.comboBox.count())]
        for n, op in enumerate(options):
            updated_text = updated_text + "\n" + str(n + 1) + ") " + op
        self.ui.textBrowser.setText(updated_text)

    def next_MCQS(self):
        question = self.ui.textEdit_2.toPlainText()
        options = [self.ui.comboBox.itemText(i) for i in range(self.ui.comboBox.count())]
        if question == "" or len(options) == 0 or self.ui.label_22.text().split(":")[1] == "":
            self.warning_obj.label_2.setText("Add full question and answer")
            self.warning.show()
            return

        # Get the length of the Questions
        result = self.sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, range="MCQs!A1:Z1000").execute()
        point = len(result.get('values')[1:]) + 1

        # Upload the MCQs to the server
        options.insert(0, question)
        options.insert(1, self.ui.lineEdit_4.text())
        options.insert(2, self.ui.label_22.text().split(":")[1])
        if len(options) != 8:
            diff = 8 - len(options)
            for _ in range(diff):
                options.append("NAN")
        self.sheet.values().update(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, range="MCQs!A" + str(point + 1),
                                   valueInputOption="USER_ENTERED", body={"values": [options]}).execute()
        # Reset every thing
        self.ui.textBrowser.setText("")
        self.ui.textEdit_2.setText("")
        self.ui.lineEdit_3.setText("")
        self.ui.comboBox.clear()
        self.ui.label_22.setText("Correct option")
        self.ui.label_14.setText("Question:")

        # Add Question counter
        self.total_MCQs += 1
        self.ui.label_14.setText("MCQs # " + str(self.total_MCQs + 1))

        if self.total_MCQs == int(self.ui.spinBox_2.text()):
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_8)
            self.ui.label_25.setText("Question:" + str(self.total_Questions + 1))

    def add_question(self):
        # Show warning if something is missing
        if self.ui.textEdit_4.toPlainText() == "" or self.ui.textEdit_3.toPlainText() == "":
            self.warning_obj.label_2.setText("Some fields are empty...")
            self.warning.show()
            return

        # Question and answer row
        row = [self.ui.textEdit_4.toPlainText(), self.ui.textEdit_3.toPlainText(), self.ui.lineEdit_4.text()]

        # Get the length of the Questions
        result = self.sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, range="Questions!A1:G1000").execute()
        point = len(result.get('values', [])[1:]) + 1

        # update into the server
        self.sheet.values().update(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, range="Questions!A" + str(point + 1),
                                   valueInputOption="USER_ENTERED", body={"values": [row]}).execute()
        self.total_Questions += 1
        self.ui.label_25.setText("Question:" + str(self.total_Questions + 1))
        self.ui.textEdit_3.setText("")
        self.ui.textEdit_4.setText("")

        if self.total_Questions == int(self.ui.spinBox_3.text()):
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_7)

    def add_option(self):
        question = self.ui.textEdit_2.toPlainText()

        if question == "":
            self.warning_obj.label_2.setText("Please enter a question")
            self.warning.show()
            return

        option = self.ui.lineEdit_3.text()
        self.ui.lineEdit_3.setText("")
        self.ui.comboBox.addItem(option)

    def delete_option(self):
        target = self.ui.comboBox.currentIndex()
        self.ui.comboBox.removeItem(target)

    def start_create_quiz(self):
        if self.ui.lineEdit_4.text() == "" or self.ui.spinBox_2.text() == "0" or self.ui.spinBox_3.text() == "0":
            self.warning_obj.label_2.setText("Invalid credentials..")
            self.warning.show()
            return
        quiz_name = self.ui.lineEdit_4.text()
        quiz_date = self.ui.calendarWidget.selectedDate().getDate()
        date = str(quiz_date[0]) + "-" + str(quiz_date[1]) + "-" + str(quiz_date[2])
        total_mcqs = int(self.ui.spinBox_2.text())
        total_question = int(self.ui.spinBox_3.text())

        row = [quiz_name, date, total_mcqs, total_question]

        # Get the length of the Questions
        result = self.sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, range="Quiz_list!A1:G1000").execute()
        point = len(result.get('values', [])[1:]) + 1

        # Upload the MCQs to the server
        self.sheet.values().update(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, range="Quiz_list!A" + str(point + 1),
                                   valueInputOption="USER_ENTERED", body={"values": [row]}).execute()

        self.ui.label_14.setText("MCQs # " + str(self.total_MCQs + 1))
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_5)

    def create_quiz_option(self):
        self.ui.label_12.setText("Teacher: " + self.user_name)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_4)

    def logout(self):
        self.ui.lineEdit.setText("")
        self.ui.lineEdit_2.setText("")
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)

    def open_menu(self):
        # if the input data is empty
        if self.ui.lineEdit.text() == "" or self.ui.lineEdit_2.text() == "":
            self.warning_obj.label_2.setText("Invalid credentials..")
            self.warning.show()
            return

        result = self.sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID, range="Users!A1:C100").execute()
        All_Users = pd.DataFrame(result.get('values', [])[1:], columns=result.get('values', [])[0])
        user_id = self.ui.lineEdit.text()
        user_password = self.ui.lineEdit_2.text()

        if list(All_Users[All_Users["Name"] == user_id]["Name"].values) != []:
            self.user_name = All_Users[All_Users["Name"] == user_id]["Name"].values[0]
            if All_Users[All_Users["Name"] == user_id]["Password"].values[0] == user_password and \
                    All_Users[All_Users["Name"] == user_id]["Role"].values[0] == self.current_user:
                if self.current_user == "Teacher":
                    self.ui.stackedWidget.setCurrentWidget(self.ui.page_7)
                elif self.current_user == "Student":
                    self.ui.stackedWidget.setCurrentWidget(self.ui.page_6)
            else:
                self.warning_obj.label_2.setText("Invalid credentials..")
                self.warning.show()
        else:
            self.warning_obj.label_2.setText("Invalid credentials..")
            self.warning.show()

    def student_sign_in(self):
        self.current_user = "Student"
        self.ui.label_4.setText("Student Login")
        self.ui.label_2.setText("Student ID")
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)

    def teacher_sign_in(self):
        self.current_user = "Teacher"
        self.ui.label_4.setText("Teacher Login")
        self.ui.label_2.setText("Teacher ID")
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    main.MainWindow.show()
    sys.exit(app.exec_())

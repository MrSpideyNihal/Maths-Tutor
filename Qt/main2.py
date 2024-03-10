import sys
import time
import threading
import math
import random
import re
import os
from PyQt5 import QtWidgets, QtGui, QtCore
import pyttsx3

engine = pyttsx3.init()

class MathsTutorWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Maths-Tutor")
        self.setGeometry(100, 100, 800, 600)

        # Create central widget
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        vbox = QtWidgets.QVBoxLayout(central_widget)
        vbox.setContentsMargins(10, 10, 10, 10)

        vbox2 = QtWidgets.QVBoxLayout()
        self.data_directory = "images"
        # Create a label
        self.label = QtWidgets.QLabel()
        self.label.setText("Welcome to maths tutor!\nPress enter to start ")
        font = QtGui.QFont()
        font.setPointSize(40)
        self.label.setFont(font)
        


        # Set text color and background color
        font_color = QtGui.QColor("#0603f0")
        background_color = QtGui.QColor("#ffffff")
        self.label.setStyleSheet("color: {}; background-color: {}".format(font_color.name(), background_color.name()))

        vbox2.addWidget(self.label)

        hbox = QtWidgets.QHBoxLayout()
        hbox2 = QtWidgets.QHBoxLayout()

        self.entry = QtWidgets.QLineEdit()
        self.entry.returnPressed.connect(self.on_entry_activated)
        hbox.addWidget(self.entry)

        #buttonsss
        
        Load_Questions_button = QtWidgets.QPushButton("Load Questions")
        Load_Questions_button.clicked.connect(self.on_Load_Questions_clicked)
        hbox.addWidget(Load_Questions_button)

        hbox2.addWidget(QtWidgets.QPushButton("User-Guide"))
        about_button = QtWidgets.QPushButton("About")
        about_button.clicked.connect(self.show_about_dialog)
        hbox2.addWidget(about_button)
        Close_button = QtWidgets.QPushButton("Quit")
        Close_button.clicked.connect(self.close)
        hbox2.addWidget(Close_button)

        vbox.addLayout(vbox2)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)

        self.current_question_index = -1
        self.wrong = False
        self.excellent = 0
        self.final_score = 0
        self.incorrect_answer_count = 0

        self.load_question_file("data.txt")
        self.set_image("welcome",3)

    def set_image(self, name, rand_range):
        
        # Create a QLabel widget to display the image
        image_label = QtWidgets.QLabel(self)
        
        # Construct the file path
        file_path = os.path.join("images", f"{name}-{rand_range}.gif")
        
        # Check if the file exists
        if os.path.exists(file_path):
            # Load the imagesssssss
            pixmap = QtGui.QPixmap(file_path)
            image_label.setPixmap(pixmap)
            image_label.setGeometry(150, 50, 300, 300)
            image_label.setAlignment(QtCore.Qt.AlignCenter)
            image_label.show()
        else:
            print("Image file not found:", file_path)
    def speak(self, text, enqueue=False):
        if not enqueue:
            if engine._inLoop:
                engine.stop()
            else:
                engine.startLoop(False)
        
        if isinstance(text, list):
            for item in text:
                engine.say(item)
                engine.iterate()
        else:
            engine.say(text)
    
        if not enqueue:
            if not engine._inLoop:
                engine.runAndWait()
    
        
  #To load question you have to press enter      
        
    def load_question_file(self, file_path):
        self.list = []
        self.current_question_index = -1
        self.wrong = False
        with open(file_path, "r") as file:
            for line in file:
                stripped_line = line.strip()
                self.list.append(stripped_line)

    def on_entry_activated(self):
        if self.current_question_index == -1:
            self.starting_time = time.time();
            self.wrong = False
            self.excellent = 0
            self.final_score = 0
            self.incorrect_answer_count = 0
            self.next_question()
        else:
            answer = self.entry.text()
            correct_answer = self.answer

            if answer == correct_answer:
                time_end = time.time()
                time_taken = time_end - self.time_start
                time_alotted = int(self.list[self.current_question_index].split("===")[2])
                self.incorrect_answer_count = 0
                print(time_taken)
                if time_taken < time_alotted:
                    self.excellent = self.excellent + 3
                    self.final_score = self.final_score + 5
                    self.speak("Excellent!")
                    self.label.setText("Excellent!")
                    self.set_image("excellent", 3)
                elif time_taken < time_alotted + 2:
                    self.excellent = self.excellent + 2
                    self.final_score = self.final_score + 4
                    self.speak("Very good!")
                    self.label.setText("Very good!")
                    self.set_image("very-good", 3)
                elif time_taken < time_alotted + 4:
                    self.final_score = self.final_score + 3
                    self.speak("Good!")
                    self.label.setText("Good!")
                    self.set_image("good", 3)
                elif time_taken < time_alotted + 6:
                    self.excellent = 0
                    self.final_score = self.final_score + 2
                    self.speak("Not bad!")
                    self.label.setText("Not bad!")
                    self.set_image("not-bad", 3)

                else:
                    self.excellent = -1
                    self.final_score = self.final_score + 1
                    self.speak("Okay!")
                    self.label.setText("Okay!")
                    self.set_image("okay", 3)

            else:
                self.wrong = True
                self.final_score = self.final_score - 1
                self.incorrect_answer_count = self.incorrect_answer_count + 1
                if self.incorrect_answer_count == 3:
                    self.set_image("wrong-anwser-repeted", 2)
                    self.incorrect_answer_count = 0
                    text = "Sorry! the correct answer is "
                    self.label.setText(text + self.answer)
                    if len(self.answer.split(".")) > 1:
                        li = list(self.answer.split(".")[1])
                        self.speak(text + self.answer.split(".")[0] + " point " + " ".join(li))
                    else:
                        self.speak(text + self.answer)

                else:
                    self.label.setText("Sorry! let's try again")
                    self.speak("Sorry! let's try again")
                    self.set_image("wrong-anwser", 3)
            QtCore.QTimer.singleShot(300, self.next_question)#speed of pausing
            self.entry.clear()

    def next_question(self):
        self.time_start = time.time()
        self.entry.setFocus()
        if self.wrong:
            self.label.setText(self.question)
            threading.Thread(target=self.announce_question, args=[self.question, self.make_sound, self.current_question_index]).start()
            self.set_image("wrong-anwser", 3)
            self.wrong = False
        else:
            if self.excellent >= 3:
                self.current_question_index = self.current_question_index + self.excellent
            else:
                self.current_question_index = self.current_question_index + 1
            if self.current_question_index < len(self.list) - 1:
                if "?" in self.list[self.current_question_index]:
                    question_to_pass = self.list[self.current_question_index].split("===")[0]
                    self.question = self.question_parser(question_to_pass)
                    number = eval(self.question)
                    if number == math.trunc(number):
                        self.answer = str(math.trunc(number))
                    else:
                        num = round(eval(str(number)), 2)
                        self.answer = str(num)
                else:
                    self.question = self.list[self.current_question_index].split("===")[0]
                    self.answer = self.list[self.current_question_index].split("===")[1]

                self.make_sound = self.list[self.current_question_index].split("===")[3]
                self.label.setText(self.question)
                threading.Thread(target=self.announce_question, args=[self.question, self.make_sound, self.current_question_index]).start()

                self.entry.clear()
            else:
                minute, seconds = divmod(round(time.time() - self.starting_time), 60)
                text = "Successfully finished! Your score is " + str(self.final_score) + \
                       "!\nTime taken " + str(minute) + " minutes and " + str(seconds) + " seconds!" + \
                       "\nPress enter to start again."
                self.speak(text)
                self.label.setText(text)
                self.set_image("finished", 3)
                self.current_question_index = -1
 
    def announce_question(self, question, make_sound, announcing_question_index):
        if make_sound == '1':
            item_list = re.split(r'(\d+)', question)[1:-1]
            for item in item_list:
                if announcing_question_index != self.current_question_index:
                    return
                if item.isnumeric():
                    self.speak(item_list)
                    time.sleep(0.7)
                else:
                    self.speak(self.convert_signs(item))
                    time.sleep(0.7)
                self.speak("equals to?")
        else:
            self.speak("question")
            time.sleep(0.7)
            self.speak(self.convert_signs(self.question) + " equals to ? ")


    def on_destroy(self):
        print("CLOSE")

    def show_about_dialog(self):
        about_dialog = QtWidgets.QMessageBox()
        about_dialog.setText(
            "MATHS TUTOR GAME\n 0.1 \n\nMATHS TUTOR is a game to develop students calculation ability in maths and to judge themselves.\n Which is helpful to the students who have basic knowledge in maths. \n They  want to answer the questions they got and can lead into progress if they can answer the questions correctly.  \n\n   Copyright(C) 2022-2023 ROOPASREE A P <roopasreeap@gmail.com>\n\n   Supervised by  Zendalona(2022-2023)\n\n This program is free software you can redistribute it and or modify \nit under the terms of GNU General Public License as published by the free software foundation \n either gpl3 of the license.This program is distributed in the hope that it will be useful,\n but without any warranty without even the implied warranty of merchantability or fitness for a particular purpose.\n see the GNU General Public License for more details")
        about_dialog.setWindowTitle("About")
        about_dialog.exec_()

    def on_Load_Questions_clicked(self, file_name):
        self.list = []
        self.current_question_index = -1
        self.wrong = False
        file_path = os.path.join(os.path.dirname(__file__), "loaddata.txt")
        with open(file_path, "r") as file:
            for line in file:
                stripped_line = line.strip()
                self.list.append(stripped_line)

    def question_parser(self, question):
        first = True
        second = False
        digit_one = ""
        digit_two = ""
        output = ""
        for i in range(0, len(question)):
            item = question[i]

            if item.isdigit():
                if second == False:
                    digit_one = digit_one + item
                else:
                    digit_two = digit_two + item
            elif item == ",":
                second = True
            else:
                second = False
                if digit_two != "":
                    output = output + self.get_randome_number(digit_one, digit_two)
                else:
                    output = output + digit_one
                output = output + item

                digit_one = ""
                digit_two = ""

            if i == len(question) - 1:
                if digit_one != "":
                    if digit_two != "":
                        output = output + self.get_randome_number(digit_one, digit_two)
                    else:
                        output = output + digit_one
        return output;

    def get_randome_number(self, value1, value2):
        if int(value1) < int(value2):
            return str(random.randint(int(value1), int(value2)))
        else:
            return str(random.randint(int(value2), int(value1)))

    def convert_signs(self, text):
        return text.replace("+", " plus ").replace("-", " minus ").replace("*", " multiply ").replace("/", " divided by ")

    def closeEvent(self, event):
        self.on_destroy()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MathsTutorWindow()
    win.show()
    sys.exit(app.exec_())

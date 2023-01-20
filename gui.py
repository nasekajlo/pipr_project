from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PyQt6.QtWidgets import QMessageBox, QLineEdit, QLabel
from PyQt6.QtWidgets import QWidget, QPushButton
from PyQt6 import QtCore
from design import Ui_MainWindow
from class_fiszki import *
import time
import sys
database = 'words_for_repeat.txt'
words_for_repeat = 'words_for_repeat.txt'
x_word = 40
y_word = 60
x_translate = 170
y_translate = 60
sorted_translate = []
sorted_words = []
current_number_word = 0
current_number_translate = 0
cards = []
timee = 0

class FiszkiWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.buttonStart.clicked.connect(self._turn_page)
        self.ui.btOk.clicked.connect(self._set_time_number)
        self.ui.word_1.clicked.connect(lambda: self._change_location(self.ui.word_1))
        self.ui.word_2.clicked.connect(lambda: self._change_location(self.ui.word_2))
        self.ui.word_3.clicked.connect(lambda: self._change_location(self.ui.word_3))
        self.ui.word_4.clicked.connect(lambda: self._change_location(self.ui.word_4))
        self.ui.word_5.clicked.connect(lambda: self._change_location(self.ui.word_5))
        self.ui.word_6.clicked.connect(lambda: self._change_location(self.ui.word_6))
        self.ui.word_7.clicked.connect(lambda: self._change_location(self.ui.word_7))
        self.ui.word_8.clicked.connect(lambda: self._change_location(self.ui.word_8))
        self.ui.word_9.clicked.connect(lambda: self._change_location(self.ui.word_9))
        self.ui.word_10.clicked.connect(lambda: self._change_location(self.ui.word_10))
        self.ui.translate_1.clicked.connect(lambda: self._change_location_translate(self.ui.translate_1))
        self.ui.translate_2.clicked.connect(lambda: self._change_location_translate(self.ui.translate_2))
        self.ui.translate_3.clicked.connect(lambda: self._change_location_translate(self.ui.translate_3))
        self.ui.translate_4.clicked.connect(lambda: self._change_location_translate(self.ui.translate_4))
        self.ui.translate_5.clicked.connect(lambda: self._change_location_translate(self.ui.translate_5))
        self.ui.translate_6.clicked.connect(lambda: self._change_location_translate(self.ui.translate_6))
        self.ui.translate_7.clicked.connect(lambda: self._change_location_translate(self.ui.translate_7))
        self.ui.translate_8.clicked.connect(lambda: self._change_location_translate(self.ui.translate_8))
        self.ui.translate_9.clicked.connect(lambda: self._change_location_translate(self.ui.translate_9))
        self.ui.translate_10.clicked.connect(lambda: self._change_location_translate(self.ui.translate_10))
        self.ui.import_card.clicked.connect(self.import_new_card)
        self.ui.define_card.clicked.connect(self.define_new_card)
        self.ui.check.clicked.connect(self.check_result)

    def define_new_card(self):
        word = self.ui.new_word.text()
        translate = self.ui.new_translate.text()
        if round.number_of_cards != 10:
            if word != '' or translate != '':
                card = Card(word, translate, 2)
                try:
                    round.export_card(card)
                    dialog = QMessageBox()
                    dialog.setWindowTitle("Succes!")
                    dialog.setIcon(QMessageBox.Icon.NoIcon)
                    dialog.setText("Now in our database we have new word!")
                    dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
                    dialog.exec()
                except:
                    dialog = QMessageBox()
                    dialog.setWindowTitle("Faile((!")
                    dialog.setIcon(QMessageBox.Icon.NoIcon)
                    dialog.setText("Now in our database we have this word yet(!")
                    dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
                    dialog.exec()
            else:
                dialog = QMessageBox()
                dialog.setWindowTitle("Invalid data")
                dialog.setIcon(QMessageBox.Icon.Warning)
                dialog.setText("Please, enter the word and its translate")
                dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
                dialog.exec()
        else:
            dialog = QMessageBox()
            dialog.setWindowTitle("Too much cards")
            dialog.setIcon(QMessageBox.Icon.Warning)
            dialog.setText("Consider the maximum value of time and cards number")
            dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
            dialog.exec()
        self.ui.new_word.setText("")
        self.ui.new_translate.setText("")

    def import_new_card(self):
        if round.number_of_cards != 10:
            global cards
            cards = round.import_card(cards)
            word_label = self.ui.page_3.findChild(QPushButton, f'word_{len(cards)}')
            word_label.setText(cards[len(cards)-1].word)
            translate_label = self.ui.page_3.findChild(QPushButton, f'translate_{len(cards)}')
            translate_label.setText(cards[len(cards)-1].translate)
            word_label.setStyleSheet("QPushButton{\n"
"background-color: rgb(252, 250, 250);\n"
"font: 20px \"Century Gothic\";\n"
"font-weight: bold;\n"
"color:rgb(37, 68, 65);\n"
"border-radius:10px;\n"
"padding-left:5px;\n"
"padding-right:5px;\n"
"}\n")
            word_label.resize(130,50)
            translate_label.setStyleSheet("QPushButton{\n"
"background-color: rgb(112, 86, 109);\n"
"font: 20px \"Century Gothic\";\n"
"font-weight: bold;\n"
"color:rgb(252, 250, 250);\n"
"border-radius:10px;\n"
"padding-left:5px;\n"
"padding-right:5px;\n"
"}\n")
            translate_label.resize(130,50)
            word_label.setEnabled(True)
            translate_label.setEnabled(True)
            round.number_of_cards = round.number_of_cards + 1
        else:
            dialog = QMessageBox()
            dialog.setWindowTitle("Invalid time")
            dialog.setIcon(QMessageBox.Icon.Warning)
            dialog.setText("Consider the maximum value of time and cards number")
            dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
            dialog.exec()


    def check_result(self):
        global timee
        timee = time.perf_counter() - timee
        result_cards = []
        for card in cards:
            for word in sorted_words:
                if card.word == word:
                    result_cards.append(card)
        bad_words = round.check_result(result_cards, sorted_translate, timee)
        all_words = round.words_for_repeat(result_cards)
        # print(result_cards[0].word)
        # print(all_words[2].repeat)
        if bad_words == []:
            dialog = QMessageBox()
            dialog.setWindowTitle("GOOD JOB")
            dialog.setIcon(QMessageBox.Icon.NoIcon)
            dialog.setText("You answer is correct")
            dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        else:
            dialog = QMessageBox()
            dialog.setWindowTitle("Pitty")
            dialog.setIcon(QMessageBox.Icon.NoIcon)
            dialog.setText("It is a pitty, but your answer is bad (time is too big or wrong answers")
            dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        dialog.exec()
        check = self.ui.page_3.findChild(QPushButton, f'check')
        self.ui.import_card.setEnabled(False)
        check.setEnabled(False)


    def check_cards_complete(self):
        if current_number_translate == current_number_word and current_number_word == round.number_of_cards:
            check = self.ui.page_3.findChild(QPushButton, f'check')
            check.setEnabled(True)
            check.setStyleSheet("QPushButton{\n"
            "background-color: rgb(255, 111, 89);\n"
            "font: 30pt \"Century Gothic\";\n"
            "font-weight: bold;\n"
            "color:rgb(252, 250, 250);\n"
            "border-radius:20px;\n"
            "}\n"
            "QPushButton:hover{\n"
            "background-color: rgb(150, 51, 51);\n"
            "}")
            check.setText("Check result")

    def increase_coord(self, x):
        return x + 55

    def _change_location(self, button):
        global current_number_word
        current_number_word += 1
        global sorted_words
        global y_word
        button.setGeometry(QtCore.QRect(x_word, y_word, 120, 50))
        y_word = self.increase_coord(y_word)
        sorted_words.append(button.text())
        self.check_cards_complete()

    def _change_location_translate(self, button):
        global current_number_translate
        current_number_translate += 1
        global sorted_translate
        global y_translate
        button.setGeometry(QtCore.QRect(x_translate, y_translate, 120, 50))
        y_translate = self.increase_coord(y_translate)
        sorted_translate.append(button.text())
        self.check_cards_complete()

    def _set_time_number(self):
        time = int(self.ui.time_test.text())
        number = int(self.ui.card_number.text())
        if time > 90 or number > 10:
            dialog = QMessageBox()
            dialog.setWindowTitle("Invalid time")
            dialog.setIcon(QMessageBox.Icon.Warning)
            dialog.setText("Consider the maximum value of time and cards number")
            dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
            dialog.exec()
        self.ui.stackedWidget.setCurrentIndex(2)
        global round
        round = Round(number, time)
        self.init_round(number)
        
    def init_round(self, number):
        global timee
        timee = time.perf_counter()
        global cards
        cards = round.choose_random_cards()
        for i in range(0, number):
            word_label = self.ui.page_3.findChild(QPushButton, f'word_{i+1}')
            word_label.setText(cards[i].word)
            translate_label = self.ui.page_3.findChild(QPushButton, f'translate_{i+1}')
            translate_label.setText(cards[i].translate)
            word_label.setStyleSheet("QPushButton{\n"
"background-color: rgb(252, 250, 250);\n"
"font: 20px \"Century Gothic\";\n"
"font-weight: bold;\n"
"color:rgb(37, 68, 65);\n"
"border-radius:10px;\n"
"padding-left:5px;\n"
"padding-right:5px;\n"
"}\n")
            word_label.resize(130,50)
            translate_label.setStyleSheet("QPushButton{\n"
"background-color: rgb(112, 86, 109);\n"
"font: 20px \"Century Gothic\";\n"
"font-weight: bold;\n"
"color:rgb(252, 250, 250);\n"
"border-radius:10px;\n"
"padding-left:5px;\n"
"padding-right:5px;\n"
"}\n")
            translate_label.resize(130,50)
            for i in range(number,10):
                word_label = self.ui.page_3.findChild(QPushButton, f'word_{i+1}')
                translate_label = self.ui.page_3.findChild(QPushButton, f'translate_{i+1}')
                word_label.setStyleSheet("QPushButton{\n"
                "background-color: transparent;\n"
                "color: transparent;\n"
                "}\n")
                word_label.setEnabled(False)
                translate_label.setStyleSheet("QPushButton{\n"
                "background-color: transparent;\n"
                "color: transparent;\n"
                "}\n")
                translate_label.setEnabled(False)
            check = self.ui.page_3.findChild(QPushButton, f'check')
            check.setStyleSheet("QPushButton{\n"
                "background-color: transparent;\n"
                "color: transparent;\n"
                "}\n")
            check.setEnabled(False)

    def _turn_page(self):
        self.ui.stackedWidget.setCurrentIndex(1)

def guiMain(args):
    app = QApplication(args)
    window = FiszkiWindow()
    window.show()
    return app.exec()

if __name__ == "__main__":
    guiMain(sys.argv)

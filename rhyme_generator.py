import sys
import re
import random
import nltk
from nltk.corpus import words
from nltk.tokenize import word_tokenize
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget, QMessageBox

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('words')


class RhymeGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 400, 400)
        self.setWindowTitle('Russian Rhyme Generator')

        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10, 10, 380, 180)

        self.generate_button = QPushButton('Generate Rhymes', self)
        self.generate_button.setGeometry(10, 200, 120, 40)
        self.generate_button.clicked.connect(self.generate_rhymes)

        self.result_text = QTextEdit(self)
        self.result_text.setGeometry(10, 250, 380, 140)
        self.result_text.setReadOnly(True)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.generate_button)
        self.layout.addWidget(self.result_text)

        self.central_widget = QWidget(self)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.nltk_words = set(words.words())

    def extract_words(self, text):
        words = word_tokenize(text)
        return words

    def find_rhymes(self, word):
        stressed_word = nltk.tag.pos_tag([word])[0][0]
        rhymes = []

        for w in self.nltk_words:
            stressed_w = nltk.tag.pos_tag([w])[0][0]
            if stressed_word[-3:] == stressed_w[-3:]:
                rhymes.append(w)
        return rhymes

    def is_russian(self, text):
        russian_characters = re.compile("[а-яА-Я]+")
        return bool(russian_characters.search(text))

    def generate_rhymes(self):
        input_text = self.text_edit.toPlainText()

        if not self.is_russian(input_text):
            QMessageBox.warning(self, 'Input Error', 'Please enter Russian text.')
            return

        if len(input_text) > 300:
            QMessageBox.warning(self, 'Input Error', 'Input text should not exceed 300 characters.')
            return

        words = self.extract_words(input_text)
        unique_words = list(set(words))

        if not unique_words:
            QMessageBox.warning(self, 'Input Error', 'No words in the input text.')
            return

        rhymes_dict = {}
        for word in unique_words:
            rhymes = self.find_rhymes(word)
            if rhymes:
                rhymes_dict[word] = rhymes

        if not rhymes_dict:
            self.result_text.setPlainText("No rhymes found.")
        else:
            result_str = "Rhymes:\n"
            for word, rhyme_list in rhymes_dict.items():
                result_str += f"{word}: {', '.join(rhyme_list)}\n"
            self.result_text.setPlainText(result_str)


def main():
    app = QApplication(sys.argv)
    window = RhymeGeneratorApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

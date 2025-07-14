from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5 import QtWidgets
import sys

def on_clicked():
    print('Pressed')

def main():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(200, 200, 300, 300)
    win.setWindowTitle("My first window")

    text = QLabel(win)
    text.setText('Hi this is my first code')
    text.move(50, 50)

    btn1=QtWidgets.QPushButton(win)
    btn1.setText("Click")
    btn1.clicked.connect(on_clicked)
    win.show()
    sys.exit(app.exec_())

main()
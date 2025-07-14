from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setGeometry(0, 0, 300, 300)
    window.show()
    
    sys.exit(app.exec_())

main()
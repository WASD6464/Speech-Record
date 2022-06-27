import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel



app = QApplication(sys.argv)
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Speech Assistant - Wait...")
        self.setGeometry(300,300,400,300)

        self.main_text = QLabel(self)
        self.main_text.setText("Your Command: ")
        self.main_text.move(10,200)
        self.main_text.setFixedWidth(100)

        self.user_text = QLabel(self)
        self.user_text.setText("")
        self.user_text.move(110,200)


        self.butt = QPushButton("Press Me!", self)
        self.butt.setText("Record")
        self.butt.resize(350,100)
        self.butt.move(25,25)
        self.butt.clicked.connect(self.progchange)

    def progchange(self):
        self.butt.setText("Recording...")
        self.butt.setEnabled(False)
        self.setWindowTitle("Speech Assistant - Process...")

window = MainWindow()
window.show()

app.exec()
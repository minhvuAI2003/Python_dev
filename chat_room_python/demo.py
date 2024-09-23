import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog

class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Video Conversion Demo')
        self.setGeometry(100, 100, 400, 300)

        self.button = QPushButton('Open Video', self)
        self.button.clicked.connect(self.showDialog)
        self.button.setGeometry(150, 130, 100, 30)

    def showDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Video", "C:\\",
                                                  "Video Files (*.mp4 *.avi *.mkv *.mov)", options=options)
        if fileName:
            self.convert_to_wmv2(fileName)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = AppDemo()
    demo.show()
    sys.exit(app.exec_())

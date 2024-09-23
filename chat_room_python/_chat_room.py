import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from demo import Ui_Dialog


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.st = Ui_Dialog()
        self.st.setupUi(self)
       # self.browse.clicked.connect(self.browsefiles)
        self.st.browse.clicked.connect(self.browsefiles)

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'D:\codefirst.io\PyQt5 tutorials\Browse Files',
                                            'Images (*.png, *.xmp *.jpg)')
        self.st.filename.setText(fname[0])


app = QApplication(sys.argv)
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(400)
widget.setFixedHeight(300)
widget.show()
sys.exit(app.exec_())

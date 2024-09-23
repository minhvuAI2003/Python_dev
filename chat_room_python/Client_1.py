import faulthandler
from Business_logic import BO as server
import socket
import sys
import threading
from Video_frame import Window
import mysql.connector
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.Qt import Qt
from Chat_room import Ui_MainWindow
import subprocess

# db = mysql.connector.connect(host="localhost", user="root", passwd="root", database="pbl5")

seperator = "do*(J#Feos(#JF1214@**jv2"
grant_port = "hIHO@HOhO@Q*hFQ#HOO#hh(%($*o9"
get_message_content = "!*&*hvHHOFHh9h93r3992338838"
status_update = "23ju9j29j(#GN$N(Wgwm123(@(@((9GJMMG"
message_update = "rkw(@Hfhieh299292BVBB@^^@"
get_port_address = "eowje283*@hfh3948"
get_ID_user = "ewj9UH(h9wheH#(@vdn*#*#34443"
get_trangthai = "wqjd92882@83hfSE"
check_message = "wj3fj@Jfq@h@*@wowww"
insert_message = "UHD*@hfshd@993900239"
get_user_by_ID = "sisidn*G*WQWQ2121221"
khongcogi = "290hf8&@*fbhdh2178177821&hos((***"
dauhieu = "34fhew8o8w%%@^@êyyde%^@"
status_update_msg = "fhw92392hf!&((@g323"
get_status_msg = "uwq89q@fj3gh))#Jqw"


class MyMainWindow(QMainWindow):
    update_text_signal = pyqtSignal(str)
    messagebox = pyqtSignal(str, str)

    def __init__(self, username="Hieu Pham"):
        super().__init__()
        self.video_window = None
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate(username, username))

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect(("172.15.112.196", 1503))
        self.server_socket2.connect(("172.15.112.196", 1504))
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.name = username
        self.client_socket.connect(("8.8.8.8", 80))
        #self.server = server()
        # Get the local IP address
        self.ip_address = self.client_socket.getsockname()[0]
        # self.port = self.client_socket.getsockname()[1]
        # self.server.port_update(self.name, self.port)

        # self.port = self.server.grant_port(self.name, self.ip_address)
        # self.server_socket.sendall(grant_port.encode('utf-8'))
        self.server_socket.sendall(self.name.encode('utf-8'))
        self.server_socket.sendall(self.ip_address.encode('utf-8'))
        self.list_of_user = self.initialize()
        #self.initialize()
        # self.server_socket.sendall(str(self.port).encode('utf-8'))

        # print(self.ip_address)
        # print(self.port)
        # self.server_socket.bind((self.ip_address, self.port))
        # self.text = ""
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # Set up the UI
        self.loadUsers()
        self.ui.list_user.setCurrentRow(1)

        # self.ui.plainTextEdit_2.keyPressEvent(e)
        currentIndex = self.ui.list_user.currentRow()
        item = self.ui.list_user.item(currentIndex)
        self.ui.label_3.setText(item.text())

        # self.text = self.server.chat_showing(self.name, item.text())
        self.ui.plainTextEdit.setPlainText(self.get_message_content(self.name, item.text()))
        # print(db)
        self.ui.list_user.clicked.connect(self.change)
        self.update_text_signal.connect(self.appendtext)
        self.messagebox.connect(self.thongbao)
        self.ui.plainTextEdit_2.textChanged.connect(self.doimau)
        # self.ui.list_user.clicked.connect(self.doimau)
        self.status_update(self.name, '1')
        self.ui.Send.clicked.connect(self.hienvideo)

        # self.ui.Send.clicked.connect(self.hienvideo)
        # self.message = {}
        # for i in range(self.ui.list_user.count()):
        # self.message[self.ui.list_user.item(i).text()] = ""

        ''''
        self.thread = threading.Thread(target=self.receiving)
        self.thread.start()
        self.tat = False
        '''

    # def set_video(self, w):
    #  w.show()
    def initialize(self):
        tt = []
        count = int(self.server_socket.recv(1024).decode())
        print(count)
        for i in range(count):
            tt.append(self.server_socket.recv(1024).decode('utf-8'))
        return tt

    def hienvideo(self):
        # app = QApplication(sys.argv)
        # subprocess.Popen([sys.executable, 'chat_room_test_video.py'])
        self.video_window = Window()
        self.video_window.show()

    # sys.exit(app.exec_())
    # self.hide()
    def doimau(self):
        if self.ui.plainTextEdit_2.hasFocus():
            st = self.get_status_msg(self.name, self.ui.label_3.text())

            row = self.ui.list_user.findItems(self.ui.label_3.text(), Qt.MatchExactly)
            row[0].setBackground(Qt.gray)
            if st == 1:
                self.update_status_msg(self.name, self.ui.label_3.text(), 0)

    def status_update(self, st1, st2):
        st = status_update + seperator + st1 + seperator + st2
        self.server_socket2.sendall(st.encode('utf-8'))

    def update_status_msg(self, st1, st2, val):
        st = status_update_msg + seperator + st1 + seperator + st2 + seperator + str(val)
        self.server_socket2.sendall(st.encode('utf-8'))

    def get_status_msg(self, st1, st2):
        st = get_status_msg + seperator + st1 + seperator + st2
        self.server_socket2.sendall(st.encode('utf-8'))
        data = self.server_socket2.recv(1024).decode('utf-8')

        if data.find(dauhieu) != -1:
            st = data[data.find(dauhieu) + len(dauhieu):]
            # print(st)
            if st == khongcogi:
                return ''
            return int(st)

    def get_message_content(self, st1, st2):
        print("problems")
        st = get_message_content + seperator + st1 + seperator + st2
        self.server_socket2.sendall(st.encode('utf-8'))

        data = self.server_socket2.recv(1024).decode('utf-8')

        if data.find(dauhieu) != -1:
            st = data[data.find(dauhieu) + len(dauhieu):]
            print(st)
            if st == khongcogi:
                return ''
            return st

    def thongbao(self, st, msg):

        row = self.ui.list_user.findItems(st, Qt.MatchExactly)
        print(st)
        print(msg)
        # self.message[st] = self.message[st] + "\n" + msg
        data = self.get_message_content(self.name, st)
        data += "\n" + msg
        self.message_update(data, self.name, st)
        row[0].setBackground(Qt.blue)

    def message_update(self, data, st1, st2):
        st2 = message_update + seperator + data + seperator + st1 + seperator + st2
        self.server_socket2.sendall(st2.encode('utf-8'))

    def get_port_address(self, st):
        st1 = get_port_address + seperator + st
        self.server_socket2.sendall(st1.encode('utf-8'))
        data = self.server_socket2.recv(1024).decode()
        if data.find(dauhieu) != -1:
            st = data[data.find(dauhieu) + len(dauhieu):]
            print(f"port:{st}")
            return int(st)

    def get_ID_user(self, st):
        st1 = get_ID_user + seperator + st
        self.server_socket2.sendall(st1.encode('utf-8'))
        data = self.server_socket2.recv(1024).decode()
        if data.find(dauhieu) != -1:
            st = data[data.find(dauhieu) + len(dauhieu):]
            print(f"ID:{st}")
            return int(st)

    def get_user_by_ID(self, ID):
        st = get_user_by_ID + seperator + str(ID)
        self.server_socket2.sendall(st.encode('utf-8'))

        data = self.server_socket2.recv(1024).decode()
        if data.find(dauhieu) != -1:
            st = data[data.find(dauhieu) + len(dauhieu):]
            return str(st)

    def get_trangthai(self, st):
        st1 = get_trangthai + seperator + st
        self.server_socket2.sendall(st1.encode('utf-8'))
        data = self.server_socket2.recv(1024).decode()
        if data.find(dauhieu) != -1:
            st = data[data.find(dauhieu) + len(dauhieu):]
            print(f"status:{st}")
            return int(st)

    def keyPressEvent(self, a0):
        print("hello")
        if a0.key() == Qt.Key_Return:
            print("pressed")
            name = self.ui.label_3.text()
            text = self.ui.plainTextEdit_2.toPlainText()
            if text != "":
                # self.message[name] = self.message[name] + "\nYou: " + text + "\n\n"

                # self.text += "\nYou: " + text + "\n\n"
                print("0")
                data1 = self.get_message_content(self.name, name) + "\nYou: " + text + "\n\n"
                print("1")
                self.ui.plainTextEdit.appendPlainText("You: " + text + "\n\n")
                self.ui.plainTextEdit_2.setPlainText("")
                self.message_update(data1, self.name, name)
                # data2 = self.server.get_message_content(name, self.name) + "\nGuest: " + text + "\n\n"
                # self.server.message_update(data2, name, self.name)
                # ip = self.server.get_ip_address(name)

                port = self.get_port_address(name)
                print("2")
                ID = self.get_ID_user(self.name)
                print("3")
                idx = self.get_ID_user(name)
                print("4")
                # print(ip)
                # print(port)
                status = self.get_trangthai(name)
                print("5")
                if port != 0:
                    tmp = str(ID) + "You: " + text + "\n\n" + "You" + str(status) + str(port) + str(idx)
                else:
                    tmp = str(ID) + "You: " + text + "\n\n" + "You" + str(status) + "0000" + str(idx)
                # tmp += str(status)+str(self.port)

                if status == 0:
                    data2 = self.get_message_content(name, self.name) + "\nGuest: " + text + "\n\n"
                    self.message_update(data2, name, self.name)
                    self.update_status_msg(name, self.name, 1)
                self.server_socket.sendall(tmp.encode('utf-8'))
            a0.accept()

    def appendtext(self, txt):
        try:
            self.ui.plainTextEdit.appendPlainText(txt)
            # self.message[self.ui.label_3.text()] = self.message[self.ui.label_3.text()] + "\n" + txt
            data = self.get_message_content(self.name, self.ui.label_3.text())
            data += "\n" + txt
            self.server.message_update(data, self.name, self.ui.label_3.text())
        except Exception as e:
            print("Error appending text:", e)

    def change(self):
        currentIndex = self.ui.list_user.currentRow()
        item = self.ui.list_user.item(currentIndex)
        print(item.text())
        # print(item)
        if item.text() != "":
            if item.background() != Qt.blue:
                item.setBackground(Qt.gray)
            for i in range(self.ui.list_user.count()):
                if self.ui.list_user.item(i) != item and self.ui.list_user.item(i).background() != Qt.blue:
                    self.ui.list_user.item(i).setBackground(Qt.white)
            self.ui.label_3.setText(item.text())
            # self.update_status_msg(self.name, item.text(), 0)
            # if self.message[item.text()] != "":

            # self.server.message_update(self.text, self.name, item.text())
            # self.message[item.text()] = ""
            # print(self.server.get_message_content("HoangNe", self.name))
            self.ui.plainTextEdit.clear()

            self.ui.plainTextEdit.setPlainText(self.get_message_content(self.name, item.text()))

    def loadUsers(self):
        self.ui.list_user.addItems([""])
        users = self.list_of_user
        for x in self.list_of_user:
            if x != self.name:
                self.ui.list_user.addItems([x])
        for i in range(len(users)):
            ten1 = users[i]
            # print(ten1)
            for j in range(len(users)):
                if i != j:
                    ten2 = users[j]
                    ktra = self.check_message(ten1, ten2)
                    if ktra == 0:
                        self.server.insert_message(ten1, ten2)
        for i in range(len(users)):
            ten1 = users[i]
            if ten1 != self.name:
                ktra_st = self.get_status_msg(self.name, ten1)
                if ktra_st == 1:
                    row = self.ui.list_user.findItems(ten1, Qt.MatchExactly)
                    row[0].setBackground(Qt.blue)

    def check_message(self, st1, st2):
        st = check_message + seperator + st1 + seperator + st2
        self.server_socket2.sendall(st.encode('utf-8'))

        data = self.server_socket2.recv(1024).decode()
        # print("data")
        return int(data)

    def insert_message(self, st1, st2):
        st = insert_message + seperator + st1 + seperator + st2
        self.server_socket2.sendall(st.encode('utf-8'))

    def closeEvent(self, a0):
        self.status_update(self.name, '0')
        self.server_socket.sendall("stop".encode('utf-8'))
    # self.server_socket.close()


def receiving(window):
    try:
        while True:

            data = window.server_socket.recv(1024)
            st = data.decode()
            print(f"received:{st}")
            if st.find(dauhieu) == -1:

                if st == "stop":
                    break
                print(st)
                ID = int(st[:st.find("You")])

                myresult = window.get_user_by_ID(ID)

                if myresult == window.ui.label_3.text():
                    print(1)
                    #            window.text += "Guest:" + st[5:]
                    # self.ui.plainTextEdit.clear()
                    print(st[5:])
                    window.update_text_signal.emit("Guest:" + st[(st.find("You") + 4):st.rfind("You")])
                    print("successful")
                else:
                    window.messagebox.emit(myresult, "Guest:" + st[(st.find("You") + 4):st.rfind("You")])
    finally:
        window.server_socket.close()


if __name__ == '__main__':
    faulthandler.enable()
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    thread = threading.Thread(target=receiving, args=[window])
    thread.start()
    sys.exit(app.exec_())

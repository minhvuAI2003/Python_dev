import socket
import threading
import base64
import time

import cv2
import imutils
import socket

import numpy as np

# import Threading
from Business_logic import BO as server

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
seperator = "do*(J#Feos(#JF1214@**jv2"
khongcogi = "290hf8&@*fbhdh2178177821&hos((***"
dauhieu = "34fhew8o8w%%@^@êyyde%^@"
status_update_msg = "fhw92392hf!&((@g323"
get_status_msg = "uwq89q@fj3gh))#Jqw"
get_all_user = "sduhw&@yhf2fkjej(((((((((((((((((((((((((("


class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.client_socket.connect(("8.8.8.8", 80))
        self.ip = "192.168.1.8"
        self.port = 1503
        self.port2 = 1504
        self.port3 = 1505
        self.socket.bind((self.ip, self.port))
        self.socket.listen(67)
        self.client_socket.bind((self.ip, self.port2))
        self.client_socket.listen(67)
        self.BUFF_SIZE = 65536

        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFF_SIZE)

        self.udp_socket.bind((self.ip, self.port3))
        # self.thread = threading.Thread(target=self.process)
        self.server = server()
        self.socket_list = {}
        # self.count = {}
        thread = threading.Thread(target=self.database)
        thread.start()
        thread_1 = threading.Thread(target=self.receive_video)
        thread_1.start()
        self.process()

    def receive_video(self):
        fps = 0
        st = 0
        frames_to_count = 20
        cnt = 0
        while True:

            while True:
                # print(count)
                packet, _ = self.udp_socket.recvfrom(self.BUFF_SIZE)
                if packet == b'Hello':
                    print("packet is none")
                    # server.explored.remove(port)
                    cv2.destroyAllWindows()

                    break

                data = base64.b64decode(packet)
                npdata = np.frombuffer(data, dtype=np.uint8)
                frame = cv2.imdecode(npdata, 1)

                frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                    (0, 0, 255), 2)
                cv2.imshow("RECEIVING VIDEO", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    cv2.destroyAllWindows()

                    break
                if cnt == frames_to_count:
                    try:
                        fps = round(frames_to_count / (time.time() - st))
                        st = time.time()
                        cnt = 0
                    except:
                        pass
                cnt += 1

    def get_server_ip(self):
        return self.ip

    def get_server_port(self):
        return self.port

    def xuli(self, client):
        try:

            while True:
                data = client.recv(1024)

                str_data = data.decode("utf-8")
                # print(str_data)
                if str_data == "stop":
                    # client.close()
                    client.sendall("stop".encode('utf-8'))
                    break

                """if not data:
                    break
                """
                ID = int(str_data[(str_data.rfind("You") + 8):])
                # myresult = self.server.get_user_by_ID(ID)
                # if self.count[addr[1]] == 0:
                # self.server.port_update(self.server.get_user_by_ID(ID), addr[1])
                # self.count[addr[1]] = 1

                # ip=self.server.get_ip_address(myresult)
                status = int(str_data[(str_data.rfind("You") + 3)])
                # print(self.server.get_user_by_ID(ID))
                print(status)
                if status == 1:
                    print(self.server.get_user_by_ID(ID))
                    port = int(str_data[(str_data.rfind("You") + 4):(str_data.rfind("You") + 8)])
                    if self.socket_list[port] is not None and port != 0:
                        self.socket_list[port].sendall(str_data.encode('utf-8'))

        finally:
            client.close()

    def progress(self, client):
        while True:
            data = client.recv(1024)

            str_data1 = data.decode("utf-8")
            # print(str_data)
            str_data = str_data1[:str_data1.find(seperator)]
            # print(str_data)

            if str_data == get_message_content:
                print("Message:")
                print(get_message_content)
                lst = str_data1.split(seperator)
                st = lst[1]
                st2 = lst[2]
                print(f" st:{st} st1:{st2}")
                data = self.server.get_message_content(st, st2)
                if data == "":
                    # client.sendall(dauhieu.encode('utf-8'))
                    st = dauhieu + khongcogi
                    client.sendall(st.encode('utf-8'))
                else:
                    # client.sendall(dauhieu.encode('utf-8'))
                    st = dauhieu + data
                    client.sendall(st.encode('utf-8'))
                print("Hiii")
                continue

            if str_data == status_update:
                print(status_update)
                lst = str_data1.split(seperator)
                st = lst[1]
                st1 = int(lst[2])
                self.server.status_update(st, st1)
                continue

            if str_data == message_update:
                print("Message")
                print(message_update)
                lst = str_data1.split(seperator)
                st = lst[1]
                st1 = lst[2]
                st2 = lst[3]
                self.server.message_update(st, st1, st2)
                continue

            if str_data == get_port_address:
                print("Message")
                print(get_port_address)
                lst = str_data1.split(seperator)

                port = self.server.get_port_address(lst[1])
                #  client.sendall(dauhieu.encode('utf-8'))
                st = dauhieu + str(port)
                client.sendall(st.encode('utf-8'))
                continue

            if str_data == get_ID_user:
                print("Message")
                print(get_ID_user)
                lst = str_data1.split(seperator)

                ID = self.server.get_ID_user(lst[1])
                # client.sendall(dauhieu.encode('utf-8'))
                st = dauhieu + str(ID)
                client.sendall(st.encode('utf-8'))
                continue

            if str_data == get_trangthai:
                print("Message")
                print(get_ID_user)
                lst = str_data1.split(seperator)

                status = self.server.get_trangthai(lst[1])
                st = dauhieu + str(status)

                client.sendall(st.encode('utf-8'))
                continue

            if str_data == check_message:
                print("message:")
                print(check_message)
                lst = str_data1.split(seperator)
                print(f"st1:{lst[1]} st2:{lst[2]}")
                st1 = lst[1]
                st2 = lst[2]
                port = self.server.check_message(st1, st2)
                client.sendall(str(port).encode('utf-8'))
                continue

            if str_data == insert_message:
                print("message:")
                print(insert_message)
                lst = str_data1.split(seperator)
                self.server.insert_message(lst[1], lst[2])
                continue

            if str_data == get_user_by_ID:
                print("message:")
                print(get_user_by_ID)
                lst = str_data1.split(seperator)
                ID = int(lst[1])
                user = self.server.get_user_by_ID(ID)

                st = dauhieu + user
                client.sendall(st.encode('utf-8'))
                continue
            if str_data == get_status_msg:
                print("message:")
                print(get_status_msg)
                lst = str_data1.split(seperator)
                st1 = lst[1]
                st2 = lst[2]
                user = str(self.server.get_status_message(st1, st2))

                st = dauhieu + user
                client.sendall(st.encode('utf-8'))
                continue
            if str_data == status_update_msg:
                print("Message")
                print(status_update_msg)
                lst = str_data1.split(seperator)
                st = lst[1]
                st1 = lst[2]
                st2 = lst[3]
                self.server.update_status_message(st, st1, int(st2))
                continue
            if str_data == get_all_user:
                print("Message")
                print(get_all_user)
                lst = str_data1.split(seperator)
                # st = lst[1]
                users = self.server.get_user_all()
            """if not data:
                break
            """

    def database(self):
        while True:
            client, _ = self.client_socket.accept()
            print("connected by ", _)
            thread = threading.Thread(target=self.progress, args=[client])
            thread.start()

    def process(self):
        while True:
            client, addr = self.socket.accept()
            # self.count[addr[1]] = 0
            print('Connected by', addr)
            name = client.recv(1024)
            name = name.decode()
            # print(str_data)
            print(name)
            ip = client.recv(1024)
            ip = ip.decode()
            print(ip)
            port = self.server.grant_port(name, ip)
            print(port)

            self.socket_list[port] = client

            users = self.server.get_user_all()
            client.sendall(str(len(users)).encode('utf-8'))
            for x in users:
                print(x[0])
                client.sendall((get_all_user+x[0]).encode('utf-8'))

            thread = threading.Thread(target=self.xuli, args=[client])
            thread.start()


s = Server()

import random

import mysql.connector


class DAO:
    def __init__(self):
        self.database = mysql.connector.connect(host="localhost", user="root", passwd="root", database="pbl5")
        self.cursor = self.database.cursor()

    def port_grant(self, name, ip_address) -> int:
        cursor = self.database.cursor()
        cursor.execute(f"select * from server_distribution where Username='{name}'")
        record = cursor.fetchall()
        if len(record) != 0:
            cursor.execute(f"update server_distribution set ip='{ip_address}' where Username='{name}'")
            self.database.commit()
        else:
            cursor.execute(f"insert into server_distribution(Username,ip) values('{name}','{ip_address}')")
            self.database.commit()
        # server_address = ('localhost', 5678)

        # self.server_socket.bind(server_address)
        cursor = self.database.cursor()
        cursor.execute(f"select port from port_distribution where Username='{name}'")
        data = cursor.fetchall()
        if len(data) == 0:
            cursor.execute("select port from port_distribution")
            data1 = cursor.fetchall()
            lst = []
            if len(data1) != 0:
                for i in data1:
                    lst.append(i[0])
            while True:
                port = random.randint(6000, 7000)
                if port not in lst:
                    port1 = port
                    sql = "insert into port_distribution(Username,port) values(%s,%s)"
                    val = (name, port)
                    cursor.execute(sql, val)
                    self.database.commit()
                    # self.server_socket.bind((self.ip_address, self.port))
                    return port1

        else:
            port = data[0][0]
            # self.server_socket.bind((self.ip_address, self.port))
            return port

    def get_status(self, name):
        self.cursor.execute(f"select status from statuc where Username='{name}'")
        return self.cursor.fetchall()[0][0]

    def update_status(self, name, val):
        self.cursor.execute(f"update statuc set status={val} where Username='{name}'")
        self.database.commit()

    def get_ip(self, name):

        self.cursor.execute(f"select ip from server_distribution where Username='{name}'")
        data = self.cursor.fetchall()[0][0]
        return data

    def get_port(self, name):
        self.cursor.execute(f"select port from port_distribution where Username='{name}'")
        data = self.cursor.fetchall()
        if len(data) == 0:
            return 0
        return data[0][0]

    def update_port(self, name, val):
        self.cursor.execute(f"update port_distribution set port={val} where Username='{name}'")
        self.database.commit()

    def getID_user(self, name):

        self.cursor.execute(f"select ID from account where Username='{name}'")
        return self.cursor.fetchall()[0][0]

    def update_message(self, content, Guest1, Guest2):
        sql = f"update message set Content='{content}' where Guest1='{Guest1}' and Guest2='{Guest2}'"

        self.cursor.execute(sql)
        self.database.commit()

    def get_content(self, name1, name2):
        self.cursor.execute(f"select Content from message where Guest1='{name1}' and Guest2='{name2}'")
        data = self.cursor.fetchall()
        if len(data) == 0:
            return ''
        return data[0][0]

    def get_all_users(self):
        self.cursor.execute("select Username from account")
        data = self.cursor.fetchall()
        data1 = str(data)
        print(data1)
        return data

    def check_existing_message(self, name1, name2):
        self.cursor.execute(f"select * from message where Guest1 ='{name1}' and Guest2='{name2}'")
        data = self.cursor.fetchall()
        if len(data) > 0:
            return 1

        return 0

    def insert_message_into_db(self, name1, name2):
        self.cursor.execute(f"insert into message(Guest1,Guest2,Content,status) values ('{name1}','{name2}','',0)")
        self.database.commit()

    def get_user_from_ID(self, ID):
        self.cursor.execute(f"select Username from account where ID={ID}")
        return self.cursor.fetchall()[0][0]

    def status_message_update(self, st1, st2, status):

        self.cursor.execute(f"update message set status={status} where Guest1='{st1}' and Guest2='{st2}'")
        self.database.commit()

    def get_message_status(self, st1, st2):
        self.cursor.execute(f"select status from message where Guest1='{st1}' and Guest2='{st2}'")
        data = self.cursor.fetchall()
        print(data)
        if len(data) == 0:
            return 0
        return data[0][0]

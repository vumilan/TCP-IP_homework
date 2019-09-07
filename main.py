from TCPserver import RobotControlServer, TCPSocketHandler
from config import HOST, PORT

if __name__ == "__main__":
    server = RobotControlServer((HOST, PORT), TCPSocketHandler)
    print("Starting TCP Robot Control server on {}:{}".format(HOST, PORT))
    server.serve_forever()





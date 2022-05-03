import os
import paramiko
import socket
import sys
import threading

CWD = os.path.dirname(os.path.realpath(__file__))
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, 'test_rsa.key'))
    
class Server(paramiko.ServerInterface):
    def __init__(self, user, password):
        self.event = threading.Event()  
        self.user = user
        self.password = password
        super().__init__()
    
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    
    def check_auth_password(self, username, password):
        if (username == self.user) and (password == self.password):
            return paramiko.AUTH_SUCCESSFUL

if __name__ == '__main__':
    import argparse
    import getpass

    parser = argparse.ArgumentParser(
        description="SSH server to listen and connect with reverse client.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('-p', '--port', dest='port', type=int, help='ssh port to listen on', default=2222)
    parser.add_argument('-u', '--user', dest='user', help='username to authenticate incoming connections', default=getpass.getuser())
    parser.add_argument('--passwd', dest='password', help='password to authenticate incoming connections', default='bhpssh')
    ns = parser.parse_args()

    server = '0.0.0.0'
    ssh_port = ns.port
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server, ssh_port))
        sock.listen(100)
        print('[+] Listening for connection...')
        client, addr = sock.accept()
        print('[+] Got a connection!', client, addr)

        bhSession = paramiko.Transport(client)
        bhSession.add_server_key(HOSTKEY)
        server = Server(ns.user, ns.password)
        bhSession.start_server(server=server)
        chan=bhSession.accept(20)
        if chan is None:
            print('*** No channel.')
            sys.exit(1)
        
        print('[+] Authenticated!')
        print(chan.recv(1024))
        chan.send('Welcome to bh_ssh')
        try:
            while True:
                command = input("Enter command: ")
                if command != "exit":
                    chan.send(command)
                    res = chan.recv(8192)
                    print(res.decode())
                else:
                    chan.send("exit")
                    print("exiting")
                    bhSession.close()
                    break
        except KeyboardInterrupt:
            bhSession.close()


    except Exception as e:
        print('[-] Listen failed: ' + str(e))
        sys.exit(1)

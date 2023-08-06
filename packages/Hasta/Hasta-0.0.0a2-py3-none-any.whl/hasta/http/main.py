'''

    Copyright (c) 2021-2021 Anoki Youssou

    -------------------------------------

    This file is used as the main file.

    -------------------------------------

    Big thanks to Archer Reilly for providing me examples !

'''

import socket

from request import Request
from response import Response
from environ import Environ

class Main:

    # Starting point.
    def __init__(self , ip , port , app):

        print("\nInitializing Hasta...")
        print("\n---------------------\n")

        self.init_info(app)
        self.init_modules()
        self.init_socket(ip , port)
        self.serve_forever()

    def init_info(self , app):

        print("Loading config..")

        self.ip_address_version = socket.AF_INET
        self.socket_protocol = socket.SOCK_STREAM
        self.request_size = 1

        self.application = app

    # Initialize the modules.
    def init_modules(self):

        print("Initializing modules..")

        self.environ = Environ()

        self.request = Request()
        self.response = Response()

    # Initialize the socket.
    def init_socket(self , server_ip_address , server_port):

        print("Initializing socket...")

        # Initialize a socket.
        self.socket = sock = socket.socket(self.ip_address_version , self.socket_protocol)

        # Reuse the socket.
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the server address.
        sock.bind((server_ip_address , server_port))

        sock.listen(1)

        # Get server host name and port
        host, port = sock.getsockname()[:2]

        self.server_ip = server_ip_address    

        self.server_name = socket.getfqdn(host)

        self.server_port = port

    def serve_forever(self):

        print (

        f"\nReady for accepting request! Serving at {self.server_ip} . Port : {self.server_port} . Name : {self.server_name}"
            
        )

        print("\n---------------------\n")

        environ = self.environ
        response = self.response

        sock = self.socket
        request = self.request

        # Loop that will respond to any request.

        try :
            while True:

                # Get the client connection and the client ip address.
                self.client_connection , self.client_ip_address = sock.accept()

                # Print the IP.
                print(f"\nRequest detected. IP : {self.client_ip_address[0]} . Port {self.client_ip_address[1]} .")

                print (

                    f"\nBEGINNING OF REQUEST FROM IP : {self.client_ip_address[0]} . Port {self.client_ip_address[1]} ."

                )

                print("\n---------------------\n")

                # Handle the request.
                request.handle_request (

                    self.server_name,
                    self.server_port,

                    self.client_connection , 

                    environ ,
                    response ,

                    self.application

                )

            sock.close()
            print("\n---------------------")

        except KeyboardInterrupt:

            print("\nGoodbye...\n")

            exit()








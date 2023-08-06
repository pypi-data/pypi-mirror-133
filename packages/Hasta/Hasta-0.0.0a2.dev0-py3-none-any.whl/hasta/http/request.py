'''

    Copyright (c) 2021-2021 Anoki Youssou

    -------------------------------------

    This file is used for handling request.

    -------------------------------------

    Big thanks to Archer Reilly for providing me examples !

'''

class Request:

    def __init__(self):

        pass

    def handle_request( self , name , port , client_connection , environ , response , app):

        # Get the request data.
        request_data = client_connection.recv(1024)

        self.request_data = request_data.decode('utf-8')

        # Print formatted request data which makes you look like a hacker.

        for line in request_data.splitlines():

            line = line.decode('utf-8')

            print(f'> {line}')

        # Get the request method, path, and the HTTP version used by the client.
        self.request_method , self.path , self.request_version  = self.parse_request(request_data)

        # Data needed by the environ.
        class environ_data :

            server_name = name ,                
            server_port = port ,
            server_path = self.path ,
            request_data_class = request_data ,
            request_method = self.request_method

        # Now, we have to make sure we deliver all the data to the environ.
        env = environ.get_environ (environ_data)

        '''

            Basically, we already proccess the request data.
            The processed data is now in the env. Now, we have
            to deliver env and the toggle for creating response
            (start_response) to the application. 

        '''
        response_body = app(env, response.start_response)

        '''

            Great, if start_response already do it's job, now
            time to finish the response, and then send it back
            to the client!

        '''

        # Construct a response and send it back to the client
        response.finish_response(response_body , client_connection)

    def parse_request(self, text):

        request_line = text.splitlines()[0]
        request_line = request_line.decode("utf-8")
        request_line = request_line.rstrip('\r\n')

        # Break down the request line into components.

        (

            self.request_method,   # Request methods.
            self.request_version , # HTTP Version that is used for the request.
            self.path,             # Path.
                                  

        ) = request_line.split()

        return self.request_method , self.path , self.request_version 



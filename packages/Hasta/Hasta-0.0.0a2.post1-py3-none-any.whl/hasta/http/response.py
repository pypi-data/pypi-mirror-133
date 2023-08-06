'''

    Copyright (c) 2021-2021 Anoki Youssou

    -------------------------------------

    This file is used for managing response.

    -------------------------------------

    Big thanks to Archer Reilly for providing me examples !

'''

class Response:

    def __init__(self):

        pass

    def start_response(self , status , response_headers):

        server_header = [

            ('Date', 'Mon, 15 Jul 2019 5:54:48 GMT'), # Temporarly.
            ('Server', 'hasta')

        ]

        self.headers_set = [status, response_headers + server_header]

    def finish_response(self, response_body , client_connection):

        try:

            status, response_headers = self.headers_set

            # Write the response header.
            response = f'HTTP/1.1 {status}\r\n'

            for header in response_headers:

                # TELNET protocol such as TCP apparently requires \r\n at the start of the line, weird.
                response += '{0}: {1}\r\n'.format(*header)

            # TELNET protocol such as TCP apparently requires \r\n at the start of the line, weird.
            response += '\r\n'

            for data in response_body:

                # Decode the data, using utf-8.
                response += data.decode('utf-8')

            # We have to convert it to bytes.
            response_bytes = response.encode()

            # SEND THE DATA ! FINALLY THE JOB IS DONE !
            client_connection.sendall(response_bytes)

        finally:

            # Close the connection.
            client_connection.close()
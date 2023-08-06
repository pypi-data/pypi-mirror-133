'''

    Copyright (c) 2021-2021 Anoki Youssou

    -------------------------------------

    This file is used for environ.

    -------------------------------------

    Big thanks to Archer Reilly for providing me examples !

'''

import io
import sys

class Environ:

    def __init__(self):

        pass

    def get_environ(self , environ_data):

        request_data = b''

        for item in environ_data.request_data_class:
            request_data = request_data + item

        request_data = request_data.decode("utf-8") 

        env = {}

        # WSGI : General info.

        env['wsgi.version']      = (1, 0)
        env['wsgi.url_scheme']   = 'http' # Using http.
        env['wsgi.input']        = io.StringIO(request_data) # Get the request data.
        env['wsgi.errors']       = sys.stderr
        env['wsgi.multithread']  = False
        env['wsgi.multiprocess'] = False # For now, it is false. I haven't implement multiproccess, probably via thread.
        env['wsgi.run_once']     = False # Nope, this server can receive more than one request.

        # Required CGI variables.
                
        env['SERVER_NAME']       = environ_data.server_name       # Server name.
        env['SERVER_PORT']       = str(environ_data.server_port)  # Server port.
        env['PATH_INFO']         = environ_data.server_path       # Server path where index.html is located.
        env['REQUEST_METHOD']    = environ_data.request_method    # Request method.
        
        return env
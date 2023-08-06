from hasta.http.main import Main

class Init:

    def __init__(self):

        pass

    def __call__(self , ip , port , app):

        main = Main(ip , port , app)


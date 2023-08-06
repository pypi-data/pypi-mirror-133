import setuptools
import json

def run(result):

    r = result

    with open(r.long_desc , "r") as fh:

        long_description = fh.read()
        

    setuptools.setup (

        # This is the name of the package.
        name = r.name ,  

        # The initial release version.                   
        version = r.version ,  

        # Full name of the author.                      
        author = r.author , 

        author_email='anoki.youssou@gmail.com',

        # Description.                 
        description = r.short_desc ,

        # Long description read from the the readme file.
        long_description = long_description ,      
        long_description_content_type = r.long_desc_content_type ,

        # List of all python modules to be installed.
        packages = setuptools.find_packages() ,  

        # Directory of the source code of the package.       
        package_dir = {'':r.path} , 

        # Information to filter the project on PyPi website.
        classifiers = [

            r.lang,
            r.os,
            r.topic,
            r.natlang ,
            r.dev,
            r.license

        ] ,

        # Minimum version requirement of the package.
        python_requires = r.python ,  

        # Name of the python package.              
        py_modules = [r.pkg] ,      

        # Install other dependencies if any.    
        install_requires = r.depen

    )

class Convert:

    def __init__(self):

        pass

    def __call__(self):

        open_file = self.open_file()

        self.data = self.read_file(open_file)

        result = self.convert()

        run(result)

    def open_file(self):

        open_file = open(r'./config.json', 'r')

        return open_file

    def read_file(self , open_file):

        data = json.load(open_file)

        return data

    def convert(self):

        data = self.data

        class result:

            name = data['info']['name']
            pkg = data['info']['pkg']

            author = data['author']['name']
            email = data['author']['email']

            path = data['info']['path']

            version = data['ver']['version']

            short_desc = data['desc']['short']
            long_desc = data['desc']['long']
            long_desc_content_type = data['desc']['content_type'] 

            python = data['require']['python']
            depen = data['require']['dependencies']

            lang = data['classifiers']['lang']
            os = data['classifiers']['os']
            topic = data['classifiers']['topic']
            natlang = data['classifiers']['natlang']
            dev = data['classifiers']['dev']
            license = data['classifiers']['license']

        return result

    
c = Convert()

c()
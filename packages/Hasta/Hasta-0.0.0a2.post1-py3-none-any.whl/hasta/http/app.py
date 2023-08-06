from init import Init

def application(environ, start_response):

   response_body = [
       '''
<!DOCTYPE html>

<html>

    <head>

        <title>HELLO WORLD</title>

    </head>

    <body>

        <style>

            .wow {
                color : blue;
                font-weight : bold;
            };

        </style>

        <hl1 class="wow">If you see this message then that means I am alive!</hl1>

        <button onclick="run()">Click me!</button>

        <p id="demo"></p>

        <script type="text/javascript">

            function run() {

                element = document.querySelector("#demo");

                element.innerHTML = "YOOOOO";

            };

        </script>

    </body>

</html>
       '''
   ]
   
   response_body = '\n'.join(response_body)

   status = '200 OK'

   response_headers = [
       ('Content-type', 'text/html'),
   ]

   start_response(status, response_headers)

   return [response_body.encode('utf-8')]

init = Init()

init('0.0.0.0' , 8000 , app = application)
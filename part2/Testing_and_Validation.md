#Testing and Validation  

##Codes de retour HTTP  
200 OK: The request has been processed successfully (used for successful GET and PUT requests).  
201 Created : A new element has been successfully created (used for successful POST requests).  
400 Bad Request : The request sent is incorrect (for example, a mandatory field is missing).  
404 Not Found : The requested resource does not exist.  
500 Internal Server Error : An internal server error has occurred, often due to a bug in the code.  

## Using Postman  

Postman is a tool that makes it easy to test APIs by sending HTTP requests and viewing the responses.  
Intuitive interface: Postman provides a simple interface for sending requests (GET, POST, PUT, DELETE) to the API and configuring headers, body and parameters.  
Automated tests : Postman also allows you to define test scripts to automatically check the response.  
Exemple de test : Pour la classe Users, nous utilisons Postman pour vérifier les codes de retour et valider les réponses pour les opérations CRUD.  



To run a test with postman, we must first launch the local server with the python3 command run.py
        python3 run.py  

        root@hey-coucou-xav:~/hbnb/part2# python3 run.py 
        * Serving Flask app 'app'
        * Debug mode: on
        WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
        * Running on http://127.0.0.1:5000
        Press CTRL+C to quit
        * Restarting with stat
        * Debugger is active!
        * Debugger PIN: 823-870-797

        
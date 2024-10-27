# Testing and Validation  

## HTTP Return Codes  
- **200 OK**: The request has been processed successfully (used for successful GET and PUT requests).
- **201 Created**: A new element has been successfully created (used for successful POST requests).
- **400 Bad Request**: The request sent is incorrect (for example, a mandatory field is missing).
- **404 Not Found**: The requested resource does not exist.
- **500 Internal Server Error**: An internal server error has occurred, often due to a bug in the code.

## Using Postman  

Postman is a tool that makes it easy to test APIs by sending HTTP requests and viewing the responses.

- **Intuitive interface**: Postman provides a simple interface for sending requests (GET, POST, PUT, DELETE) to the API and configuring headers, body, and parameters.
- **Automated tests**: Postman also allows you to define test scripts to automatically check the response.
  
**Example of testing**: For the Users class, we use Postman to check return codes and validate responses for CRUD operations.

### Running a Test with Postman  
To run a test with Postman, first launch the local server with the following command:
```bash
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

Example with the Users class:  

**POST**

        http://127.0.0.1:5000/api/v1/users/
        
        {  
            "first_name": "John",  
            "last_name": "Doe",  
            "email": "john.doe@example.com"
        } 
        
        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        }

        201CREATED
        313 ms
        312 B
        
        {
            ····"id":·"cfaa0359-f8f2-45e6-9333-b790ade56d6b",  
            ····"first_name":·"John",  
            ····"last_name":·"Doe",  
            ····"email":·"john.doe@example.com"  
        }

        **GET**

        http://127.0.0.1:5000/api/v1/users/cfaa0359-f8f2-45e6-9333-b790ade56d6b  
        
        {  
            "first_name": "John",  
            "last_name": "Doe",  
            "email": "john.doe@example.com"
        } 

        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        }

        200OK
        156 ms
        307 B
        
        {    
            "id": "cfaa0359-f8f2-45e6-9333-b790ade56d6b",    
            "first_name": "John",    
            "last_name": "Doe",    
            "email": "john.doe@example.com"  
        }


        ### PUT

        http://127.0.0.1:5000/api/v1/users/cfaa0359-f8f2-45e6-9333-b790ade56d6b

        {  
            "first_name": "John",  
            "last_name": "Doe",  
            "email": "john.doe@example.com"
        } 

        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        }

        200OK
        53 ms
        307 B
        
        {   "id": "cfaa0359-f8f2-45e6-9333-b790ade56d6b",    
            "first_name": "John",    
            "last_name": "Doe",    
            "email": "john.doe@example.com"  
        }


        ### DELETE

        http://127.0.0.1:5000/api/v1/users/cfaa0359-f8f2-45e6-9333-b790ade56d6b
        
        {  
            "first_name": "John",  
            "last_name": "Doe",  
            "email": "john.doe@example.com"
        }

        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        }

        200OK
        9 ms
        213 B
        
        {    "message": "User deleted successfully"}


        127.0.0.1 - - [26/Oct/2024 16:14:40] "POST /api/v1/users/ HTTP/1.1" 201 -
        127.0.0.1 - - [26/Oct/2024 16:17:57] "GET /api/v1/users/cfaa0359-f8f2-45e6-9333-b790ade56d6b HTTP/1.1" 200 -
        127.0.0.1 - - [26/Oct/2024 16:19:15] "PUT /api/v1/users/cfaa0359-f8f2-45e6-9333-b790ade56d6b HTTP/1.1" 200 -
        127.0.0.1 - - [26/Oct/2024 16:22:00] "DELETE /api/v1/users/cfaa0359-f8f2-45e6-9333-b790ade56d6b HTTP/1.1" 200 -


Example with the Amenities class:  

        ### POST
        http://127.0.0.1:5000/api/v1/amenities/
        
        {    "name": "wifi"}

        {
            "name": "wifi"
        }
        201CREATED
        11 ms
        244 B
        1234
        {····"id":·"279c8831-a7c6-4c93-8ed1-d7ad56cfa29a",····"name":·"wifi"}

        ### GET
        http://127.0.0.1:5000/api/v1/amenities/279c8831-a7c6-4c93-8ed1-d7ad56cfa29a
        
        {    "name": "wifi"}

        {
            "name": "wifi"
        }
        200OK
        66 ms
        239 B
        1234
        {    "id": "279c8831-a7c6-4c93-8ed1-d7ad56cfa29a",    "name": "wifi"}

        ### PUT
        http://127.0.0.1:5000/api/v1/amenities/279c8831-a7c6-4c93-8ed1-d7ad56cfa29a
        
        {    "name": "wifi"}

        {
            "name": "wifi"
        }
        200OK
        42 ms
        215 B
        123
        {    "message": "Amenity updated sucessfully"}

        ### DELETE
        http://127.0.0.1:5000/api/v1/amenities/279c8831-a7c6-4c93-8ed1-d7ad56cfa29a
        
        {    "name": "wifi"}

        {
            "name": "wifi"
        }
        200OK
        42 ms
        215 B
        123
        {    "message": "Amenity updated sucessfully"}

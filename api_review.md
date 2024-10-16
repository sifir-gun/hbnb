
# API POST /reviews Sequence Diagram

## User Sends POST /reviews Request

**User**:  
This is the person who uses the application and submits a review for a place.

**API**:  
This is the interface that allows the user to communicate with the backend via HTTP requests (in this case, a POST /reviews request).

**BusinessLogic**:  
This layer contains all the business logic of the application, such as validations and decisions, which processes the review data sent by the API.

**Database**:  
The database stores all information about reviews. The business logic interacts with the database to save the review.

### Description of the interaction flow:

### POST /reviews request
The user sends an HTTP POST request to the API to submit a review. This request includes data such as the rating, review text, and user ID.

### Processing in the API
The API receives the request and validates the review data. It checks if all required fields are provided, ensures that the data types are correct (e.g., the rating is a number), and verifies that the user has permission to submit the review.

### Forwarding Data to Business Logic
After the validation, the API sends the review data to the BusinessLogic layer. The API acts as an intermediary and does not handle the processing itself.

### Processing and Saving Data by Business Logic
The BusinessLogic layer processes the review, applying any relevant business rules or additional checks (e.g., verifying if the user has already submitted a review for the same place). Once processed, it sends the data to the database to be saved.

### Backing up Data in the Database
The BusinessLogic layer sends the validated review data to the database for storage. The data includes information such as user ID, review content, and timestamps.

### Database Confirms Save
Once the review data is saved, the database sends a confirmation back to the BusinessLogic layer, indicating that the operation was successful.

### Returning Response to the API
The BusinessLogic layer sends a response to the API, indicating whether the review submission was successful or if there was an issue (e.g., validation failure or database error).

### Returning Response to the User
The API sends a final response back to the user, informing them of the outcome. If successful, the response might be something like "Review submitted successfully"; otherwise, the user may receive an error message.

![API POST reviews](./home/neia/HOLBERTON_PROJECTS/hbnb/API_POST_reviews.jpg)

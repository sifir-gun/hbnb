
# HBnB API Documentation

This documentation provides details for the HBnB API endpoints, organized by entities such as Users, Places, Reviews, and Amenities.

## Base URL

```
http://127.0.0.1:5000/api/v1/
```

## Endpoints

### 1. Users

#### Create a User

- **URL**: `/users/`
- **Method**: `POST`
- **Description**: Creates a new user.
- **Request Body**:
    ```json
    {
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@example.com"
    }
    ```
- **Responses**:
    - `201 Created`: User successfully created.
    - `400 Bad Request`: Email already registered or invalid input data.

#### Get a User by ID

- **URL**: `/users/{user_id}`
- **Method**: `GET`
- **Description**: Retrieves details of a user by ID.
- **Response**:
    - `200 OK`: Returns user details.
    - `404 Not Found`: User not found.

#### Update a User

- **URL**: `/users/{user_id}`
- **Method**: `PUT`
- **Description**: Updates the details of a user by ID.
- **Request Body**:
    ```json
    {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "janedoe@example.com"
    }
    ```
- **Responses**:
    - `200 OK`: User successfully updated.
    - `404 Not Found`: User not found.

#### Delete a User

- **URL**: `/users/{user_id}`
- **Method**: `DELETE`
- **Description**: Deletes a user by ID.
- **Response**:
    - `200 OK`: User successfully deleted.
    - `404 Not Found`: User not found.

### 2. Places

#### Create a Place

- **URL**: `/places/`
- **Method**: `POST`
- **Description**: Creates a new place.
- **Request Body**:
    ```json
    {
        "title": "Beach House",
        "description": "A lovely beach house with sea view.",
        "price": 200.0,
        "latitude": 36.7783,
        "longitude": -119.4179,
        "owner_id": "user_id_here",
        "amenities": ["Wi-Fi", "BBQ"]
    }
    ```
- **Responses**:
    - `201 Created`: Place successfully created.
    - `400 Bad Request`: Invalid input data.

#### Get All Places

- **URL**: `/places/`
- **Method**: `GET`
- **Description**: Retrieves a list of all places.
- **Response**:
    - `200 OK`: Returns list of places.

#### Get a Place by ID

- **URL**: `/places/{place_id}`
- **Method**: `GET`
- **Description**: Retrieves details of a place by ID.
- **Response**:
    - `200 OK`: Returns place details.
    - `404 Not Found`: Place not found.

#### Update a Place

- **URL**: `/places/{place_id}`
- **Method**: `PUT`
- **Description**: Updates the details of a place by ID.
- **Request Body**:
    ```json
    {
        "title": "Updated Beach House",
        "description": "An updated lovely beach house.",
        "price": 250.0
    }
    ```
- **Responses**:
    - `200 OK`: Place successfully updated.
    - `404 Not Found`: Place not found.

#### Delete a Place

- **URL**: `/places/{place_id}`
- **Method**: `DELETE`
- **Description**: Deletes a place by ID.
- **Response**:
    - `200 OK`: Place successfully deleted.
    - `404 Not Found`: Place not found.

### 3. Reviews

#### Create a Review

- **URL**: `/reviews/`
- **Method**: `POST`
- **Description**: Creates a new review for a place.
- **Request Body**:
    ```json
    {
        "text": "Amazing place!",
        "rating": 5,
        "user_id": "user_id_here",
        "place_id": "place_id_here"
    }
    ```
- **Responses**:
    - `201 Created`: Review successfully created.
    - `400 Bad Request`: Invalid input data.

#### Get All Reviews

- **URL**: `/reviews/`
- **Method**: `GET`
- **Description**: Retrieves a list of all reviews.
- **Response**:
    - `200 OK`: Returns list of reviews.

#### Get a Review by ID

- **URL**: `/reviews/{review_id}`
- **Method**: `GET`
- **Description**: Retrieves details of a review by ID.
- **Response**:
    - `200 OK`: Returns review details.
    - `404 Not Found`: Review not found.

#### Update a Review

- **URL**: `/reviews/{review_id}`
- **Method**: `PUT`
- **Description**: Updates the details of a review by ID.
- **Request Body**:
    ```json
    {
        "text": "Updated review text",
        "rating": 4
    }
    ```
- **Responses**:
    - `200 OK`: Review successfully updated.
    - `404 Not Found`: Review not found.

#### Delete a Review

- **URL**: `/reviews/{review_id}`
- **Method**: `DELETE`
- **Description**: Deletes a review by ID.
- **Response**:
    - `200 OK`: Review successfully deleted.
    - `404 Not Found`: Review not found.

### 4. Amenities

#### Create an Amenity

- **URL**: `/amenities/`
- **Method**: `POST`
- **Description**: Creates a new amenity.
- **Request Body**:
    ```json
    {
        "name": "Wi-Fi"
    }
    ```
- **Responses**:
    - `201 Created`: Amenity successfully created.
    - `400 Bad Request`: Invalid input data.

#### Get All Amenities

- **URL**: `/amenities/`
- **Method**: `GET`
- **Description**: Retrieves a list of all amenities.
- **Response**:
    - `200 OK`: Returns list of amenities.

#### Get an Amenity by ID

- **URL**: `/amenities/{amenity_id}`
- **Method**: `GET`
- **Description**: Retrieves details of an amenity by ID.
- **Response**:
    - `200 OK`: Returns amenity details.
    - `404 Not Found`: Amenity not found.

#### Update an Amenity

- **URL**: `/amenities/{amenity_id}`
- **Method**: `PUT`
- **Description**: Updates the details of an amenity by ID.
- **Request Body**:
    ```json
    {
        "name": "Updated Wi-Fi"
    }
    ```
- **Responses**:
    - `200 OK`: Amenity successfully updated.
    - `404 Not Found`: Amenity not found.

#### Delete an Amenity

- **URL**: `/amenities/{amenity_id}`
- **Method**: `DELETE`
- **Description**: Deletes an amenity by ID.
- **Response**:
    - `200 OK`: Amenity successfully deleted.
    - `404 Not Found`: Amenity not found.

---

**Note**: All responses are in JSON format.
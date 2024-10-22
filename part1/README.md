
# **HBnB Project**

Welcome to the **HBnB Project**, a simplified version of a vacation rental platform inspired by Airbnb. This project focuses on developing the key functionalities of such platforms, helping you explore how similar applications are built and understand the architecture behind them.

## **Table of Contents**

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Project Architecture](#project-architecture)
4. [API Workflow](#api-workflow)
    - [User Registration](#user-registration)
    - [Place Creation](#place-creation)
    - [Review Submission](#review-submission)
    - [Fetching Places](#fetching-places)
5. [How to Run the Project](#how-to-run-the-project)
6. [Contributing](#contributing)
7. [License](#license)

## **Project Overview**

The **HBnB Project** is a web-based platform that replicates the core functionality of a vacation rental service. Users can:

- Register and create accounts.
- List properties (places) for rent.
- Submit and manage reviews for places they've stayed at.
- Search for and browse through available rental places based on specific filters.

This project is designed with a modular approach, separating different components to ensure scalability and ease of maintenance, with a focus on user management, property management, and review submissions.

## **Features**

- **User Management**: Allows users to register, update profiles, and manage account roles (regular users, admins).
- **Place Management**: Property owners can list places with details such as name, description, price, and location. The system also supports listing amenities like Wi-Fi, parking, etc.
- **Review System**: Users can submit reviews for rented places, rate them, and share comments.
- **Amenity Management**: Provides functionality for managing property amenities like internet, pool, etc.

## **Project Architecture**

The architecture of the HBnB platform is organized into three main layers, following a **Layered Architecture Pattern**:

1. **Presentation Layer**: Contains the API endpoints and services that handle user interaction and input.
2. **Business Logic Layer**: Contains the core logic that processes user requests, handles validation, and applies business rules.
3. **Persistence Layer**: Responsible for managing database operations, including data storage, retrieval, and updates.

These layers are connected using the **Facade Pattern**, ensuring a clean separation of concerns while facilitating communication between the layers.

## **API Workflow**

This section outlines the workflows for key API operations:

### **User Registration**

1. User sends a `POST` request to `/register` with necessary details (e.g., email, password).
2. The API forwards the request to the Business Logic Layer for validation.
3. After successful validation, the user details are saved to the database.
4. A confirmation is returned to the user.

### **Place Creation**

1. User sends a `POST` request to `/places` with property details (e.g., name, price, description).
2. The API processes and validates the request.
3. Upon successful validation, the property is stored in the database.
4. The system responds with a success message.

### **Review Submission**

1. User sends a `POST` request to `/reviews` with review content and rating.
2. The API validates the review data.
3. The validated review is saved to the database, and a confirmation is sent back to the user.

### **Fetching Places**

1. User sends a `GET` request to `/places` with optional filters (e.g., price, location).
2. The API queries the database for matching places.
3. The list of places is returned as a response.

## **How to Run the Project**

To run the HBnB project locally, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/HBnB.git
   ```

2. **Set up the database**:

   ```bash
   python manage.py migrate
   ```

3. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

## **Contributing**

Contributions are welcome! Here's how you can get involved:

1. **Fork the repository** to your GitHub account.
2. **Create a new feature branch**:

   ```bash
   git checkout -b feature/new-feature
   ```

3. **Make your changes** and commit them:

   ```bash
   git commit -m "Add new feature"
   ```

4. **Push your changes** to your feature branch:

   ```bash
   git push origin feature/new-feature
   ```

5. **Submit a pull request** for review.

Please make sure to follow the project's coding guidelines and style recommendations.

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for more details.


# HBnB Project

Welcome to the **HBnB Project**, a simplified version of a vacation rental platform inspired by Airbnb. This project is designed to help you understand the core functionalities of such platforms while giving you the opportunity to explore how similar applications are built.

## Table of Contents

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

## Project Overview

The **HBnB Project** is a web-based platform where users can:

- Register and create accounts.
- List properties (places) for rent.
- Leave reviews for places they've stayed at.
- Browse through available rentals.

It focuses on delivering a seamless user experience for both property owners and renters, making it easier to manage bookings, reviews, and property listings.

## Features

- **User Management**: Register, update profiles, and manage user roles (e.g., regular users, admins).
- **Place Management**: List properties with details like name, description, price, and location.
- **Review System**: Submit reviews for listed places, including ratings and comments.
- **Amenity Management**: Handle amenities for each place (e.g., Wi-Fi, parking, pool).

## Project Architecture

The HBnB platform is built with a modular architecture, dividing the system into three main layers:

1. **Presentation Layer**: The API and services through which users interact with the system.
2. **Business Logic Layer**: The core logic and rules of the application, handling requests, validation, and processing.
3. **Persistence Layer**: Responsible for storing and retrieving data from the database.

## API Workflow

Here’s how the key workflows are implemented in the platform:

### User Registration

1. User sends a `POST` request to `/register`.
2. The API forwards the request to the Business Logic for validation.
3. The system validates the input (e.g., email, password).
4. The validated data is saved to the database, and a confirmation is returned to the user.

### Place Creation

1. User sends a `POST` request to `/places` with property details.
2. The API forwards the data for validation.
3. Once validated, the property is saved in the database.
4. A success response is sent back to the user.

### Review Submission

1. User sends a `POST` request to `/reviews` with review details.
2. The API validates the review (e.g., rating, content).
3. The review is stored in the database, and a confirmation is sent back.

### Fetching Places

1. User sends a `GET` request to `/places` with optional filters (e.g., location, price).
2. The system processes the filters and queries the database.
3. A list of matching places is returned in response to the user.

## How to Run the Project

To run the HBnB project locally:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/HBnB.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:

   ```bash
   python manage.py migrate
   ```

4. Start the development server:

   ```bash
   python manage.py runserver
   ```

## Contributing

Contributions are welcome! To get involved:

1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Submit a pull request.

Please make sure to follow the project’s coding standards and guidelines when contributing.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

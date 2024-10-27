# HBnB - Location Management Platform

![Python Version](https://img.shields.io/badge/python-3.12.2-blue.svg)
![Flask Version](https://img.shields.io/badge/flask-3.0.0-green.svg)
![Flask-restx Version](https://img.shields.io/badge/flask-restx-1.3.0-red.svg)
![Status](https://img.shields.io/badge/status-development-yellow.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technical Stack](#technical-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [API Documentation](#api-documentation)
- [Development Team](#development-team)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

HBnB is an advanced property rental management platform inspired by Airbnb. It provides a robust backend API for managing properties, user accounts, reviews, and amenities. The platform is built with scalability and maintainability in mind, following clean architecture principles and modern development practices.

## ✨ Features

- **User Management**
  - User registration and profile management
  - Authentication and authorization
  - Admin and regular user roles

- **Property Management**
  - Property listing creation and management
  - Detailed property information (location, price, amenities)
  - Geographic coordinate support

- **Review System**
  - Property review submission
  - Rating system
  - Review management

- **Amenity Management**
  - Customizable amenity listings
  - Property-amenity associations

## 🏗 Architecture

The application follows a layered architecture pattern:

1. **Presentation Layer** (API)
   - RESTful endpoints using Flask-RESTx
   - Request validation and response formatting
   - API documentation with Swagger UI

2. **Service Layer**
   - Business logic implementation
   - Facade pattern for simplified interface
   - Data validation and processing

3. **Persistence Layer**
   - Data storage and retrieval
   - Repository pattern implementation
   - In-memory storage (expandable to other storage solutions)

## 🛠 Technical Stack

- **Framework**: Flask 3.0.0
- **API Documentation**: Flask-RESTx 1.3.0
- **Security**: bcrypt 3.2.0
- **Development Tools**:
  - Python 3.12.2
  - Git for version control

## 📁 Project Structure

```
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py
├── run.py
├── config.py
├── requirements.txt
├── README.md
```

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/sifir-gun/hbnb.git
cd hbnb
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the application:
```bash
python run.py
```

The API will be available at `http://localhost:5000`

## 📚 API Documentation

Once the application is running, you can access the Swagger UI documentation at:
`http://localhost:5000/`

Available endpoints:
- `/api/v1/users` - User management
- `/api/v1/places` - Property management
- `/api/v1/reviews` - Review management
- `/api/v1/amenities` - Amenity management

## 👥 Development Team

- **Guney TASDELEN** - Backend Development & Architecture
- **Xavier PIEDALLU** - API Development & Documentation
- **Neia SANTOS** - Data Models & Business Logic

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Developed with ❤️ by Guney, Xavier, and Neia.

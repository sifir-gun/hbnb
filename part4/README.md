# 🚀 HBnB Evolution - Part 3: Enhanced Backend with Authentication and Database Integration

---

## 📋 Table of Contents

- [🚀 HBnB Evolution - Part 3: Enhanced Backend with Authentication and Database Integration](#-hbnb-evolution---part-3-enhanced-backend-with-authentication-and-database-integration)
	- [📋 Table of Contents](#-table-of-contents)
	- [📖 Introduction](#-introduction)
	- [🌟 New Features in Part 3](#-new-features-in-part-3)
		- [🔐 Authentication and Authorization](#-authentication-and-authorization)
		- [🗃️ Persistent Storage](#️-persistent-storage)
		- [🛡️ Enhanced Data Models](#️-enhanced-data-models)
		- [🌐 Secure API Endpoints](#-secure-api-endpoints)
	- [🏗️ Architecture and Design](#️-architecture-and-design)
		- [📂 High-Level Package Diagram](#-high-level-package-diagram)
		- [🧩 Business Logic Layer Class Diagram](#-business-logic-layer-class-diagram)
		- [🔄 Sequence Diagrams for API Calls](#-sequence-diagrams-for-api-calls)
	- [🛠️ Usage](#️-usage)
		- [🛑 Prerequisites](#-prerequisites)
		- [▶️ Steps to Run](#️-steps-to-run)
	- [🤝 Acknowledgments](#-acknowledgments)

---

## 📖 Introduction

Welcome to **Part 3** of the HBnB Evolution project! 🎉 This phase focuses on transitioning the backend from prototype to a robust and scalable system by introducing authentication, persistent database storage, and enhanced CRUD operations.

---

## 🌟 New Features in Part 3

### 🔐 Authentication and Authorization
- **JWT Authentication**: Secure user sessions with JSON Web Tokens (JWT).
- **Role-Based Access**: Admins have unrestricted access, while regular users are limited to their own resources.

### 🗃️ Persistent Storage
- **SQLite Integration**: Transitioned from in-memory storage to SQLite for development.
- **SQLAlchemy CRUD Operations**: Refactored to handle persistent data effectively.

### 🛡️ Enhanced Data Models
- Refined entity models (`User`, `Place`, `Review`, `Amenity`) with SQLAlchemy database mappings.
- Enforced relationships between entities for data consistency and integrity.

### 🌐 Secure API Endpoints
- Authenticated endpoints for creating, updating, and deleting resources.
- Public endpoints remain accessible without authentication for general queries.

---

## 🏗️ Architecture and Design

### 📂 High-Level Package Diagram

The application follows a **three-layer architecture**:

1. **Presentation Layer**: Handles user interaction through APIs.
2. **Business Logic Layer**: Contains core application logic and models.
3. **Persistence Layer**: Manages data storage and retrieval with SQLAlchemy.

---

### 🧩 Business Logic Layer Class Diagram

The class diagram includes the following key entities:
- **User**: Attributes such as `email`, `password_hash`, and `is_admin`.
- **Place**: Attributes such as `name`, `description`, and associated amenities.
- **Review**: User ratings and comments for places.
- **Amenity**: Features that enhance a place.

---

### 🔄 Sequence Diagrams for API Calls

Here are the main API interaction flows in this phase:
1. **User Registration**: Securely register a new user with password hashing.
2. **Place Creation**: Authenticated users can add new listings.
3. **Review Submission**: Users can leave reviews with validation.
4. **Fetching Places**: Retrieve a list of places based on filters.

---

## 🛠️ Usage

To explore the features of Part 3:

### 🛑 Prerequisites
- Python 3.10+
- SQLite installed
- Flask and SQLAlchemy dependencies (`pip install -r requirements.txt`)

### ▶️ Steps to Run
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/hbnb-evolution.git
   cd hbnb-evolution/part3
   ```
2. **Set Up Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   flask run
   ```

4. **Test Endpoints**:
   - Use tools like `Postman` or `cURL` to test APIs.

---

## 🤝 Acknowledgments

A big thanks to our team and mentors for their guidance and support throughout this phase of the project. Your contributions made this possible! 🌟

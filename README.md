# HBnB Evolution - Technical Documentation

## Table of Contents

- [Introduction](#introduction)
- [Project Overview](#project-overview)
- [Architecture and Design](#architecture-and-design)
  - [High-Level Package Diagram](#high-level-package-diagram)
  - [Business Logic Layer Class Diagram](#business-logic-layer-class-diagram)
  - [Sequence Diagrams for API Calls](#sequence-diagrams-for-api-calls)
- [Documentation Compilation](#documentation-compilation)
- [Team Members](#team-members)
- [Usage](#usage)
- [Acknowledgments](#acknowledgments)

---

## Introduction

Welcome to the **HBnB Evolution** project! This repository contains the comprehensive technical documentation for the development of the HBnB application, a simplified version of an Airbnb-like platform. This documentation serves as the foundation for the project's implementation phases, providing clear insights into the application's architecture, design, and interaction flows.

---

## Project Overview

**HBnB Evolution** is a web application that allows users to:

- **User Management**: Register, update profiles, and be identified as regular users or administrators.
- **Place Management**: List properties with details such as name, description, price, and location, along with associated amenities.
- **Review Management**: Leave reviews for places, including ratings and comments.
- **Amenity Management**: Manage amenities that can be associated with places.

The project follows a layered architecture divided into:

- **Presentation Layer**: Services and APIs for user interaction.
- **Business Logic Layer**: Core logic and models of the application.
- **Persistence Layer**: Data storage and retrieval from the database.

---

## Architecture and Design

### High-Level Package Diagram

The high-level package diagram illustrates the three-layer architecture of the HBnB application and the communication between these layers via the facade pattern. It provides a conceptual overview of how the components are organized and interact.

- **Presentation Layer**: Handles user interactions, including services and API endpoints.
- **Business Logic Layer**: Contains core business logic and models (User, Place, Review, Amenity).
- **Persistence Layer**: Responsible for data storage and retrieval, interacting with the database.

**[View High-Level Package Diagram](Documentation_Compilation.md#high-level-package-diagram)**

### Business Logic Layer Class Diagram

The detailed class diagram represents the internal structure of the Business Logic layer, focusing on the key entities: User, Place, Review, and Amenity. It includes their attributes, methods, and relationships such as associations, inheritance, and dependencies.

**[View Class Diagram and Explanation](Documentation_Compilation.md#business-logic-layer-class-diagram-explanation)**

### Sequence Diagrams for API Calls

Sequence diagrams have been developed for four different API calls to illustrate the interaction between the layers and the flow of information within the application:

1. **User Registration**: A user signs up for a new account.
2. **Place Creation**: A user creates a new place listing.
3. **Review Submission**: A user submits a review for a place.
4. **Fetching a List of Places**: A user requests a list of places based on certain criteria.

These diagrams help visualize how different components interact to fulfill specific use cases, showing the step-by-step process of handling API requests.

**[View Sequence Diagrams](Documentation_Compilation.md#api-interaction-flow-sequence-diagram-for-user-registration)**

---

## Documentation Compilation

All diagrams and explanatory notes have been compiled into a comprehensive technical document. This document serves as a detailed blueprint for the HBnB project, guiding the implementation phases and providing a clear reference for the system’s architecture and design.

**[Access the Full Documentation](Documentation_Compilation.md)**

---

## Team Members

This project is a collaborative effort by:

- **Guney TASDELEN**
- **Xavier PIEDALLU**
- **Neia SANTOS**

---

## Usage

Since this phase of the project focuses on technical documentation, there is currently no executable code in the repository. To utilize the documentation:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/hbnb-evolution.git
   ```
2. **Navigate to the Documentation**:
   - Open `Documentation_Compilation.md` to access all diagrams and explanations.
   - Diagrams are available in image format within the document for easy reference.

3. **Review the Diagrams**:
   - Use the high-level package diagram to understand the overall architecture.
   - Study the class diagrams to grasp the structure of the business logic layer.
   - Examine the sequence diagrams to follow the interaction flows for various API calls.

---

## Acknowledgments

We would like to thank our institution and mentors for providing the guidance and resources necessary to complete this phase of the HBnB Evolution project. The collaborative effort and collective learning have been invaluable.

---

**Note**: This README will be updated in future phases to include implementation details, setup instructions, and usage examples as the project progresses into development stages.
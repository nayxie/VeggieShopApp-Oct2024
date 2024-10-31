# Veggie Shop Management System

This project marks my first independent development of a full-stack web application, completed over 4 weeks in October 2024. Developed as the final assessment for the COMP642 Advanced Programming course at Lincoln University, the application implements a `Domain-Driven Design` approach, integrating domain models, database models, routers, services, and utilities.

The technology stack includes `Python with Flask`, `SQLAlchemy`, `Jinja templating`, `HTML`, `Bootstrap`, `CSS`, `JavaScript`, and `MySQL`, with `Pytest` used for testing. This stack enabled the creation of a responsive and maintainable application that manages core functionalities of a vegetable shop.

**Test accounts:** 
- customer: moe_m (pw:123456)
- corporate customer: doe_m (pw:123456)
- staff: steve_j (pw:123456)

## :rocket: Layered Architectural Design

The application follows a `layered architectural design`. Each layer is separated according to best practices, making the architecture clean, modular, and easy to maintain. 

<img width="507" alt="Screenshot 2024-10-31 at 15 53 04" src="https://github.com/user-attachments/assets/10273f29-b768-4a21-8994-968a4146f963">

**Database Layer**
- Technology: MySQL
- Role: Handles data storage, retrieval, and management.

**Persistence Layer**
- Technology: SQLAlchemy ORM models
- Role: Provides an object-relational mapping that aligns closely with the domain models. Facilitates data interactions between the business layer and the database.

**Business Layer**
- Technology: Domain Models
- Role: Encapsulates core business logic and rules specific to the veggie shop, modelling key entities with attributes and methods within the application.

**Application Layer**
- Technology: Flask Routers with Python
- Role: Handles application routing, request processing, data validation, and delegation of business logic execution. Acts as a bridge between the presentation layer and business layer to manage user requests and responses.

**Presentation Layer**
- Technology: Bootstrap, HTML, CSS, JavaScript
- Role: Manages the user interface, providing an interactive and responsive experience to end-users.

## :star: Functionalities

**Customer Features**
- Authentication: Log in and log out of their account securely.
- Product Viewing: Browse available vegetables and premade boxes.
- Order Placement: Place orders for individual vegetables or premade boxes.At checkout, customers can pay using a credit card, debit card, or charge the amount to their account.
- Order Management: View current and previous order details. Cancel an order if it has not yet been fulfilled.
- Account Management: View their own personal account details.

**Staff Features**
- Authentication: Log in and log out of their account securely.
- Product Viewing: Access details of all vegetables and premade boxes.
- Order Management: View all current and previous orders and their details. Update the status of orders as they progress.
- Customer Management: Access details of all customers. Generate a list of all customers in the system.
- Sales Reporting:Generate reports on total sales for the week, month, and year.
- Product Insights: View the most popular items based on sales and customer demand.

## :key: Data Modelling

<img width="769" alt="Screenshot 2024-10-31 at 16 21 15" src="https://github.com/user-attachments/assets/fc8d74db-b726-452b-8f13-fb23fc153f57">

## :dragon_face: UI Screenshots

<img width="894" alt="Screenshot 2024-10-31 at 16 07 58" src="https://github.com/user-attachments/assets/c05ad3a7-f612-4a8c-a19f-8108c0c56537">
<img width="894" alt="Screenshot 2024-10-31 at 16 09 10" src="https://github.com/user-attachments/assets/0d300f4c-163c-42a1-9343-98fafc5d1ad9">
<img width="894" alt="Screenshot 2024-10-31 at 16 11 13" src="https://github.com/user-attachments/assets/0c5a1f29-c543-4809-91f2-04509b17ea2b">
<img width="894" alt="Screenshot 2024-10-31 at 16 12 05" src="https://github.com/user-attachments/assets/e0383370-16fa-453a-aba3-c868f879078b">
<img width="894" alt="Screenshot 2024-10-31 at 16 13 36" src="https://github.com/user-attachments/assets/735eac4e-8b70-428c-b054-a516803efc21">
<img width="894" alt="Screenshot 2024-10-31 at 16 14 21" src="https://github.com/user-attachments/assets/570a4145-8d03-4098-bb4d-cdbd67fbe40d">







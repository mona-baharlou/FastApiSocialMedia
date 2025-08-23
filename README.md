#  FastAPI Social Media API

A **social media backend API** built with **FastAPI**, featuring secure authentication, user management, posts, and voting. The project follows clean architecture principles, uses database migrations, and leverages modern Python tools for scalability and security.

##  Features

*  **Authentication & Authorization**

  * Secure login with **OAuth2PasswordBearer**
  * **JWT tokens** for session management
  * Password hashing using **bcrypt**
  * JWT validation and error handling with `JWTError`

* **Database & Migrations**

  * PostgreSQL with **SQLAlchemy ORM**
  * Schema migrations with **Alembic**
  * Dependency injection with `Depends`

* **Core Functionality**

  * **Users**: register, authenticate, and manage accounts
  * **Posts**: create, read, update, delete (CRUD)
  * **Votes**: upvote/downvote posts (many-to-many relation)
  * **Timestamps & Ownership** tracking

* **Modular Design**

  * Separate **routers** for authentication, users, posts, and votes


##  Tech Stack

* **Framework**: FastAPI
* **Database**: PostgreSQL + SQLAlchemy
* **Migrations**: Alembic
* **Authentication**: OAuth2 + JWT + bcrypt
* **Dependency Injection**: FastAPI `Depends`
* **Routing**: Modular Routers

##  What I Learned

Building this project improved my understanding of:

* **FastAPI Fundamentals** – routers, dependency injection, Pydantic schemas
* **Database Management** – SQLAlchemy ORM + Alembic migrations
* **Authentication & Security** – JWT, bcrypt, OAuth2 flows
* **API Design** – modular structure with separate routers for scalability
* **Error Handling** – JWT errors, authentication issues, request validation
* **Production-Ready Skills** – handling migrations without data loss

---

##  API Endpoints

* **Users**

  * `POST /users` – create user
  * `GET /users/{id}` – get user by ID
* **Auth**
  
  * `POST /login` – login & receive JWT token   
* **Posts**

  * `GET /posts` – list posts
  * `POST /posts` – create a new post
  * `PUT /posts/{id}` – update post
  * `DELETE /posts/{id}` – delete post
* **Votes**

  * `POST /vote` – upvote or remove vote from a post

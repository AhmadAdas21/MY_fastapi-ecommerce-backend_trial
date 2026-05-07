My project is an E-commerce Backend API built using FastAPI. It provides backend services for managing products, categories, users, shopping cart, and orders. The project supports full CRUD operations for products and categories, with search, price filtering, and pagination for the products section.

The API includes user registration and login using JWT authentication, password hashing, and role-based authorization. Normal users can browse products, add items to the cart, and create orders through the checkout process. Admin users can manage products, categories, users, product images, and order statuses.

The project is organized using routers, schemas, models, and utility files to keep the code clean and maintainable. It also uses SQLAlchemy with a SQLite database, includes product image upload, automatic API documentation through Swagger, and basic automated tests using Pytest.

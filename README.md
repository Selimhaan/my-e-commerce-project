E-Commerce Web Application

This is a fully functional e-commerce web application built with Django. The project provides features like product listing, product details, cart management, and user authentication, making it a comprehensive solution for small to medium-scale online stores.

Features

Core Features

Product Listing: View all available products with details like name, price, and stock.

Product Details: View detailed information about individual products, including images and descriptions.

Add to Cart: Add products to your cart for later checkout.

Cart Management: Adjust product quantities, remove items, or clear the entire cart.

User Authentication

Register: Create a new user account.

Login: Authenticate existing users.

Logout: Securely log out users.

Session-Based Cart:

For unauthenticated users: cart data is stored temporarily.

For authenticated users: cart data is persistent across sessions.

Additional Features

Search Products: Search for products using a keyword.

Responsive Design: The application is mobile-friendly, ensuring a great user experience across devices.

Tech Stack

Backend: Django Framework

Frontend: HTML, CSS (with TailwindCSS)

Database: SQLite (default) or Microsoft SQL Server

Third-Party Libraries:

Font Awesome (for icons)

Django Tailwind (for styling support)

Installation

Follow these steps to set up the project locally:

Prerequisites

Python 3.8+

pip

Virtual Environment (optional but recommended)

Steps

Clone the Repository:

git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name

Create a Virtual Environment (optional):

python -m venv venv
source venv/bin/activate   # For Linux/Mac
venv\Scripts\activate     # For Windows

Install Dependencies:

pip install -r requirements.txt

Apply Migrations:

python manage.py makemigrations
python manage.py migrate

Run the Server:

python manage.py runserver

Access the Application:
Open your browser and visit http://127.0.0.1:8000/.

Usage

Add Products:

Visit the admin panel at /admin to add products.

Ensure products have a name, price, stock, and optionally an image.

Browse Products:

Use the product list page to browse available products.

Click on a product to view its details.

Manage Cart:

Add products to the cart using the "Add to Cart" button.

Adjust quantities or remove items directly from the cart page.

Authentication:

Register or log in to access advanced features like persistent cart data.

Screenshots

screenshots are added to the file array

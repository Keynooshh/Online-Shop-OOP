Online Shop CLI Application
This is a simple Command Line Interface (CLI) application for an online shop. The application allows users to register, log in, view products, add products to their cart, place orders, and manage their orders. The data is stored in a JSON file, which is loaded and saved when the application starts and exits, respectively.

Features
User Registration and Login: Users can register with a unique username and email, and log in to access their account.
Product Management: Users can view a list of available products, see product details, and add products to their cart.
Cart Management: Users can view their cart, remove products from the cart, and place orders.
Order Management: Users can view their orders and cancel them if needed.
Data Persistence: User data, product data, and order data are stored in a JSON file, ensuring data persistence between sessions.
Classes
User
Attributes:
username: The username of the user.
email: The email of the user.
password: The password of the user.
order: The current order of the user.
cart: The current cart of the user.
Methods:
make_dict(): Converts the user object to a dictionary for JSON serialization.
Product
Attributes:
name: The name of the product.
price: The price of the product.
description: The description of the product.
Methods:
update_price(new_price): Updates the price of the product.
update_desc(new_desc): Updates the description of the product.
make_dict(): Converts the product object to a dictionary for JSON serialization.
Cart
Attributes:
user: The user who owns the cart.
products: A list of products in the cart.
Methods:
add_product(product): Adds a product to the cart.
remove_product(product): Removes a product from the cart.
get_total_price(): Calculates the total price of the products in the cart.
make_dict(): Converts the cart object to a dictionary for JSON serialization.
Order
Attributes:
user: The user who placed the order.
products: A list of products in the order.
total_price: The total price of the order.
Methods:
place_order(cart): Places an order by transferring products from the cart to the order.
cancel_order(): Cancels the order and clears the products.
make_dict(): Converts the order object to a dictionary for JSON serialization.
Manager
Attributes:
users: A list of all registered users.
logged_in_user: The currently logged-in user.
products: A list of all available products.
Methods:
find_userbyusername(uname): Finds a user by their username.
find_userbyemail(email): Finds a user by their email.
login(): Handles the user login process.
register(): Handles the user registration process.
logout(): Logs out the currently logged-in user.
Usage
Run the Application: Execute the Python script to start the application.
Login or Register: If you have an account, log in with your username and password. If not, register a new account.
View Products: Browse the list of available products and add them to your cart.
Manage Cart: View your cart, remove products, or place an order.
View Orders: View your placed orders and cancel them if necessary.
Logout: Log out of your account when you’re done.
Data Persistence
All user data, product data, and order data are stored in a JSON file (online_shop.json). This file is loaded when the application starts and saved when the application exits, ensuring that all changes are persisted between sessions.

JSON Structure
The JSON file has the following structure:

{
  "users": [
    {
      "username": "user1",
      "email": "user1@example.com",
      "password": "password1",
      "order": {
        "user": "user1",
        "products": [
          {
            "name": "Product1",
            "price": 100,
            "description": "Description of Product1"
          }
        ],
        "total_price": 100
      },
      "cart": {
        "user": "user1",
        "products": [
          {
            "name": "Product2",
            "price": 200,
            "description": "Description of Product2"
          }
        ]
      }
    }
  ],
  "products": [
    {
      "name": "Product1",
      "price": 100,
      "description": "Description of Product1"
    },
    {
      "name": "Product2",
      "price": 200,
      "description": "Description of Product2"
    }
  ]
}
Running the Application
To run the application, ensure you have Python installed and execute the script:

python online_shop.py
Contributing
Feel free to fork this repository, make changes, and submit pull requests. Any contributions are welcome!

Enjoy shopping with TimTim Online Shop! 🛒

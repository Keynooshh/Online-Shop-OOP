import json

class User:

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.order = None
        self.cart = None

    def make_dict(self):   # Convert to JSON Format
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "order": self.order.make_dict(),
            "cart": self.cart.make_dict()
        }


class Product:

    def __init__(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description

    def update_price(self, new_price):   # Update Price
        self.price = new_price

    def update_desc(self, new_desc):   # Update Description
        self.description = new_desc

    def make_dict(self):   # Convert to JSON Format
        return {
            "name": self.name,
            "price": self.price,
            "description": self.description
        }


class Cart:

    def __init__(self, user: User):
        self.user = user
        self.products = []

    def add_product(self, product):   # Add Product
        self.products.append(product)

    def remove_product(self, product):   # Remove Product
        self.products.remove(product)

    def get_total_price(self):   # Calculate Total
        total_price = 0
        for p in self.products:
            total_price = total_price + p.price
        return total_price

    def make_dict(self):
        return {
            "user": self.user.username,
            "products": [p.make_dict() for p in self.products]
        }


class Order:

    def __init__(self, user):
        self.user = user
        self.products = []
        self.total_price = 0

    def place_order(self, cart: Cart):   # Placing Order Process
        self.total_price = cart.get_total_price() + self.total_price   # Price Total
        self.products.extend(cart.products)   # Add
        cart.products.clear()   # Emptying the Cart

    def cancel_order(self):   # Removing Order Process
        self.products.clear()
        self.total_price = 0

    def make_dict(self):
        return {
            "user": self.user.username,
            "products": [p.make_dict() for p in self.products],
            "total_price": self.total_price
        }


class Manager:
    users: list[User] = []   # User Instances
    logged_in_user: User = None   # Checking Access Privilege 
    products = []

    @staticmethod
    def find_userbyusername(uname):    # Find By UserName
        for u in Manager.users:
            if u.username == uname:
                return u
        return None

    @staticmethod
    def find_userbyemail(email):   # Find by Email
        for i in Manager.users:
            if i.email == email:
                return i
        return None

    @staticmethod
    def login():   # Logging In Process
        username = input("please input your username:")    # User Input
        u = Manager.find_userbyusername(username)   # Checking For UserName in DB
        counter = 0
        while u is None:
            username = input("username wasn't found please try again:")
            u = Manager.find_userbyusername(username)
            counter += 1
            if counter == 3:
                return
        password = input("please enter your password:")
        while password != u.password:
            password = input("incorrect password please try again:")
        Manager.logged_in_user = u

    @staticmethod
    def register():   # Adding New Users 
        username = input("please choose an username:")   # Checking In For Duplications
        while Manager.find_userbyusername(username) is not None:
            username = input("this username is taken please choose another one:")
        email = input("please enter your email:")
        while Manager.find_userbyemail(email) is not None:
            email = input("this email is taken please choose another one:")
        u = User(username, email, input("please choose your password:"))
        Manager.users.append(u)   # Add New User
        Manager.logged_in_user = u

    @staticmethod
    def logout():   # Log Out 
        Manager.logged_in_user = None


with open(r"C:\Users\keyno\OneDrive\Documents\py projects\online_shop\online_shop.json", "r") as load_file:   # Loading JSON File
    data = json.load(load_file)
    products_list = data["products"]   # Ungrouping Loaded Data
    users_list = data["users"]

    for prod_dict in products_list:   # Loading Data From DB
        product = Product(prod_dict["name"], prod_dict['price'], prod_dict['description'])
        Manager.products.append(product)

    for user_dict in users_list:
        user = User(user_dict["username"], user_dict['email'], user_dict['password'])

        # USER ORDER
        order_dict = user_dict["order"]
        order_products_dict_list = order_dict["products"]
        # By the Structure, Orders are Built-in Users as a Sub-Tree 
        # To Load Orders, First We load users
        order_products = []   
        for prod_dict in order_products_dict_list:
            product = Product(prod_dict["name"], prod_dict['price'], prod_dict['description'])
            order_products.append(product)

        user.order = Order(user)   # Adding Order by Submitting order
        user.order.products = order_products
        user.order.total_price = order_dict["total_price"]

        # USER CART
        cart_dict = user_dict["cart"]
        cart_products_dict_list = cart_dict["products"]

        cart_products = []
        for prod_dict in cart_products_dict_list:
            product = Product(prod_dict["name"], prod_dict['price'], prod_dict['description'])
            cart_products.append(product)

        user.cart = Cart(user)
        user.cart.products = cart_products

        Manager.users.append(user)

while True:   # CLI Initiator 
    print("Hello, welcome to TimTim online shop")
    entered_minus1 = False   # Level Control  // Logout..Exit

    while Manager.logged_in_user is None:   # Logging Process
        has_account = input("Do you have an account?\nenter Y/N:").upper().strip()

        if has_account == "Y":
            Manager.login()
        elif has_account == "N":
            Manager.register()
        elif has_account == "-1":
            entered_minus1 = True
            break

    if entered_minus1: break   # Exit

    print("successfully we logged in")   # Loading data 
    cart = Manager.logged_in_user.cart if Manager.logged_in_user.cart is not None else Cart(Manager.logged_in_user)
    order = Manager.logged_in_user.order if Manager.logged_in_user.order is not None else Order(Manager.logged_in_user)
    user_input = int(
        input("1)view products\n2)view your cart\n3)view your orders\n-1)logout\nplease choose a number:").strip())

    while user_input != -1:
        if user_input == 1:   # View Products
            x = 1   # Sequence Number
            for i in Manager.products:
                print(x, ")", i.name, sep="")
                x = x + 1
            chosen_product_num = int(input("please choose product number:"))   # User CLI Interactions
            while not (1 <= chosen_product_num <= len(Manager.products)):
                chosen_product_num = int(input("please choose valid product number:"))
            chosen_product = Manager.products[chosen_product_num - 1]
            print(chosen_product.name, str(chosen_product.price) + " Toman", chosen_product.description, sep="\n")
            decision = input("\nwould you like to add this to your cart?(Y/N):").upper().strip()
            while decision != "Y" and decision != "N":
                decision = input("would you like to add this to your cart?(Y/N):").upper().strip()
            if decision == 'Y':
                cart.add_product(chosen_product)
                print()
                print("the", chosen_product.name, "is in your cart!\n\nanything else you want to do?")
        elif user_input == 2:   # View Cart
            if cart.products:
                x = 1   # Sequence Number
                for i in cart.products:
                    print(x, ")", i.name, str(i.price) + " Toman")
                    x = x + 1
                print("------------------\nyour total is", cart.get_total_price(), "Toman")
                decision = int(input(
                    "\n1)would you like to remove a product from your cart\n2)place order\nplease choose a number:").strip())
                if decision == 1:
                    chosen_product_num = int(input("which product you would like to remove:"))
                    while not (1 <= chosen_product_num <= len(cart.products)):
                        chosen_product_num = int(input("please choose valid product number:"))
                    chosen_product = cart.products[chosen_product_num - 1]
                    cart.remove_product(chosen_product)
                    print()
                    print(chosen_product.name, "has been removed from your cart successfully\n")
                elif decision == 2:
                    order.place_order(cart)
                    print("\nyour cart has been emptied and you have your order placed!\n")
            else:
                print("\nyour cart is empty!\n")
        elif user_input == 3:   # View Order
            if order.products:
                print("your order is:")
                x = 1
                for i in order.products:
                    print(x, ")", i.name, str(i.price) + " Toman")
                    x = x + 1
                print("------------------\nyour total is", order.total_price, "Toman\n")
                cancel_decision = input("do you want to cancel the order?(Y/N):").upper().strip()
                if cancel_decision == "Y":
                    order.cancel_order()
                    print("\nyour order has been canceled and your money would be back in your account by 72hrs!")

            else:
                print("\nyou have not placed an order!\n")

        user_input = int(
            input("1)view products\n2)view your cart\n3)view your orders\n-1)logout\nplease choose a number:").strip())

    Manager.logged_in_user.order = order
    Manager.logged_in_user.cart = cart
    Manager.logout()
    print("-------------------------------------------")
    print("[-1 to EXIT program]")

data = {   # Instances
    "users": [],
    "products": []
}

# JSON Export/Dump data 
for user_obj in Manager.users:
    data["users"].append(user_obj.make_dict())

for prod_obj in Manager.products:
    data["products"].append(prod_obj.make_dict())
    
with open(r"C:\Users\keyno\OneDrive\Documents\py projects\online_shop\online_shop.json", "w") as save_file:
    json.dump(data, save_file, indent=4)
    

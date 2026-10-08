#************************************************
# RESTAURANT MANAGEMENT SYSTEM (24_DHOROU RESTAURANT)
# GROUP 7 MEMBERS

# 1. AJAK DENG GARANG M25B38/031
# 2. BULIMA EEKIEL M25B38/028
# 3. APONI ALLAN DANIEL M25B38/029
# 4. AYOO ALICE  S25B38/026
# 5. AGENORWOT CYNTHIA JILLIAN S25B38/034
# 6. AYEBAZIBWE TRAVIS   S24B38/007

#************************************************



from abc import ABC, abstractmethod  # Import tools for creating an abstract class.
from datetime import datetime  # Import datetime to record order creation time.


# ABSTRACT MENU ITEM CLASS


class MenuItem(ABC):  # Parent class for all menu items.

    def __init__(self, item_code, name, price):
        self.item_code = item_code      # Public attribute
        self.name = name                # Public attribute
        self.__price = price            # Private attribute:  # ENCAPSULATION: controlled access to the private __price.

    
    @property # The property allows the rest of the program to use price safely without directly accessing __price.
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative.")
        self.__price = value

    @abstractmethod
    def calculate_price(self, quantity): # POLYMORPHISM: This method has the same name in the parent class, but each child class provides its own implementation.
        pass

    @abstractmethod
    def prepare(self):
        pass

    def show(self):
        print(f"Code: {self.item_code} | Name: {self.name} | Price: UGX {self.price:,.2f}")






# FOOD ITEM

class FoodItem(MenuItem):  # FoodItem inherits from MenuItem.

    def calculate_price(self, quantity):  # Calculate food price.
        return self.price * quantity  # Food price = price × quantity.

    def prepare(self):  # Describe food preparation.
        return "Prepared in the kitchen."  # Return preparation message.


# DRINK ITEM

class DrinkItem(MenuItem):  # DrinkItem inherits from MenuItem.

    def calculate_price(self, quantity):  # Calculate drink price.
        return self.price * quantity  # Drink price = price × quantity.

    def prepare(self):  # Describe drink preparation.
        return "Prepared at the drinks counter."  # Return preparation message.


# DESSERT ITEM

class DessertItem(MenuItem):  # DessertItem inherits from MenuItem.

    def calculate_price(self, quantity):  # Calculate dessert price.
        base_price = self.price * quantity  # Calculate normal price.
        service_charge = base_price * 0.05  # Add 5% service charge.
        return base_price + service_charge  # Return final dessert price.

    def prepare(self):  # Describe dessert preparation.
        return "Prepared and served as a dessert."  # Return preparation message.


# ORDER ITEM

class OrderItem:  # Represents one item inside an order.

    def __init__(self, menu_item, quantity):
        self.menu_item = menu_item  # Public attribute.
        self.quantity = quantity  # Use the setter so validation is applied.

    @property
    def quantity(self):  
        return self.__quantity

    @quantity.setter
    def quantity(self, value):
        if value <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.__quantity = value

    def calculate_total(self): # POLYMORPHISM: The correct calculate_price() method is selected according to the actual type of menu_item.
        return self.menu_item.calculate_price(self.quantity)

    def show(self, number):
        print(
            f"{number}. {self.menu_item.name} | Quantity: {self.quantity} | "
            f"Total: UGX {self.calculate_total():,.2f}"
        )






# CUSTOMER ORDER CLASS

class Order:  # Represents a customer's order.

    next_order_id = 1  # Starting number for orders.

    def __init__(self):  # Create a new order.
        self.order_id = Order.next_order_id  # Give the order an ID.
        Order.next_order_id += 1  # Increase the next order ID.
        self.items = []  # Create an empty list for order items.

        self.status = "Active"  # Set status through the encapsulated property.

        self.created_at = datetime.now()  # Record the current date and time.

    
    @property
    def status(self): # ENCAPSULATION: provide controlled access to the order status.
        return self.__status

    @status.setter
    def status(self, value): # ENCAPSULATION: only accepted order states are allowed.
        allowed_statuses = ("Active", "Completed", "Cancelled")
        if value not in allowed_statuses:
            raise ValueError("Invalid order status.")
        self.__status = value

    # ADD ITEM

    def add_item(self, menu_item, quantity):  # Add an item to the order.

        if self.status != "Active":  # Check if the order is still active.
            print("Only active orders can be changed.")  # Show an error.
            return False  # Stop the operation.

        if quantity <= 0:  # Check if quantity is invalid.
            print("Quantity must be greater than zero.")  # Show an error.
            return False  # Tell the program the operation failed.

        for item in self.items:  # Check existing order items.
            if item.menu_item.item_code == menu_item.item_code:  # Check if the item already exists.
                item.quantity += quantity  # Increase its quantity.
                return True  # Tell the program the item was added.

        new_item = OrderItem(menu_item, quantity)  # Create a new order item.
        self.items.append(new_item)  # Add the new item to the order.
        return True  # Tell the program the operation was successful.

    
    # CHANGE QUANTITY

    def change_quantity(self, item_number, new_quantity):  # Change an item's quantity.

        if self.status != "Active":  # Check if the order is still active.
            print("Only active orders can be changed.")  # Show an error.
            return False  # Stop the operation.

        if new_quantity <= 0:  # Check if the new quantity is valid.
            print("Quantity must be greater than zero.")  # Show an error.
            return False  # Stop the operation.

        if item_number < 1 or item_number > len(self.items):  # Check the item number.
            print("Invalid item number.")  # Show an error.
            return False  # Stop the operation.

        self.items[item_number - 1].quantity = new_quantity  # Change the quantity.
        return True  # Tell the program the operation succeeded.

    
    # REPLACE ITEM

    def replace_item(self, item_number, new_menu_item):  # Replace an ordered item.

        if self.status != "Active":  # Check if the order is still active.
            print("Only active orders can be changed.")  # Show an error.
            return False  # Stop the operation.

        if item_number < 1 or item_number > len(self.items):  # Check the item number.
            print("Invalid item number.")  # Show an error.
            return False  # Stop the operation.

        old_item = self.items[item_number - 1]  # Get the old item.
        old_quantity = old_item.quantity  # Keep the old quantity.

        for index, item in enumerate(self.items):  # Check other items in the order.
            if index != item_number - 1 and item.menu_item.item_code == new_menu_item.item_code:  # Check for duplicate item.
                item.quantity += old_quantity  # Combine the quantities.
                self.items.pop(item_number - 1)  # Remove the old item.
                return True  # Finish the replacement.

        old_item.menu_item = new_menu_item  # Replace the menu item.
        return True  # Tell the program the operation succeeded.


    # REMOVE ITEM

    def remove_item(self, item_number):  # Remove an item from the order.

        if self.status != "Active":  # Check if the order is still active.
            print("Only active orders can be changed.")  # Show an error.
            return False  # Stop the operation.

        if item_number < 1 or item_number > len(self.items):  # Check the item number.
            print("Invalid item number.")  # Show an error.
            return False  # Stop the operation.

        self.items.pop(item_number - 1)  # Remove the selected item.
        return True  # Tell the program the operation succeeded.


    # CALCULATE SUBTOTAL

    def calculate_subtotal(self):  # Calculate the subtotal.
        subtotal = 0  # Start subtotal at zero.

        for item in self.items:  # Go through all order items.
            subtotal += item.calculate_total()  # Add each item's total.

        return subtotal  # Return the subtotal.


    # CALCULATE TOTAL

    def calculate_total(self):  # Calculate the final bill.
        return self.calculate_subtotal()  # In this system total equals subtotal.

    
    # COMPLETE ORDER

    def complete_order(self):  # Complete the customer order.

        if len(self.items) == 0:  # Check if the order is empty.
            print("Cannot complete an empty order.")  # Show an error.
            return False  # Stop the operation.

        if self.status != "Active":  # Check if the order is active.
            print("Only active orders can be completed.")  # Show an error.
            return False  # Stop the operation.

        self.status = "Completed"  # Change order status.
        return True  # Tell the program the order was completed.

   
    # CANCEL ORDER

    def cancel_order(self):  # Cancel the customer order.

        if self.status == "Completed":  # Check if the order is completed.
            print("Completed orders cannot be cancelled.")  # Show an error.
            return False  # Stop the operation.

        if self.status == "Cancelled":  # Check if the order is already cancelled.
            print("This order is already cancelled.")  # Show an error.
            return False  # Stop the operation.

        self.status = "Cancelled"  # Change the order status to Cancelled.
        return True  # Tell the program cancellation was successful.


    # DISPLAY ORDER

    def show(self):  # Display the complete order.

        print("\n--------------------------------------------")  # Print separator.
        print(f"ORDER #{self.order_id}")  # Display order number.
        print(f"Status: {self.status}")  # Display order status.
        print(f"Created: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}")  # Display creation time.
        print("--------------------------------------------")  # Print separator.

        if len(self.items) == 0:  # Check if there are no items.
            print("No items in this order.")  # Show empty order message.
            return  # Stop displaying the order.

        for number, item in enumerate(self.items, 1):  # Number each order item.
            item.show(number)  # Display the item.

        print("--------------------------------------------")  # Print separator.
        print(f"Subtotal: UGX {self.calculate_subtotal():,.2f}")  # Display subtotal.
        print(f"Total:    UGX {self.calculate_total():,.2f}")  # Display total.


# RESTAURANT CLASS

class Restaurant:  # Main class that manages menu and orders.

    def __init__(self):  # Create the restaurant.
        self.menu = []  # Create an empty menu.
        self.orders = []  # Create an empty order list.

    
    # ADD MENU ITEM

    def add_menu_item(self):  # Allow staff to add a menu item.

        print("\n========== ADD MENU ITEM ==========")  # Display heading.

        item_code = input("Item code: ").strip()  # Ask for item code.

        if item_code == "":  # Check for empty code.
            print("Item code cannot be empty.")  # Show an error.
            return  # Stop the method.

        for item in self.menu:  # Check existing menu items.
            if item.item_code.upper() == item_code.upper():  # Compare item codes.
                print("That item code already exists.")  # Show duplicate message.
                return  # Stop the method.

        name = input("Item name: ").strip()  # Ask for item name.

        if name == "":  # Check for empty name.
            print("Item name cannot be empty.")  # Show an error.
            return  # Stop the method.

        try:
            price = float(input("Price (UGX): "))  # Ask for price.
        except ValueError:
            print("Please enter a valid price.")  # Show an error.
            return  # Stop the method.

        if price <= 0:  # Check if price is valid.
            print("Price must be greater than zero.")  # Show an error.
            return  # Stop the method.

        print("\n1. Food")  # Show food option.
        print("2. Drink")  # Show drink option.
        print("3. Dessert")  # Show dessert option.

        category = input("Choose category: ").strip()  # Ask for category.

        if category == "1": item = FoodItem(item_code, name, price)  # Create food item.
        elif category == "2": item = DrinkItem(item_code, name, price)  # Create drink item.
        elif category == "3": item = DessertItem(item_code, name, price)  # Create dessert item.
        else:
            print("Invalid category.")  # Show an error.
            return  # Stop the method.

        self.menu.append(item)  # Add item to the menu.
        print("\nMenu item added successfully.")  # Confirm the addition.

    
    # ADD DEMO ITEM

    def add_demo_item(self, item_code, name, price, category):  # Add an item automatically.

        if category == "Food": item = FoodItem(item_code, name, price)  # Create food item.
        elif category == "Drink": item = DrinkItem(item_code, name, price)  # Create drink item.
        elif category == "Dessert": item = DessertItem(item_code, name, price)  # Create dessert item.
        else: return  # Stop if the category is invalid.

        self.menu.append(item)  # Add item to menu.
        print(f"Added: {item_code} - {name} (UGX {price:,.0f})")  # Show added item.

    
    # VIEW MENU

    def view_menu(self):  # Display the restaurant menu.

        print("\n========== RESTAURANT MENU ==========")  # Display heading.

        if len(self.menu) == 0:  # Check if menu is empty.
            print("No menu items available.")  # Show empty menu message.
            return  # Stop the method.

        for number, item in enumerate(self.menu, 1):  # Number menu items.
            print(f"{number}. ", end="")  # Display item number.
            item.show()  # Display item information.

   
    # SEARCH MENU

    def search_menu(self, search_term):  # Search for an item by name.

        print("\n========== MENU SEARCH ==========")  # Display heading.
        found = False  # Assume nothing has been found.

        for item in self.menu:  # Go through menu items.
            if search_term.lower() in item.name.lower():  # Check if the name matches.
                item.show()  # Display matching item.
                found = True  # Mark that an item was found.

        if not found:  # Check if no item was found.
            print("No matching menu item found.")  # Show no-result message.

    
    # CREATE ORDER

    def create_order(self):  # Create a new customer order.

        order = Order()  # Create a new Order object.
        self.orders.append(order)  # Add the order to the restaurant.
        print(f"\nOrder #{order.order_id} created successfully.")  # Confirm the order.
        return order  # Return the new order.

    
    # FIND ORDER

    def find_order(self, order_id):  # Find an order using its ID.

        for order in self.orders:  # Search through all orders.
            if order.order_id == order_id:  # Check the order ID.
                return order  # Return the matching order.

        return None  # Return nothing if not found.

    
    # ACTIVE ORDERS

    def active_orders(self):  # Display active orders.

        print("\n========== ACTIVE ORDERS ==========")  # Display heading.
        found = False  # Assume there are no active orders.

        for order in self.orders:  # Go through all orders.
            if order.status == "Active":  # Check for active orders.
                order.show()  # Display the order.
                found = True  # Mark that an order was found.

        if not found:  # Check if no active orders were found.
            print("No active orders.")  # Show message.

    
    # COMPLETED ORDERS

    def completed_orders(self):  # Display completed orders.

        print("\n========== COMPLETED ORDERS ==========")  # Display heading.
        found = False  # Assume there are no completed orders.

        for order in self.orders:  # Go through all orders.
            if order.status == "Completed":  # Check for completed orders.
                order.show()  # Display the order.
                found = True  # Mark that an order was found.

        if not found:  # Check if none were found.
            print("No completed orders.")  # Show message.

    
    # CANCELLED ORDERS

    def cancelled_orders(self):  # Display cancelled orders.

        print("\n========== CANCELLED ORDERS ==========")  # Display heading.
        found = False  # Assume there are no cancelled orders.

        for order in self.orders:  # Go through all orders.
            if order.status == "Cancelled":  # Check for cancelled orders.
                order.show()  # Display the order.
                found = True  # Mark that an order was found.

        if not found:  # Check if no cancelled orders were found.
            print("No cancelled orders.")  # Show message.

    
    # DAILY SUMMARY

    def daily_summary(self):  # Display daily sales information.

        print("\n========== DAILY ORDER SUMMARY ==========")  # Display heading.
        completed_orders = 0  # Start completed order count at zero.
        total_sales = 0  # Start total sales at zero.

        for order in self.orders:  # Go through all orders.
            if order.status == "Completed":  # Only count completed orders.
                completed_orders += 1  # Increase order count.
                total_sales += order.calculate_total()  # Add order total to sales.

        print(f"Completed Orders: {completed_orders}")  # Display number of completed orders.
        print(f"Total Sales: UGX {total_sales:,.2f}")  # Display total sales.

    
    # COMPLETE TEST DEMO

    def test_demo(self):  # Run an automatic demonstration.

        print("""
============================================================
        RESTAURANT ORDERING AND BILLING SYSTEM
                       TEST DEMO
============================================================
""")

        self.menu.clear()  # Clear old menu items.
        self.orders.clear()  # Clear old orders.
        Order.next_order_id = 1  # Reset order numbering.

        print("\n[TEST 1] ADDING SAMPLE MENU ITEMS")  # Show test heading.

        self.add_demo_item("F001", "Chicken and Chips", 15000, "Food")  # Add food.
        self.add_demo_item("F002", "Beef Burger", 12000, "Food")  # Add food.
        self.add_demo_item("D001", "Soda", 3000, "Drink")  # Add drink.
        self.add_demo_item("D002", "Fresh Juice", 5000, "Drink")  # Add drink.
        self.add_demo_item("DS001", "Ice Cream", 6000, "Dessert")  # Add dessert.

        print("\n[TEST 2] DISPLAYING RESTAURANT MENU")  # Show test heading.
        self.view_menu()  # Display menu.

        print("\n[TEST 3] CREATING CUSTOMER ORDER")  # Show test heading.
        order1 = self.create_order()  # Create first order.

        print("\n[TEST 4] CUSTOMER ADDS ITEMS")  # Show test heading.

        chicken = self.menu[0]  # Get chicken.
        soda = self.menu[2]  # Get soda.
        ice_cream = self.menu[4]  # Get ice cream.

        print("Customer orders 2 Chicken and Chips...")  # Explain action.
        order1.add_item(chicken, 2)  # Add chicken.

        print("Customer orders 2 Sodas...")  # Explain action.
        order1.add_item(soda, 2)  # Add soda.

        print("Customer orders 1 Ice Cream...")  # Explain action.
        order1.add_item(ice_cream, 1)  # Add ice cream.

        order1.show()  # Display order.

        print("\n[TEST 5] CUSTOMER CHANGES QUANTITY")  # Show test heading.
        print("Customer changes Chicken and Chips from quantity 2 to 3...")  # Explain action.
        order1.change_quantity(1, 3)  # Change chicken quantity.
        order1.show()  # Display updated order.

        print("\n[TEST 6] CUSTOMER REPLACES AN ORDERED ITEM")  # Show test heading.
        print("Customer decides they do not want Soda.")  # Explain action.
        print("Customer changes Soda to Fresh Juice...")  # Explain action.

        fresh_juice = self.menu[3]  # Get fresh juice.
        order1.replace_item(2, fresh_juice)  # Replace soda.
        order1.show()  # Display updated order.

        print("\n[TEST 7] CUSTOMER REMOVES AN ITEM")  # Show test heading.
        print("Customer decides they do not want Ice Cream.")  # Explain action.
        order1.remove_item(3)  # Remove ice cream.
        order1.show()  # Display updated order.

        print("\n[TEST 8] CALCULATING FINAL BILL")  # Show test heading.

        subtotal = order1.calculate_subtotal()  # Calculate subtotal.
        total = order1.calculate_total()  # Calculate total.

        print(f"Subtotal: UGX {subtotal:,.2f}")  # Display subtotal.
        print(f"Total: UGX {total:,.2f}")  # Display total.

        # Parent-class encapsulation demonstration:
        # __price is private, but its value is accessed through the price property.
        print(f"MenuItem private price accessed through property: UGX {chicken.price:,.2f}")

        print("\n[TEST 9] TESTING ENCAPSULATION AND POLYMORPHISM")
        print("Encapsulation: OrderItem controls access to quantity through a private attribute and property.")
        print("Encapsulation: Order controls valid status values through a private attribute and property.")
        print("Polymorphism: FoodItem, DrinkItem and DessertItem use the same methods differently.")
        print("Encapsulation: MenuItem.__price, OrderItem.__quantity and Order.__status are private and accessed in a controlled way.")
        print("Polymorphism: the same methods behave differently for different menu item types.")  # Show test heading.

        print(f"{chicken.name}: {chicken.prepare()}")  # Call FoodItem prepare().
        print(f"{fresh_juice.name}: {fresh_juice.prepare()}")  # Call DrinkItem prepare().
        print(f"{ice_cream.name}: {ice_cream.prepare()}")  # Call DessertItem prepare().

        print("\n[TEST 10] COMPLETING FIRST ORDER")  # Show test heading.

        order1.complete_order()  # Complete the order.

        print(f"Order #{order1.order_id} status: {order1.status}")  # Show status.
        print(f"Final bill: UGX {order1.calculate_total():,.2f}")  # Show final bill.

        print("\n[TEST 11] DISPLAYING COMPLETED ORDERS")  # Show test heading.
        self.completed_orders()  # Display completed orders.

        print("\n[TEST 12] DISPLAYING ACTIVE ORDERS")  # Show test heading.
        self.active_orders()  # Display active orders.

        print("\n[TEST 13] CREATING SECOND CUSTOMER ORDER")  # Show test heading.

        order2 = self.create_order()  # Create second order.
        burger = self.menu[1]  # Get burger.

        print("Customer orders 1 Beef Burger...")  # Explain action.
        order2.add_item(burger, 1)  # Add burger.

        print("Customer orders 2 Fresh Juices...")  # Explain action.
        order2.add_item(fresh_juice, 2)  # Add juice.

        order2.show()  # Display second order.

        print("\n[TEST 14] SEARCHING THE MENU")  # Show test heading.
        print("Searching for 'juice'...")  # Explain search.
        self.search_menu("juice")  # Search for juice.

        print("\n[TEST 15] TESTING INVALID QUANTITY")  # Show test heading.
        print("Trying to add 0 Beef Burgers...")  # Explain action.

        result = order2.add_item(burger, 0)  # Try adding invalid quantity.

        if not result:  # Check if operation failed.
            print("Invalid quantity was correctly rejected.")  # Confirm validation.

        print("\n[TEST 16] TESTING COMPLETED ORDER PROTECTION")  # Show test heading.
        print("Completing Order #2...")  # Explain action.

        order2.complete_order()  # Complete second order.

        print("Trying to change Order #2 after completion...")  # Explain action.

        result = order2.change_quantity(1, 5)  # Try changing completed order.

        if not result:  # Check if operation failed.
            print("Correctly prevented changes to completed order.")  # Confirm protection.

        print("\n[TEST 17] TESTING ORDER CANCELLATION")  # Show test heading.

        order3 = self.create_order()  # Create third order.
        order3.add_item(chicken, 1)  # Add chicken to third order.
        order3.add_item(soda, 1)  # Add soda to third order.

        print("Customer decides to cancel Order #3...")  # Explain action.
        order3.cancel_order()  # Cancel third order.

        print(f"Order #{order3.order_id} status: {order3.status}")  # Show cancelled status.

        print("\n[TEST 18] DISPLAYING CANCELLED ORDERS")  # Show test heading.
        self.cancelled_orders()  # Display cancelled orders.

        print("\n[TEST 19] TESTING CANCELLED ORDER PROTECTION")  # Show test heading.

        print("Trying to change the cancelled order...")  # Explain action.
        result = order3.change_quantity(1, 5)  # Try changing cancelled order.

        if not result:  # Check if operation failed.
            print("Correctly prevented changes to cancelled order.")  # Confirm protection.

        print("\n[TEST 20] FINAL COMPLETED ORDERS")  # Show test heading.
        self.completed_orders()  # Display completed orders.

        print("\n[TEST 21] DAILY ORDER SUMMARY")  # Show test heading.
        self.daily_summary()  # Display daily summary.

        print("""
============================================================
                    TEST DEMO COMPLETE
============================================================

The demonstration tested:

✓ Abstract MenuItem class
✓ FoodItem
✓ DrinkItem
✓ DessertItem
✓ Inheritance
✓ Polymorphism
✓ Creating customer orders
✓ Adding menu items
✓ Changing item quantities
✓ Replacing an ordered item
✓ Removing an ordered item
✓ Calculating subtotal
✓ Calculating total bill
✓ Different preparation behaviour
✓ Completing orders
✓ Cancelling orders
✓ Active orders
✓ Completed orders
✓ Cancelled orders
✓ Searching menu items
✓ Invalid quantity validation
✓ Protecting completed orders
✓ Protecting cancelled orders
✓ Daily order summary
✓ OrderItem composition

============================================================
""")



# ============================================================
# OOP CONCEPTS USED IN THIS PROGRAM
# ============================================================
# ENCAPSULATION:
# 1. OrderItem.quantity is stored privately as __quantity.
#    The @property getter and setter control how quantity is accessed and changed.
# 2. Order.status is stored privately as __status.
#    The status property allows only Active, Completed or Cancelled.
# 3. MenuItem does NOT make every attribute private; item_code, name and price
#    remain public because encapsulation should be applied where it is useful.
#
# POLYMORPHISM:
# 1. MenuItem defines calculate_price() and prepare() as abstract methods.
# 2. FoodItem, DrinkItem and DessertItem override these methods with different
#    behaviours.
# 3. Therefore, the same method call can produce different results depending
#    on the type of menu item.
# ============================================================

# INTERACTIVE FUNCTIONS


def add_item_to_order(restaurant):  # Add a menu item to an order.

    print("\n========== ADD ITEM TO ORDER ==========")  # Display heading.

    try:
        order_id = int(input("Order ID: "))  # Ask for order ID.
    except ValueError:
        print("Please enter a valid order ID.")  # Show an error.
        return  # Stop the function.

    order = restaurant.find_order(order_id)  # Find the order.

    if order is None:  # Check if order was found.
        print("Order not found.")  # Show error.
        return  # Stop the function.

    if order.status != "Active":  # Check order status.
        print("Only active orders can be changed.")  # Show error.
        return  # Stop the function.

    restaurant.view_menu()  # Display the menu.

    try:
        item_number = int(input("Menu item number: "))  # Ask for menu item.
        quantity = int(input("Quantity: "))  # Ask for quantity.
    except ValueError:
        print("Please enter valid numbers.")  # Show an error.
        return  # Stop the function.

    if item_number < 1 or item_number > len(restaurant.menu):  # Check menu number.
        print("Invalid menu item.")  # Show an error.
        return  # Stop the function.

    menu_item = restaurant.menu[item_number - 1]  # Get selected menu item.

    if order.add_item(menu_item, quantity):  # Add item to order.
        print("Item added successfully.")  # Confirm addition.
        print(f"Preparation: {menu_item.prepare()}")  # Show preparation method.



# CHANGE QUANTITY

def change_quantity_menu(restaurant):  # Change an item's quantity.

    print("\n========== CHANGE QUANTITY ==========")  # Display heading.

    try:
        order_id = int(input("Order ID: "))  # Ask for order ID.
    except ValueError:
        print("Please enter a valid order ID.")  # Show an error.
        return  # Stop the function.

    order = restaurant.find_order(order_id)  # Find the order.

    if order is None:  # Check if order exists.
        print("Order not found.")  # Show error.
        return  # Stop the function.

    order.show()  # Display the order.

    try:
        item_number = int(input("Item number: "))  # Ask for item number.
        quantity = int(input("New quantity: "))  # Ask for new quantity.
    except ValueError:
        print("Please enter valid numbers.")  # Show an error.
        return  # Stop the function.

    if order.change_quantity(item_number, quantity):  # Change quantity.
        print("Quantity changed successfully.")  # Confirm change.



# REPLACE ITEM MENU

def replace_item_menu(restaurant):  # Replace an ordered item.

    print("\n========== REPLACE ORDERED ITEM ==========")  # Display heading.

    try:
        order_id = int(input("Order ID: "))  # Ask for order ID.
    except ValueError:
        print("Please enter a valid order ID.")  # Show an error.
        return  # Stop the function.

    order = restaurant.find_order(order_id)  # Find the order.

    if order is None:  # Check if order exists.
        print("Order not found.")  # Show error.
        return  # Stop the function.

    if order.status != "Active":  # Check order status.
        print("Only active orders can be changed.")  # Show error.
        return  # Stop the function.

    order.show()  # Display current order.

    try:
        item_number = int(input("\nEnter item number you want to replace: "))  # Ask which item to replace.
    except ValueError:
        print("Please enter a valid number.")  # Show an error.
        return  # Stop the function.

    if item_number < 1 or item_number > len(order.items):  # Validate item number.
        print("Invalid item number.")  # Show an error.
        return  # Stop the function.

    print("\nChoose the NEW menu item:")  # Ask for replacement.
    restaurant.view_menu()  # Display menu.

    try:
        new_item_number = int(input("\nEnter new menu item number: "))  # Ask for new item.
    except ValueError:
        print("Please enter a valid number.")  # Show an error.
        return  # Stop the function.

    if new_item_number < 1 or new_item_number > len(restaurant.menu):  # Validate menu number.
        print("Invalid menu item.")  # Show an error.
        return  # Stop the function.

    new_item = restaurant.menu[new_item_number - 1]  # Get new menu item.
    old_item = order.items[item_number - 1]  # Get old order item.

    print(f"\nReplacing: {old_item.menu_item.name}")  # Show old item.
    print(f"With: {new_item.name}")  # Show new item.

    if order.replace_item(item_number, new_item):  # Replace the item.
        print("\nItem replaced successfully.")  # Confirm replacement.
        order.show()  # Display updated order.



# REMOVE ITEM

def remove_item_menu(restaurant):  # Remove an item from an order.

    print("\n========== REMOVE ORDER ITEM ==========")  # Display heading.

    try:
        order_id = int(input("Order ID: "))  # Ask for order ID.
    except ValueError:
        print("Please enter a valid order ID.")  # Show an error.
        return  # Stop the function.

    order = restaurant.find_order(order_id)  # Find the order.

    if order is None:  # Check if order exists.
        print("Order not found.")  # Show error.
        return  # Stop the function.

    order.show()  # Display the order.

    try:
        item_number = int(input("Enter item number to remove: "))  # Ask for item number.
    except ValueError:
        print("Please enter a valid number.")  # Show an error.
        return  # Stop the function.

    if order.remove_item(item_number):  # Remove the item.
        print("Item removed successfully.")  # Confirm removal.
        order.show()  # Display updated order.


# COMPLETE ORDER

def complete_order_menu(restaurant):  # Complete an order.

    print("\n========== COMPLETE ORDER ==========")  # Display heading.

    try:
        order_id = int(input("Order ID: "))  # Ask for order ID.
    except ValueError:
        print("Please enter a valid order ID.")  # Show an error.
        return  # Stop the function.

    order = restaurant.find_order(order_id)  # Find the order.

    if order is None:  # Check if order exists.
        print("Order not found.")  # Show error.
        return  # Stop the function.

    order.show()  # Display the order.

    confirm = input("\nComplete this order? (Y/N): ").strip().lower()  # Ask for confirmation.

    if confirm == "y":  # Check if user confirmed.
        if order.complete_order():  # Complete the order.
            print("\nOrder completed successfully.")  # Confirm completion.
            print(f"Final Bill: UGX {order.calculate_total():,.2f}")  # Show final bill.
    else:
        print("Order remains active.")  # Keep order active.


# CANCEL ORDER

def cancel_order_menu(restaurant):  # Allow the customer to cancel an order.

    print("\n========== CANCEL ORDER ==========")  # Display heading.

    try:
        order_id = int(input("Order ID: "))  # Ask for order ID.
    except ValueError:
        print("Please enter a valid order ID.")  # Show an error.
        return  # Stop the function.

    order = restaurant.find_order(order_id)  # Find the order.

    if order is None:  # Check if order exists.
        print("Order not found.")  # Show error.
        return  # Stop the function.

    if order.status == "Completed":  # Check if the order is completed.
        print("Completed orders cannot be cancelled.")  # Show error.
        return  # Stop the function.

    if order.status == "Cancelled":  # Check if already cancelled.
        print("This order is already cancelled.")  # Show error.
        return  # Stop the function.

    order.show()  # Display the order before cancellation.

    confirm = input("\nCancel this order? (Y/N): ").strip().lower()  # Ask for confirmation.

    if confirm == "y":  # Check if customer confirmed.
        if order.cancel_order():  # Cancel the order.
            print("\nOrder cancelled successfully.")  # Confirm cancellation.
    else:
        print("Order was not cancelled.")  # Keep order active.



# MAIN PROGRAM

def main():  # Main function of the program.

    restaurant = Restaurant()  # Create the restaurant object.

    # Add sample menu items so the program is ready to use.
    restaurant.add_demo_item("F001", "Chicken and Chips", 15000, "Food")  # Add food.
    restaurant.add_demo_item("F002", "Beef Burger", 12000, "Food")  # Add food.
    restaurant.add_demo_item("D001", "Soda", 3000, "Drink")  # Add drink.
    restaurant.add_demo_item("D002", "Fresh Juice", 5000, "Drink")  # Add drink.
    restaurant.add_demo_item("DS001", "Ice Cream", 6000, "Dessert")  # Add dessert.

    while True:  # Keep showing the menu until the user exits.

        print("\n" + "=" * 60)  # Print separator.
        print("       RESTAURANT ORDERING & BILLING SYSTEM")  # Display title.
        print("=" * 60)  # Print separator.

        print("1. Add menu item")  # Menu option 1.
        print("2. View menu")  # Menu option 2.
        print("3. Create new customer order")  # Menu option 3.
        print("4. Add item to order")  # Menu option 4.
        print("5. Change item quantity")  # Menu option 5.
        print("6. Replace ordered item")  # Menu option 6.
        print("7. Remove item from order")  # Menu option 7.
        print("8. Display active orders")  # Menu option 8.
        print("9. Display completed orders")  # Menu option 9.
        print("10. Complete order / Generate bill")  # Menu option 10.
        print("11. Search menu")  # Menu option 11.
        print("12. Daily order summary")  # Menu option 12.
        print("13. Cancel order")  # Menu option 13.
        print("14. Display cancelled orders")  # Menu option 14.
        print("15. Run complete test demo")  # Menu option 15.
        print("0. Exit")  # Exit option.

        choice = input("\nChoose an option: ").strip()  # Ask the user for a choice.

        if choice == "1":  # Add menu item.
            restaurant.add_menu_item()  # Call the method.

        elif choice == "2":  # View menu.
            restaurant.view_menu()  # Display menu.

        elif choice == "3":  # Create order.
            restaurant.create_order()  # Create a new order.

        elif choice == "4":  # Add item to order.
            add_item_to_order(restaurant)  # Call the function.

        elif choice == "5":  # Change quantity.
            change_quantity_menu(restaurant)  # Call the function.

        elif choice == "6":  # Replace item.
            replace_item_menu(restaurant)  # Call the function.

        elif choice == "7":  # Remove item.
            remove_item_menu(restaurant)  # Call the function.

        elif choice == "8":  # Show active orders.
            restaurant.active_orders()  # Display active orders.

        elif choice == "9":  # Show completed orders.
            restaurant.completed_orders()  # Display completed orders.

        elif choice == "10":  # Complete an order.
            complete_order_menu(restaurant)  # Call the function.

        elif choice == "11":  # Search menu.
            search_term = input("Enter item name to search: ")  # Ask for search term.
            restaurant.search_menu(search_term)  # Search the menu.

        elif choice == "12":  # Show daily summary.
            restaurant.daily_summary()  # Display summary.

        elif choice == "13":  # Cancel order.
            cancel_order_menu(restaurant)  # Call the cancellation function.

        elif choice == "14":  # Display cancelled orders.
            restaurant.cancelled_orders()  # Display cancelled orders.

        elif choice == "15":  # Run test demo.
            restaurant.test_demo()  # Run automatic demonstration.

        elif choice == "0":  # Exit the program.
            print("\nThank you for using Restaurant Ordering & Billing System.")  # Goodbye message.
            print("Goodbye!")  # Final message.
            break  # Stop the loop.

        else:  # Handle invalid choices.
            print("\nInvalid option. Please choose a valid number.")  # Show error.

        input("\nPress ENTER to return to the menu...")  # Pause before showing menu again.


# PROGRAM START

if __name__ == "__main__":  # Check if this file is being run directly.
    main()  # Start the program.

    

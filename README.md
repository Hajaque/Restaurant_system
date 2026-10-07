# Restaurant Ordering & Billing System

A simple text-based program that helps a restaurant take customer orders, change them, and work out the final bill. It runs in the terminal, so there is no website or app to install.

## What it does

- Keeps a **menu** of foods, drinks and desserts, each with a code, name and price in Ugandan Shillings (UGX).
- Lets staff **create orders** for customers and add items to them.
- Lets staff **change an order**: update a quantity, swap one item for another, or remove an item.
- **Calculates the bill** automatically.
- Lets staff **complete** an order (the customer has paid) or **cancel** it.
- Shows orders grouped as **active, completed or cancelled**.
- Gives a **daily summary**: how many orders were completed and the total sales.
- Lets staff **search the menu** by name.
- Includes a built-in **test demo** that runs through every feature automatically.

## How to run it

1. Install Python 3.
2. Open a terminal in the folder with the file.
3. Run: `python Restaurant_ordering_&_billing_system.py`
4. Type the number of an option from the menu and press Enter. Type `0` to exit.

The program starts with five sample menu items (Chicken and Chips, Beef Burger, Soda, Fresh Juice, Ice Cream), so you can start taking orders straight away.

## How it works

The program is built around a few simple "objects", each with one job:

| Part | Job |
|---|---|
| **Menu item** (Food, Drink, Dessert) | Stores an item's code, name and price, and knows how to work out its own cost. |
| **Order item** | One line on a bill, such as "2 x Soda". |
| **Order** | A customer's whole order. It holds the lines, a status and the time it was created. |
| **Restaurant** | Holds the menu and all orders, and handles searching and reports. |

A few details worth knowing:

- **Desserts cost slightly more.** Food and drinks are simply price x quantity, but desserts add a 5% service charge.
- **Orders have a life cycle.** Every order starts as *Active*. It can become *Completed* or *Cancelled*, and after that it is locked and cannot be edited. A completed order can never be cancelled.
- **Duplicates are merged.** If you add an item that is already on the order, its quantity goes up instead of creating a second line.
- **Bad input is rejected.** Empty names, zero or negative quantities, duplicate item codes, unknown order IDs and typing letters where numbers are expected all produce a friendly message instead of a crash.
- **The main menu loops.** The program keeps showing the menu and carrying out your choice until you exit.

## Important to Note

- Data is kept in memory only. When you close the program, all orders and any menu items you added are lost.
- Running the test demo (option 15) clears the current menu and orders before it starts.

## Programming concepts shown

This project was written to demonstrate object-oriented programming in Python: **abstract classes, inheritance, polymorphism, composition and input validation**.

## Authors (Group 7)

- Ajak Deng Garang
- Bulima Ezekiel
- Aponi Allan Daniel
- Ayoo Alice
- Agenorwot Cynthia Jillian
- Ayebazibwe Travis

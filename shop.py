import sqlite3
import os

class Main:
    def messagePrinter(self):
        os.system('cls')
        print("Welcome to XYZ shop inventory".center(os.get_terminal_size().columns))
        print("_"*os.get_terminal_size().columns)
        print("1. Create new order/item/user")
        print("2. Read orders/items/users")
        print("3. Update order/item/user from database")
        print("4. Delete order/item/user from database")
        print("0. Create new database (overwrites current)")
        print("To exit just click Enter")

    def userAddRow(self):
        choice = input("1. Add order\n2. Add item\n3. Add user\nClick enter to return\n")

        if choice == "1":
            db.getItems()
            item = input("Choose item in order: ")
            db.getUsers()
            user = input("Choose user who placed the order: ")
            quantity = input("Quantity: ")
            db.insertOrder(item, user, quantity)

        elif choice == "2":
            name = input("Name of item: ")
            quantity = input("Quantity: ")
            price = input("Price: ")
            db.insertItem(name, quantity, price)
        
        elif choice == "3":
            name = input("Name of user: ")
            phone = input("Phone number: ")
            address = input("Address: ")
            db.insertUser(name, phone, address)

        else:
            return

    def userRead(self):
        choice = input("1. Show orders\n2. Show items\n3. Show users\nClick enter to return\n")

        if choice == "1":
            db.getOrders()

        elif choice == "2":
            db.getItems()

        elif choice == "3":
            db.getUsers()

        else:
            return

    def userUpdate(self):
        choice = input("1. Update order\n2. Update item\n3. Update user\nClick enter to return\n")

        if choice == "1":
            db.getOrders()
            id = input("Which element?: ")

            db.getItems()
            item = input("Update with which item?: ")
            db.getUsers()
            user = input("New user: ")
            quantity = input("Quantity: ")
            db.updateOrder(id, item, user, quantity)

        elif choice == "2":
            db.getItems()
            id = input("Which element?: ")

            name = input("New item name: ")
            quantity = input("How many in stock?: ")
            price = input("New price: ") 
            db.updateItem(id, name, quantity, price)
        
        elif choice == "3":
            db.getUsers()
            id = input("Which element?: ")

            name = input("New user name: ")
            phone = input("Phone: ")
            address = input("Address: ") 
            db.updateUser(id, name, phone, address)


    def userDelete(self):
        choice = input("1. Delete order\n2. Delete item\n3. Delete user\nClick enter to return\n")

        if choice == "1":
            db.getOrders()
            table = "orders"

        elif choice == "2":
            db.getItems()
            table = "items"

        elif choice == "3":
            db.getUsers()
            table = "users"

        else:
            return

        row = input("Which row whould you like to delete?: ")
        db.deleteFromTable(table, row)


class dbHandler:
    def __init__(self):
        self.conn = sqlite3.connect('shop.db')

    def createDB(self):
        self.conn.execute("DROP TABLE IF EXISTS items;")
        self.conn.execute("DROP TABLE IF EXISTS users;")
        self.conn.execute("DROP TABLE IF EXISTS orders;")
        self.conn.execute("CREATE TABLE items(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT, quantity INT, price FLOAT);")
        self.conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT, phone VARCHAR(20), address VARCHAR(50));")
        self.conn.execute("CREATE TABLE orders(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, item INTEGER, user INTEGER, quantity INT, FOREIGN KEY(item) REFERENCES items(id), FOREIGN KEY(user) REFERENCES users(id));")

    def insertItem(self, name, quantity, price):
        name = "'" + name + "',"
        quantity = "'" + quantity + "',"
        price = "'" + price + "'"
        query = "INSERT INTO items (name, quantity, price) VALUES(" + name + quantity + price + ") ;"
        self.conn.execute(query)
        self.conn.commit()
    
    def getItems(self):        
        row = self.conn.execute("SELECT * FROM items;")
        for i in row: 
            print(i[0], i[1], i[2], i[3])
        
    def updateItem(self, id, name, quantity, price):
        name = "'" + name + "'"
        query = "UPDATE items SET name = " + name + ", quantity = " + quantity + ", price = " + price + " WHERE id = " + id + ";"
        self.conn.execute(query)
        self.conn.commit()

    def insertUser(self, name, phone, address):
        name = "'" + name + "',"
        phone = "'" + phone + "',"
        address = "'" + address + "'"
        query = "INSERT INTO users (name, phone, address) VALUES(" + name + phone + address + ") ;"
        self.conn.execute(query)
        self.conn.commit()
    
    def getUsers(self):        
        row = self.conn.execute("SELECT * FROM users;")
        for i in row:
            print(i[0], i[1], i[2], i[3])

    def updateUser(self, id, name, phone, address):
        name = "'" + name + "'"
        address = "'" + address + "'"
        phone = "'" + phone + "'"
        query = "UPDATE users SET name = " + name + ", phone = " + phone + ", address = " + address + " WHERE id = " + id + ";"
        self.conn.execute(query)
        self.conn.commit()

    def insertOrder(self, item, user, quantity):
        item2 = "'" + item + "'"
        item = "'" + item + "',"
        user = "'" + user + "',"
        quantity = "'" + quantity + "'"
        query = "INSERT INTO orders (item, user, quantity) VALUES(" + item + user + quantity + ") ;"
        itemQuery = "UPDATE items SET quantity = quantity - " + quantity + " WHERE id = " + item2 + ";"
        self.conn.execute(query)
        self.conn.execute(itemQuery)
        self.conn.commit()
    
    def getOrders(self):
        row = self.conn.execute("SELECT o.id, i.name, u.name, o.quantity, i.price*o.quantity FROM orders o, items i, users u WHERE o.item = i.id AND o.user = u.id;")

        for i in row:
            print("ID:", i[0], "item:", i[1], "buyer:", i[2], "quantity:", i[3], "order value:", i[4])

    def updateOrder(self, id, item, user, quantity):
        query = "UPDATE orders SET item = " + item + ", user = " + user + ", quantity = " + quantity + " WHERE id = " + id + ";"
        self.conn.execute(query)
        self.conn.commit()

    def deleteFromTable(self, table, row):
        query = "DELETE FROM " + table + " WHERE id = " + row + ";"
        self.conn.execute(query)
        self.conn.commit()
       

main = Main()
db = dbHandler()

while True:
    main.messagePrinter()
    option = input("Your option: ")

    if option == "0":
        db.createDB()
        # test values
        db.insertItem("Milk", "22", "2.44")
        db.insertUser("Adam", "123456789", "London")
        db.insertOrder("1","1","7")
        continue

    if option == "1":
        main.userAddRow()
        input("Added...")
        continue

    if option == "2":
        main.userRead()
        input("Press Enter to continue...")
        continue

    if option == "3":
        main.userUpdate()
        input("Row updated...")
        continue

    if option == "4":
        main.userDelete()
        input("Row deleted...")
        continue

    else:
        break
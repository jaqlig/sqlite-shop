import sqlite3
import os

class Main:
    def messagePrinter(self):
        os.system('cls')
        print("Welcome to XYZ shop inventory".center(os.get_terminal_size().columns))
        print("_"*os.get_terminal_size().columns)
        print("1. Show orders")
        print("2. Show items")
        print("3. Show users")
        print("4. Create new order/item/user")
        print("5. Modify order/item/user from database")
        print("6. Delete order/item/user from database")
        print("0. Create new databse (overwrites current)")
        print("To exit just click Enter")

    def userAddRow(self):
        choice = input("1. Add order\n2. Add item\n3. Add user\nEnter to return\n")

        if choice == "1":

            db.getItems()
            item = input("Choose item in order: ")
            db.getUsers()
            user = input("Choose user who placed the order: ")
            db.insertOrder(item, user)


        elif choice == "2":
            name = input("Name of item: ")
            quantity = input("Quantity: ")
            price = input("Price: ")
            db.insertItem(name, quantity, price)
        
        elif choice == "3":
            name = input("Name of user: ")
            phone = input("Phone number: ")
            address = input("Address: ")
            db.insertItem(name, phone, address)

        else:
            return    


class dbHandler:
    def __init__(self):
        self.conn = sqlite3.connect('shop.db')

    def createDB(self):
        self.conn.execute("DROP TABLE IF EXISTS items;")
        self.conn.execute("DROP TABLE IF EXISTS users;")
        self.conn.execute("DROP TABLE IF EXISTS orders;")
        self.conn.execute("CREATE TABLE items(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT, quantity INT, price FLOAT);")
        self.conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT, phone VARCHAR(20), address VARCHAR(50));")
        self.conn.execute("CREATE TABLE orders(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, item INTEGER, user INTEGER, FOREIGN KEY(item) REFERENCES items(id), FOREIGN KEY(user) REFERENCES users(id));")

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

    def insertOrder(self, item, user):
        item = "'" + item + "',"
        user = "'" + user + "'"
        query = "INSERT INTO orders (item, user) VALUES(" + item + user + ") ;"
        self.conn.execute(query)
        self.conn.commit()
    
    def getOrders(self):
        row = self.conn.execute("SELECT o.id, i.name, u.name FROM orders o, items i, users u WHERE o.item = i.id AND o.user = u.id;")

        for i in row:
            print(i[0], i[1], i[2])
       

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
        db.insertOrder("1","1")
        continue

    if option == "1":
        db.getOrders()
        input("Press Enter to continue...")
        continue

    if option == "2":
        db.getItems()
        input("Press Enter to continue...")
        continue

    if option == "3":
        db.getUsers()
        input("Press Enter to continue...")
        continue

    if option == "4":
        main.userAddRow()
        input("Added...")
        continue

    else:
        break
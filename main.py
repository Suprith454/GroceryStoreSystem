import csv
import os
from datetime import datetime

PRODUCT_FILE = "store.csv"
BILL_DIR = "bills"

# Ensure bill directory exists
os.makedirs(BILL_DIR, exist_ok=True)

def load_products():
    products = []
    if os.path.exists(PRODUCT_FILE):
        with open(PRODUCT_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['price'] = float(row['price'])
                row['stock'] = int(row['stock'])
                products.append(row)
    return products

def save_products(products):
    with open(PRODUCT_FILE, mode='w', newline='') as file:
        fieldnames = ['id', 'name', 'price', 'stock']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)

def add_product():
    products = load_products()
    pid = input("Enter product ID: ")
    if any(p['id'] == pid for p in products):
        print("Product ID already exists!")
        return
    name = input("Enter product name: ")
    price = float(input("Enter price: "))
    stock = int(input("Enter stock quantity: "))
    products.append({'id': pid, 'name': name, 'price': price, 'stock': stock})
    save_products(products)
    print("Product added successfully.")

def view_products():
    products = load_products()
    print("\nAvailable Products:")
    print("{:<10} {:<20} {:<10} {:<10}".format("ID", "Name", "Price", "Stock"))
    for p in products:
        print("{:<10} {:<20} {:<10} {:<10}".format(p['id'], p['name'], p['price'], p['stock']))

def update_product():
    products = load_products()
    pid = input("Enter product ID to update: ")
    for p in products:
        if p['id'] == pid:
            p['name'] = input("Enter new name: ")
            p['price'] = float(input("Enter new price: "))
            p['stock'] = int(input("Enter new stock: "))
            save_products(products)
            print("Product updated.")
            return
    print("Product not found.")

def delete_product():
    products = load_products()
    pid = input("Enter product ID to delete: ")
    products = [p for p in products if p['id'] != pid]
    save_products(products)
    print("Product deleted if it existed.")

def search_product():
    products = load_products()
    query = input("Enter product name to search: ").lower()
    found = [p for p in products if query in p['name'].lower()]
    if found:
        print("\nSearch Results:")
        for p in found:
            print(p)
    else:
        print("No product found.")

def create_bill():
    products = load_products()
    cart = []
    total = 0
    while True:
        view_products()
        pid = input("Enter product ID to buy (or 'done' to finish): ")
        if pid.lower() == 'done':
            break
        quantity = int(input("Enter quantity: "))
        for p in products:
            if p['id'] == pid and p['stock'] >= quantity:
                cost = quantity * p['price']
                cart.append((p['name'], quantity, p['price'], cost))
                p['stock'] -= quantity
                total += cost
                break
        else:
            print("Invalid ID or insufficient stock.")

    save_products(products)

    # Generate Bill
    if cart:
        filename = f"bill_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        path = os.path.join(BILL_DIR, filename)
        with open(path, 'w') as file:
            file.write("====== Grocery Store Bill ======\n")
            for name, qty, price, cost in cart:
                file.write(f"{name} x{qty} @ {price} = ₹{cost:.2f}\n")
            file.write(f"\nTotal Amount: ₹{total:.2f}\n")
            file.write("Thank you for shopping!\n")
        print(f"Bill generated: {filename}")
    else:
        print("No items in cart.")

def menu():
    while True:
        print("\n--- Grocery Store Management ---")
        print("1. Add Product")
        print("2. View Products")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Search Product")
        print("6. Create Bill")
        print("7. Exit")
        choice = input("Enter choice: ")
        if choice == '1':
            add_product()
        elif choice == '2':
            view_products()
        elif choice == '3':
            update_product()
        elif choice == '4':
            delete_product()
        elif choice == '5':
            search_product()
        elif choice == '6':
            create_bill()
        elif choice == '7':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    menu()

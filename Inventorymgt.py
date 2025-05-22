inventory = {}

menu_options = [
    "Display Inventory",
    "Add Product",
    "Update Product Quantity",
    "Remove product"
    "Exit"
]

while True:
    print("\nInventory Management System")
    for i in range(len(menu_options)):
        print(f"{i+1}.{menu_options[i]}")

    choice = int(input("Enter your choice(1-5): "))

    if choice == 1:
        if not inventory :
            print("No inventory available at the moment")
        else:
            print("\nProduct Name\tQuantity")
            for name in inventory:
                print(f"{name}\t\t{inventory[name]}")

    elif choice == 2:
        name = input("Enter product name: ")
        if name in inventory:
            print("Product already exists. Try updating it.")
        else:
            quantity = int(input("Enter Quantity: "))
            inventory[name] = quantity
            print("Product entered successfully!")

    elif choice == 3:
        name = input("Enter product name to update: ")
        if name in inventory:
            change = int(input("Enter quantity to add or subtract(e.g -3 or 5): "))
            inventory[name] += change
            print("Quantity updated.")
        else:
            print("Product not found")

    elif choice == 4:
        name = input("Enter product name to remove: ")
        if name in inventory:
            del inventory[name]
            print("Product removed")
        else:
            print("Product not found")
    
    elif choice == 5:
        print("Exiting program.")
        break

    else:
        print("Invalid choice. Please choose a number between 1 and 5.")

import json
import tkinter as tk
from tkinter import messagebox

# Opens Order and product data files and reads in as JSON
order_path = 'OrderData.txt'
with open(order_path, 'r') as file:
    orders = json.load(file)

product_path = 'productData.txt'
with open(product_path, 'r') as file:
    products = json.load(file)


# Checks inputted barcode to actual item barcode to verify correct item is being scanned
def check_item(barcode, order):
    global scanned_items, checkbox_var, entry, current_index
    item_num = entry.get().strip()
    current_item = barcode

    if checkbox_var.get():
        messagebox.showinfo("Barcode Bypass", "Barcode for item has been bypassed.")
        # order['line_items'].pop(0)
        current_index += 1
        scanned_items += str(current_item) + ", "
        remaining = order['line_items']
        entry.delete(0, tk.END)
        next_item(remaining, order)
    else:
        try:
            item_num = str(item_num)
            if item_num == current_item:
                entry.delete(0, tk.END)
                # order['line_items'].pop(0)
                current_index += 1
                scanned_items += str(current_item) + ", "
                remaining = order['line_items']
                messagebox.showinfo("Correct Item", "Correct item scanned! Good Job!")
                next_item(remaining, order)
            else:
                entry.delete(0, tk.END)
                messagebox.showerror("Error", "Incorrect item scanned! Try again.")
        except ValueError:
            entry.delete(0, tk.END)
            messagebox.showerror("Error", "Please enter a valid Item number.")


# Proceeds to increase index to move to next item if there is another
def next_item(remaining, order):
    global current_index, scanned_label, checkbox_var, item_label, entry
    scanned_label.config(text=scanned_items)

    if current_index < len(remaining):
        # entry.delete(0, tk.END)
        checkbox_var.set(False)
        new_window.destroy()
        open_order_items(order)
        # item_label.config(text=next_barcode)
    else:
        messagebox.showinfo("Info", "All items checked!")
        order['tags'] += 'Scanned '
        with open(order_path, 'w') as file:
            json.dump(orders, file, indent = 2)
        new_window.destroy()


# Gets the barcode to ensure correct item is scanned
def get_barcode(prod_id, var_id):
    for product in products:
        if prod_id == product['id']:
            for variant in product['variants']:
                if var_id == variant['id']:
                    return variant['barcode']
    messagebox.showinfo("Incorrect Item Number", "The item number is not valid.")
    return False


# Opens new window to allow for ensuring each order item is scanned and correct
def open_order_items(order):
    global current_index, scanned_label, checkbox_var, item_label, entry, image_label, new_window
    new_window = tk.Toplevel(root)
    new_window.title(order['name'])

    new_window.geometry("800x600")

    prod_id = order['line_items'][current_index]['product_id']
    var_id = order['line_items'][current_index]['variant_id']

    barcode = get_barcode(prod_id, var_id)

    item_label = tk.Label(new_window, text=barcode)
    item_label.pack(pady=10)

    entry = tk.Entry(new_window)
    entry.pack(pady=10)
    entry.bind("<Return>", lambda event=None: check_item(barcode, order))

    checkbox_var = tk.BooleanVar()
    checkbox = tk.Checkbutton(new_window, text="Bypass Barcode", variable=checkbox_var)
    checkbox.pack(pady=10)

    check_button = tk.Button(new_window, text="Process Item", command=lambda: check_item(barcode, order))
    check_button.pack(pady=10)

    scanned_label = tk.Label(new_window, text=scanned_items)
    scanned_label.pack(pady=10)

    root.wait_window(new_window)


# Gets entered order number and compares it to order numbers in order data
# and proceeds to open_order_items if order num found, else throws an error
def check_order_num():
    entered_order_num = order_entry.get()

    for order in orders:
        if entered_order_num == '':
            messagebox.showinfo("Incorrect Order Number", "No order number was entered.")
            return False
        elif entered_order_num in order['name']:
            open_order_items(order)
            return True
    messagebox.showinfo("Incorrect Order Number", "The order number you entered is incorrect.")
    order_entry.delete(0, tk.END)
    return False


# Main function that creates Order Number Window
root = tk.Tk()
root.title("Orders")

root.geometry("800x600")

scanned_label, checkbox_var, item_label, entry, image_label, new_window = None, None, None, None, None, None
scanned_items = "Scanned Items: "
current_index = 0

# Order Entry
order_label = tk.Label(root, text="Enter Order Number:")
order_label.pack(pady=10, padx=10)

order_entry = tk.Entry(root, relief="solid")
order_entry.pack(pady=10, padx=10)

order_entry.bind("<Return>", lambda event=None: check_order_num())

# Submit button
submit_button = tk.Button(root, text="Submit", command=check_order_num)
submit_button.pack(pady=10, padx=10)

root.mainloop()
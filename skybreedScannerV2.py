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


def check_order_num():
    entered_order_num = order_entry.get()

    for order in orders:
        if entered_order_num == '':
            messagebox.showinfo("Incorrect Order Number", "No order number was entered.")
            return False
        elif entered_order_num in order['name']:
            messagebox.showinfo("Correct order number", "Correct order number scanned! Good Job!.")
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

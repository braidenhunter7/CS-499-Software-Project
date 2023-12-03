import json
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO
import requests


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
    current_barcode = barcode
    current_item = order['line_items'][current_index]
    remaining = order['line_items']

    # Checks to see if checkbox is clicked and bypasses product barcode if so
    if checkbox_var.get():
        messagebox.showinfo("Barcode Bypass", "Barcode for item has been bypassed.")
        # If quantity of product more than one, cycle through to scan each item
        if current_item['quantity'] != 1:
            quantity = current_item['quantity']
            for i in range(0, quantity):
                scanned_items += str(current_item['title']) + ", "
                next_item(remaining, order)
        # If only one item in quantity, proceed to next item
        else:
            current_index += 1
            scanned_items += str(current_item['title']) + ", "
            entry.delete(0, tk.END)
            next_item(remaining, order)
    # If checkbox is not clicked, test wether barcode inputted matches product barcode
    else:
        try:
            item_num = str(item_num)
            if item_num == current_barcode:
                entry.delete(0, tk.END)
                if current_item['quantity'] != 1:
                    quantity = current_item['quantity']
                    for i in range(0, quantity):
                        scanned_items += str(current_item['title']) + ", "
                        next_item(remaining, order)
                else:
                    current_index += 1
                    scanned_items += str(current_item['title']) + ", "
                    remaining = order['line_items']
                    messagebox.showinfo("Correct Item", "Correct item scanned! Good Job!")
                    next_item(remaining, order)
            # If incorrect barcode scanned popup error
            else:
                entry.delete(0, tk.END)
                messagebox.showerror("Error", "Incorrect item scanned! Try again.")
        except ValueError:
            entry.delete(0, tk.END)
            messagebox.showerror("Error", "Please enter a valid Item number.")


# Updates the order tag with Scanned after all items in order are scanned
def update_order_tag(order):
    if 'Scanned ' in order['tags']:
        new_window.destroy()
    else:
        order['tags'] += 'Scanned '
        with open(order_path, 'w') as file:
            json.dump(orders, file, indent=2)
        new_window.destroy()


# Proceeds to increase index to move to next item if there is another
def next_item(remaining, order):
    global current_index, scanned_label, checkbox_var, item_label, entry, scanned_items
    scanned_label.config(text=scanned_items)

    # Moves to the next item if there is one
    if current_index < len(remaining):
        # entry.delete(0, tk.END)
        checkbox_var.set(False)
        new_window.destroy()
        open_order_items(order)
    # If no items left in order to be scanned, update order tag
    else:
        messagebox.showinfo("Info", "All items checked!")
        current_index = 0
        scanned_items = "Scanned Items: "
        update_order_tag(order)


# Gets the url for image
def get_src(product_id, image_id):
    for category in product_id['images']:
        if image_id == category['id']:
            return category['src']
    messagebox.showinfo("Incorrect Image ID", "The image ID is not valid.")
    return False


# Gets the image ID for use in obtaining src above
def get_img_id(prod_id, var_id):
    for product in products:
        if prod_id == product['id']:
            product_id = product
            for variant in product['variants']:
                if var_id == variant['id']:
                    try:
                        image_id = variant['image_id']
                        src = get_src(product_id, image_id)
                    except:
                        src = 'https://cdn.shopify.com/s/files/1/0255/7739/0125/files/500px_x_250px_480x480.png?v=1637720912'
                    return src
    messagebox.showinfo("Incorrect Item Number", "The item number is not valid.")
    return False


# Gets the barcode to ensure correct item is scanned
def get_barcode(prod_id, var_id):
    for product in products:
        if prod_id == product['id']:
            for variant in product['variants']:
                if var_id == variant['id']:
                    return variant['barcode']
    messagebox.showinfo("Incorrect Item Number", "The item number is not valid.")
    return False

# Displays an image via url
def display_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = img.resize((300, 200))
    photo = ImageTk.PhotoImage(img)
    return photo

# Creates a popup that asks user if they want to close out without finishing
def on_closing():
    global current_index, scanned_items
    if messagebox.askokcancel("Quit", "Are you sure you want to quit? Progress will not be saved."):
        current_index = 0
        scanned_items = "Scanned Items: "
        new_window.destroy()


# Opens new window to allow for ensuring each order item is scanned and correct
def open_order_items(order):
    global current_index, scanned_label, checkbox_var, item_label, entry, image_label, new_window
    new_window = tk.Toplevel(root, bg="black")
    new_window.title(order['name'])

    new_window.geometry("800x600")
    new_window.protocol("WM_DELETE_WINDOW", on_closing)

    prod_id = order['line_items'][current_index]['product_id']
    var_id = order['line_items'][current_index]['variant_id']

    barcode = get_barcode(prod_id, var_id)
    src = get_img_id(prod_id, var_id)

    photo = display_image(src)
    image_label = tk.Label(new_window, image=photo)
    image_label.photo = photo
    image_label.pack(pady=10, padx=10)

    item_label = tk.Label(new_window, text=order['line_items'][current_index]['name'], fg="black")
    item_label.pack(pady=10, padx=10)

    entry = tk.Entry(new_window, fg="black")
    entry.pack(pady=10, padx=10)
    entry.bind("<Return>", lambda event=None: check_item(barcode, order))

    checkbox_var = tk.BooleanVar()
    checkbox = tk.Checkbutton(new_window, text="Bypass Barcode", variable=checkbox_var, fg="black", cursor="hand2")
    checkbox.pack(pady=10, padx=10)

    check_button = tk.Button(new_window, text="Process Item", command=lambda: check_item(barcode, order), fg="black")
    check_button.configure(cursor="hand2")
    check_button.pack(pady=10, padx=10)

    scanned_label = tk.Label(new_window, text=scanned_items, fg="black")
    scanned_label.pack(pady=10, padx=10)

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
            order_entry.delete(0, tk.END)
            open_order_items(order)
            return True
    messagebox.showinfo("Incorrect Order Number", "The order number you entered is incorrect.")
    order_entry.delete(0, tk.END)
    return False


# Main function that creates Order Number Window
root = tk.Tk()
root.title("Orders")

root.geometry("800x600")
root.configure(bg="black")

scanned_label, checkbox_var, item_label, entry, image_label, new_window = None, None, None, None, None, None
scanned_items = "Scanned Items: "
current_index = 0
stock_url = 'https://cdn.shopify.com/s/files/1/0255/7739/0125/files/500px_x_250px_480x480.png?v=1637720912'

stock_photo = display_image(stock_url)
image_label = tk.Label(new_window, image=stock_photo)
image_label.photo = stock_photo
image_label.pack(pady=10, padx=10)

# Order Entry
order_label = tk.Label(root, text="Enter Order Number:", fg="white", bg="red")
order_label.pack(pady=10, padx=10)

order_entry = tk.Entry(root, relief="solid")
order_entry.pack(pady=10, padx=10)

order_entry.bind("<Return>", lambda event=None: check_order_num())

# Submit button
submit_button = tk.Button(root, text="Submit", command=check_order_num, fg="white", background="red", cursor="hand2")
submit_button.pack(pady=10, padx=10)

root.mainloop()

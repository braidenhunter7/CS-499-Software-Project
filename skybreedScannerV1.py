import tkinter as tk
from tkinter import messagebox

class MyGUI:
    def __init__(self):
        self.root = tk.Tk()

        self.label = tk.Label(self.root, text="Order", font=('Arial', 18))
        self.label.pack(padx=10, pady=10)

        self.textbox = tk.Text(self.root, height=5, font=('Arial', 16))
        self.textbox.pack(padx=10, pady=10)

        self.check = tk.Checkbutton(self.root, text="No Barcode", font=('Arial', 18), command=self.no_barcode)
        self.check.pack(padx=10, pady=10)

        self.button = tk.Button(self.root, text="Check Barcode", font=('Arial', 18), command = self.check_item)
        self.button.pack(padx=10,pady=10)

        self.root.mainloop()

    def no_barcode(self):
        messagebox.showinfo(title="Check Item", message="Barcode scanning bypassed")

    def check_item(self):
        if self.textbox.get('1.0', tk.END).strip() == 2203:
            messagebox.showinfo(title="Check Item", message = "Correct item! Good Job!")
        else:
            print(self.textbox.get('1.0', tk.END))
            messagebox.showinfo(title="Check Item", message = "Incorrect item: Please try again")

MyGUI()
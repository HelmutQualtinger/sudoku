import tkinter as tk

root = tk.Tk()

# Create a frame to hold the grid
frame = tk.Frame(root)
frame.pack()

# Create a button to open the popup menu
button = tk.Button(root, text="Arrange",
                   command=lambda: popup_menu.post(button.winfo_root()))


# Create a popup menu
popup_menu = tk.Menu(root, tearoff=0)

# Add arrange options to the popup menu
popup_menu.add_command(label="Grid", command=lambda: arrange_grid())
popup_menu.add_command(label="Pack", command=lambda: arrange_pack())

# Set the grid layout for the frame
frame.grid(row=0, column=0, sticky="nsew")

# Bind the grid layout to the popup menu
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

button.grid()
def arrange_grid():
    for widget in popup_menu.winfo_children():
        widget.grid(row=0, column=0)


def arrange_pack():
    for widget in popup_menu.winfo_children():
        widget.pack()


root.mainloop()

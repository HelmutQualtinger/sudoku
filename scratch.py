import tkinter as tk
import random
root = tk.Tk()

# Create the grid of frames
frames = []
for i in range(3):
    for j in range(3):
        frame = tk.Frame(root, borderwidth=2, relief="solid")
        frame.grid(row=i, column=j, padx=5, pady=5)
        frames.append(frame)

# Create the buttons inside each frame
buttons = []
for frame in frames:
    for i in range(3):
        for j in range(3):
            button = tk.Button(frame, text=random.choice([1,2,3,4,5,6,7,9,9,""]),width=3, height=3,
                               justify='center', bg="#80f080", relief=tk.RAISED, fg='#000000',
                               font=("Helvetica", 16),
                               borderwidth=4)
            button.grid(row=i, column=j, padx=5, pady=5)
            buttons.append(button)

root.mainloop()

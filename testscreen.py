import tkinter as tk

# Initialize the window
root = tk.Tk()
root.attributes("-fullscreen", True) # Fills the 3.5" TFT screen
root.configure(bg='#539d8b')        # BMO's signature teal

# Create the text label
label = tk.Label(
    root, 
    text="HELLO! I AM BMO", 
    font=("Helvetica", 32, "bold"), 
    fg="white", 
    bg='#539d8b'
)

label.pack(expand=True)

# Run the interface
root.mainloop()

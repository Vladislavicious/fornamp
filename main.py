import tkinter as tk
import customtkinter as ctk

from GUI.GUI import *


if __name__ == "__main__":
    root = ctk.CTk()
    font_ = ctk.CTkFont(family="Arial", size=16)
    fontmini = ctk.CTkFont(family="Arial", size=12)
    app = Main_window(root)
    app.pack()
    root.title("Task manager")
    root.geometry("1000x600+250+100")
    root.resizable(False, False)
    root.mainloop()

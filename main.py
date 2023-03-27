import tkinter as tk
from tkinter import ttk

from GUI.GUI import *


if __name__ == "__main__":
    root = tk.Tk()
    app = Main_window(root)
    app.pack()
    root.title("Task manager")
    root.geometry("1000x600+250+100")
    root.resizable(False, False)
    root.mainloop()
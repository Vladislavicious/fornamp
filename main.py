import GUI.GUI as gui

if __name__ == "__main__":
    root = gui.ctk.CTk()
    
    app = gui.Main_window(root)
    app.pack()
    root.title("Task manager")
    root.geometry("1000x600+250+100")
    root.resizable(False, False)
    root.mainloop()

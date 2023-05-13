import GUI.ProfileWindow as prof

if __name__ == "__main__":
    root = prof.ctk.CTk()
    profile = prof.ProfileWindow(root)
    profile.pack()
    root.title("Autorization\Registration")
    root.geometry("500x250+500+390")
    root.resizable(False, False)
    root.mainloop()
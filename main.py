import GUI.ProfileWindow as prof

if __name__ == "__main__":
    root = prof.ctk.CTk()
    profile = prof.ProfileWindow(root)
    profile.pack()
    root.title("Autorization\Registration")
    root.geometry("500x220+500+340")
    root.resizable(False, False)
    root.mainloop()

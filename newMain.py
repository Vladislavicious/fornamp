import customtkinter as ctk
from altGUI.NewProfileWindow import NewProfileWindow

if __name__ == "__main__":
    root = ctk.CTk()
    profile = NewProfileWindow(root)
    profile.pack()
    root.title("Autorization\Registration")
    root.geometry("500x220+500+340")
    root.resizable(False, False)
    root.mainloop()

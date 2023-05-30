import customtkinter as ctk
from GUI.ProfileWindow import ProfileWindow

if __name__ == "__main__":
    root = ctk.CTk()
    profile = ProfileWindow(root)
    profile.pack()
    root.title("Autorization\Registration")
    root.geometry("500x220+500+340")
    root.resizable(False, False)
    root.mainloop()

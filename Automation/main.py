import customtkinter as ctk

from gui.main_window import MainWindow

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()

MainWindow(root)

root.mainloop()
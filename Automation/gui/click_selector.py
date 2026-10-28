import tkinter as tk


class ClickSelector:

    def __init__(self):

        self.result = None

    def select(self):

        root = tk.Toplevel()

        root.attributes("-fullscreen", True)
        root.attributes("-topmost", True)
        root.attributes("-alpha", 0.15)

        root.configure(bg="black")

        canvas = tk.Canvas(
            root,
            cursor="crosshair",
            bg="black",
            highlightthickness=0
        )

        canvas.pack(
            fill="both",
            expand=True
        )

        def on_click(event):

            self.result = {

                "x": root.winfo_pointerx(),
                "y": root.winfo_pointery()

            }

            root.destroy()

        root.bind(
            "<Button-1>",
            on_click
        )

        root.focus_force()

        root.wait_window()

        return self.result
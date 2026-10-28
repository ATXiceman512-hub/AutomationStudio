import tkinter as tk


class RegionSelector:

    def __init__(self):

        self.result = None

    def select(self):

        root = tk.Toplevel()

        root.attributes("-fullscreen", True)
        root.attributes("-topmost", True)
        root.attributes("-alpha", 0.25)

        root.configure(bg="black")

        canvas = tk.Canvas(
            root,
            bg="black",
            highlightthickness=0,
            cursor="cross"
        )

        canvas.pack(
            fill="both",
            expand=True
        )

        start_x = None
        start_y = None

        rect = None

        def on_press(event):

            nonlocal start_x
            nonlocal start_y
            nonlocal rect

            start_x = root.winfo_pointerx()
            start_y = root.winfo_pointery()

            rect = canvas.create_rectangle(
                start_x,
                start_y,
                start_x,
                start_y,
                outline="red",
                width=2
            )

        def on_drag(event):

            if rect is None:
                return

            current_x = root.winfo_pointerx()
            current_y = root.winfo_pointery()

            canvas.coords(
                rect,
                start_x,
                start_y,
                current_x,
                current_y
            )

        def on_release(event):

            if start_x is None:
                return

            end_x = root.winfo_pointerx()
            end_y = root.winfo_pointery()

            self.result = {

                "x": min(start_x, end_x),
                "y": min(start_y, end_y),

                "width": abs(end_x - start_x),
                "height": abs(end_y - start_y)
            }

            print(
                "REGION CAPTURED:",
                self.result
            )

            root.quit()
            root.destroy()

        def on_escape(event):

            self.result = None

            root.quit()
            root.destroy()

        canvas.bind(
            "<ButtonPress-1>",
            on_press
        )

        canvas.bind(
            "<B1-Motion>",
            on_drag
        )

        canvas.bind(
            "<ButtonRelease-1>",
            on_release
        )

        root.bind(
            "<Escape>",
            on_escape
        )

        root.focus_force()

        root.mainloop()

        return self.result
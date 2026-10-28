import customtkinter as ctk

from core.region_manager import RegionManager
from gui.region_selector import RegionSelector


class RegionsTab(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.manager = RegionManager()

        self.build_ui()

        self.refresh()

    def build_ui(self):

        ctk.CTkLabel(
            self,
            text="Regions",
            font=("Segoe UI", 22, "bold")
        ).pack(
            pady=10
        )

        form = ctk.CTkFrame(
            self
        )

        form.pack(
            fill="x",
            padx=10,
            pady=10
        )

        #
        # Name
        #

        ctk.CTkLabel(
            form,
            text="Name"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        ctk.CTkButton(
            form,
            text="Select Region",
            command=self.pick_region
        ).grid(
            row=0,
            column=2,
            padx=10
        )

        self.name_entry = ctk.CTkEntry(
            form
        )

        self.name_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        #
        # X
        #

        ctk.CTkLabel(
            form,
            text="X"
        ).grid(
            row=1,
            column=0
        )

        self.x_entry = ctk.CTkEntry(
            form
        )

        self.x_entry.grid(
            row=1,
            column=1
        )

        #
        # Y
        #

        ctk.CTkLabel(
            form,
            text="Y"
        ).grid(
            row=2,
            column=0
        )

        self.y_entry = ctk.CTkEntry(
            form
        )

        self.y_entry.grid(
            row=2,
            column=1
        )

        #
        # Width
        #

        ctk.CTkLabel(
            form,
            text="Width"
        ).grid(
            row=3,
            column=0
        )

        self.width_entry = ctk.CTkEntry(
            form
        )

        self.width_entry.grid(
            row=3,
            column=1
        )

        #
        # Height
        #

        ctk.CTkLabel(
            form,
            text="Height"
        ).grid(
            row=4,
            column=0
        )

        self.height_entry = ctk.CTkEntry(
            form
        )

        self.height_entry.grid(
            row=4,
            column=1
        )

        ctk.CTkButton(
            form,
            text="Add Region",
            command=self.add_region
        ).grid(
            row=5,
            column=0,
            columnspan=2,
            pady=10
        )

        self.region_list = ctk.CTkTextbox(
            self
        )

        self.region_list.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    def add_region(self):

        try:

            self.manager.add_region(

                self.name_entry.get(),

                self.x_entry.get(),
                self.y_entry.get(),

                self.width_entry.get(),
                self.height_entry.get()
            )

            self.refresh()

        except:

            pass


    def pick_region(self):

        selector = RegionSelector()

        region = selector.select()

        if not region:
            return

        self.x_entry.delete(0, "end")
        self.y_entry.delete(0, "end")
        self.width_entry.delete(0, "end")
        self.height_entry.delete(0, "end")

        self.x_entry.insert(
            0,
            str(region["x"])
        )

        self.y_entry.insert(
            0,
            str(region["y"])
        )

        self.width_entry.insert(
            0,
            str(region["width"])
        )

        self.height_entry.insert(
            0,
            str(region["height"])
        )

    def refresh(self):

        self.region_list.delete(
            "1.0",
            "end"
        )

        for name, region in (
            self.manager.regions.items()
        ):

            self.region_list.insert(
                "end",
                f"{name}\n"
                f" X:{region['x']}\n"
                f" Y:{region['y']}\n"
                f" W:{region['width']}\n"
                f" H:{region['height']}\n\n"
            )
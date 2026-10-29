import customtkinter as ctk
import json

from gui.click_selector import ClickSelector
from tkinter import ttk


class MacroEditor(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.events = []
        self.selected_index = None
        self.drag_item = None

        self.build_ui()

    def build_ui(self):

        self.grid_columnconfigure(0, weight=0)  # toolbox
        self.grid_columnconfigure(1, weight=3)  # event list
        self.grid_columnconfigure(2, weight=2)  # properties

        self.grid_rowconfigure(0, weight=1)


        #TOOLBOX
        toolbox_frame = ctk.CTkFrame(self)

        toolbox_frame.grid(
            row=0,
            column=0,
            sticky="ns",
            padx=(10, 5),
            pady=10
        )

        #LEFT
        left_frame = ctk.CTkFrame(self)

        left_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=10,
            pady=10
        )

        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="#1e1e1e",
            foreground="white",
            fieldbackground="#1e1e1e",
            borderwidth=0,
            rowheight=36
        )

        style.configure(
            "Treeview.Heading",
            background="#222222",
            foreground="white",
            relief="flat"
        )

        style.map(
            "Treeview",
            background=[
                ("selected", "#2d6ca2")
            ],
            foreground=[
                ("selected", "white")
            ]
        )

        self.tree = ttk.Treeview(
            left_frame,
            columns=(
                "index",
                "type",
                "details"
            ),
            show="headings"
        )

        self.tree.configure(
            selectmode="browse"
        )

        self.tree.heading("index", text="#")
        self.tree.heading("type", text="Event")
        self.tree.heading("details", text="Details")

        self.tree.column(
            "index",
            width=50,
            anchor="center"
        )

        self.tree.column(
            "type",
            width=150,
            anchor="center"
        )

        self.tree.column(
            "details",
            width=300,
            anchor="w"
        )

        self.tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.on_select
        )

        #
        # Drag & Drop
        #

        self.tree.bind(
            "<ButtonPress-1>",
            self.on_drag_start
        )

        self.tree.bind(
            "<B1-Motion>",
            self.on_drag_motion
        )

        self.tree.bind(
            "<ButtonRelease-1>",
            self.on_drag_drop
        )


        #RIGHT
        right_frame = ctk.CTkFrame(self)

        right_frame.grid(
            row=0,
            column=2,
            sticky="nsew",
            padx=10,
            pady=10
        )

        ctk.CTkLabel(
            right_frame,
            text="Properties",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=10)

        self.type_label = ctk.CTkLabel(
            right_frame,
            text="Type: None"
        )

        self.type_label.pack(
            pady=5
        )

        self.value1_label = ctk.CTkLabel(
            right_frame,
            text="Value 1"
        )

        self.value1_label.pack()

        self.value1_entry = ctk.CTkEntry(
            right_frame
        )

        self.value1_entry.pack(
            fill="x",
            padx=10,
            pady=5
        )

        self.value2_label = ctk.CTkLabel(
            right_frame,
            text="Value 2"
        )

        self.value2_label.pack()

        self.value2_entry = ctk.CTkEntry(
            right_frame
        )

        self.value2_entry.pack(
            fill="x",
            padx=10,
            pady=5
        )

        self.select_location_btn = ctk.CTkButton(
            right_frame,
            text="🎯 Capture Mouse Position",
            command=self.select_click_location
        )

        self.select_location_btn.pack_forget()

        self.value3_label = ctk.CTkLabel(
            right_frame,
            text="Value 3"
        )

        self.value3_label.pack()

        self.value3_entry = ctk.CTkEntry(
            right_frame
        )

        self.value3_entry.pack(
            fill="x",
            padx=10,
            pady=5
        )

        #
        # Image Event Dropdowns
        #

        self.image_combo = ctk.CTkComboBox(
            right_frame,
            values=[""]
        )

        self.region_combo = ctk.CTkComboBox(
            right_frame,
            values=[""]
        )

        #
        # Insert directly below labels
        #

        self.image_combo.pack(
            before=self.value2_label,
            fill="x",
            padx=10,
            pady=5
        )

        self.region_combo.pack(
            before=self.value3_label,
            fill="x",
            padx=10,
            pady=5
        )

        self.image_combo.pack_forget()
        self.region_combo.pack_forget()

        button_frame = ctk.CTkFrame(
            right_frame,
            fg_color="transparent"
        )

        button_frame.pack(
            side="bottom",
            fill="x",
            padx=10,
            pady=10
        )

        self.apply_btn = ctk.CTkButton(
            button_frame,
            text="✅ Apply Changes",
            command=self.apply_changes
        )

        self.apply_btn.pack(
            fill="x"
        )

        #
        # Actions
        #

        ctk.CTkLabel(
            toolbox_frame,
            text="Actions",
            font=("Segoe UI", 16, "bold")
        ).pack(
            pady=(10, 15)
        )

        #
        # Mouse
        #

        ctk.CTkLabel(
            toolbox_frame,
            text="Mouse",
            font=("Segoe UI", 14, "bold"),
            text_color="#4EA3FF"
        ).pack(
            fill="x",
            pady=(0, 5)
        )

        ctk.CTkButton(
            toolbox_frame,
            text="🖱 Click",
            command=self.add_click
        ).pack(
            fill="x",
            padx=10,
            pady=2
        )

        ctk.CTkButton(
            toolbox_frame,
            text="🖼 Click Image",
            command=self.add_click_image
        ).pack(
            fill="x",
            padx=10,
            pady=2
        )

        #
        # Timing
        #

        ctk.CTkLabel(
            toolbox_frame,
            text="Timing",
            font=("Segoe UI", 14, "bold"),
            text_color="#4EA3FF"
        ).pack(
            fill="x",
            pady=(12, 5)
        )

        ctk.CTkButton(
            toolbox_frame,
            text="⏱ Wait",
            command=self.add_wait
        ).pack(
            fill="x",
            padx=10,
            pady=2
        )

        ctk.CTkButton(
            toolbox_frame,
            text="👁 Wait Image",
            command=self.add_wait_image
        ).pack(
            fill="x",
            padx=10,
            pady=2
        )

        #
        # Keyboard
        #

        ctk.CTkLabel(
            toolbox_frame,
            text="Keyboard",
            font=("Segoe UI", 14, "bold"),
            text_color="#4EA3FF"
        ).pack(
            fill="x",
            pady=(12, 5)
        )

        ctk.CTkButton(
            toolbox_frame,
            text="⌨ Key",
            command=self.add_key
        ).pack(
            fill="x",
            padx=10,
            pady=2
        )

        #
        # Edit
        #

        ctk.CTkLabel(
            toolbox_frame,
            text="Edit",
            font=("Segoe UI", 14, "bold"),
            text_color="#4EA3FF"
        ).pack(
            fill="x",
            pady=(12, 5)
        )

        ctk.CTkButton(
            toolbox_frame,
            text="✏ Duplicate",
            command=self.duplicate_selected
        ).pack(
            fill="x",
            padx=10,
            pady=2
        )

        ctk.CTkButton(
            toolbox_frame,
            text="🗑 Delete",
            command=self.delete_selected,
            fg_color="#AA3333",
            hover_color="#882222"
        ).pack(
            fill="x",
            padx=10,
            pady=2
        )

    #
    # ADD EVENTS
    #

    def show_normal_properties(self):

        self.image_combo.pack_forget()
        self.region_combo.pack_forget()

        self.value1_label.pack_forget()
        self.value1_entry.pack_forget()

        self.value2_label.pack_forget()
        self.value2_entry.pack_forget()

        self.value3_label.pack_forget()
        self.value3_entry.pack_forget()

        self.value1_label.pack()

        self.value1_entry.pack(
            fill="x",
            padx=10,
            pady=5
        )

        self.value2_label.pack()

        self.value2_entry.pack(
            fill="x",
            padx=10,
            pady=5
        )

        self.value3_label.pack()

        self.value3_entry.pack(
            fill="x",
            padx=10,
            pady=5
        )

    def show_image_properties(self):

        self.value1_entry.pack_forget()
        self.value2_entry.pack_forget()

        self.image_combo.pack_forget()
        self.region_combo.pack_forget()

        self.image_combo.pack(
            before=self.value2_label,
            fill="x",
            padx=10,
            pady=5
        )

        self.region_combo.pack(
            before=self.value3_label,
            fill="x",
            padx=10,
            pady=5
        )

    def select_click_location(self):

        root = self.winfo_toplevel()

        root.withdraw()

        self.after(
            300,
            lambda: self._capture_click_location(root)
        )

    def _capture_click_location(self, root):

        selector = ClickSelector()

        result = selector.select()

        root.deiconify()

        root.lift()

        root.focus_force()

        if not result:
            return

        #
        # Update UI
        #

        self.value1_entry.delete(0, "end")
        self.value2_entry.delete(0, "end")

        self.value1_entry.insert(
            0,
            str(result["x"])
        )

        self.value2_entry.insert(
            0,
            str(result["y"])
        )

        #
        # Update event immediately
        #

        if self.selected_index is not None:
            self.events[self.selected_index]["x"] = result["x"]
            self.events[self.selected_index]["y"] = result["y"]

            self.refresh()

            self.tree.selection_set(
                str(self.selected_index)
            )

            self.tree.focus(
                str(self.selected_index)
            )

            self.on_select()

    def add_click(self):

        self.events.append(
            {
                "type": "click",
                "x": 500,
                "y": 500,
                "random_offset": 0
            }
        )

        self.selected_index = (
                len(self.events) - 1
        )

        self.refresh()

        self.on_select()

    def load_images(self):

        try:

            with open(
                    "images.json",
                    "r"
            ) as f:

                return list(
                    json.load(f).keys()
                )

        except:

            return []


    def load_regions(self):

        try:

            with open(
                    "regions.json",
                    "r"
            ) as f:

                return list(
                    json.load(f).keys()
                )

        except:

            return []

    def add_wait(self):

        self.events.append(
            {
                "type": "wait",
                "duration": 1000,
                "random_variance": 0
            }
        )

        self.selected_index = (
                len(self.events) - 1
        )

        self.refresh()

        self.on_select()

    def add_key(self):

        self.events.append(
            {
                "type": "keypress",
                "key": "f"
            }
        )

        self.selected_index = (
                len(self.events) - 1
        )

        self.refresh()

        self.on_select()

    def add_click_image(self):

        self.events.append(
            {
                "type": "click_image",
                "image": "",
                "region": "",
                "confidence": 0.85
            }
        )

        self.selected_index = (
                len(self.events) - 1
        )

        self.refresh()

        self.on_select()

    def add_wait_image(self):

        self.events.append(
            {
                "type": "wait_image",
                "image": "",
                "region": "",
                "confidence": 0.85
            }
        )

        self.selected_index = (
                len(self.events) - 1
        )

        self.refresh()

        self.on_select()

    #
    # SELECTION
    #

    def on_select(self, event=None):

        self.select_location_btn.pack_forget()

        selection = self.tree.selection()

        if not selection:
            return

        self.selected_index = int(
            selection[0]
        )

        evt = self.events[
            self.selected_index
        ]

        self.show_normal_properties()

        self.type_label.configure(
            text=f"Type: {evt['type']}"
        )

        self.value1_entry.delete(0, "end")
        self.value2_entry.delete(0, "end")
        self.value3_entry.delete(0, "end")

        self.value1_label.configure(text="Value 1")
        self.value2_label.configure(text="Value 2")
        self.value3_label.configure(text="Value 3")

        self.value3_entry.pack(
            fill="x",
            padx=10,
            pady=5
        )

        self.image_combo.pack_forget()
        self.region_combo.pack_forget()

        self.value1_entry.pack(
            fill="x",
            padx=10,
            pady=5
        )

        self.value2_entry.pack(
            fill="x",
            padx=10,
            pady=5
        )

        if evt["type"] == "click":

            self.show_normal_properties()

            self.value1_label.configure(
                text="X Position"
            )

            self.value2_label.configure(
                text="Y Position"
            )

            self.value3_label.pack_forget()
            self.value3_entry.pack_forget()

            self.value1_entry.insert(
                0,
                evt["x"]
            )

            self.value2_entry.insert(
                0,
                evt["y"]
            )

            self.select_location_btn.pack(
                pady=10
            )

            self.value3_label.configure(
                text="Random Offset"
            )

            self.value3_label.pack()

            self.value3_entry.pack(
                fill="x",
                padx=10,
                pady=5
            )

            self.value3_entry.insert(
                0,
                evt.get(
                    "random_offset",
                    0
                )
            )

        elif evt["type"] == "wait":

            self.show_normal_properties()

            self.value1_label.configure(
                text="Duration (ms)"
            )

            self.value2_label.configure(
                text="Random Variance (ms)"
            )

            self.value3_label.pack_forget()
            self.value3_entry.pack_forget()

            self.value1_entry.insert(
                0,
                evt["duration"]
            )

            self.value2_entry.insert(
                0,
                evt.get(
                    "random_variance",
                    0
                )
            )

        elif evt["type"] == "keypress":

            self.show_normal_properties()

            self.value1_label.configure(
                text="Key"
            )

            self.value2_label.pack_forget()
            self.value2_entry.pack_forget()

            self.value3_label.pack_forget()
            self.value3_entry.pack_forget()

            self.value1_entry.insert(
                0,
                evt["key"]
            )

        elif evt["type"] in (
            "click_image",
            "wait_image"
        ):

            self.value1_label.configure(
                text="Image Alias"
            )

            self.value2_label.configure(
                text="Region"
            )

            self.value3_label.configure(
                text="Confidence"
            )

            self.show_image_properties()

            self.image_combo.configure(
                values=self.load_images()
            )

            self.region_combo.configure(
                values=self.load_regions()
            )

            self.image_combo.set(
                evt.get("image", "")
            )

            self.region_combo.set(
                evt.get("region", "")
            )

            self.image_combo.pack_forget()
            self.region_combo.pack_forget()

            self.image_combo.pack(
                before=self.value2_label,
                fill="x",
                padx=10,
                pady=5
            )

            self.region_combo.pack(
                before=self.value3_label,
                fill="x",
                padx=10,
                pady=5
            )

            self.value3_entry.delete(
                0,
                "end"
            )

            self.value3_entry.insert(
                0,
                str(
                    evt.get(
                        "confidence",
                        0.85
                    )
                )
            )

    #
    # APPLY
    #

    def apply_changes(self):

        if self.selected_index is None:
            return

        evt = self.events[
            self.selected_index
        ]

        try:

            if evt["type"] == "click":

                evt["x"] = int(
                    self.value1_entry.get()
                )

                evt["y"] = int(
                    self.value2_entry.get()
                )

                evt["random_offset"] = int(
                    self.value3_entry.get()
                )

            elif evt["type"] == "wait":

                evt["duration"] = int(
                    self.value1_entry.get()
                )

                evt["random_variance"] = int(
                    self.value2_entry.get()
                )

            elif evt["type"] == "keypress":

                evt["key"] = (
                    self.value1_entry.get()
                )

            elif evt["type"] in (
                    "click_image",
                    "wait_image"
            ):

                evt["image"] = (
                    self.image_combo.get()
                )

                evt["region"] = (
                    self.region_combo.get()
                )

                evt["confidence"] = float(
                    self.value3_entry.get()
                )

            self.refresh()

        except Exception as e:

            print(e)

    #
    # DELETE
    #

    def delete_selected(self):

        if self.selected_index is None:
            return

        del self.events[
            self.selected_index
        ]

        self.selected_index = None

        self.refresh()

    #
    # DUPLICATE
    #

    def duplicate_selected(self):

        if self.selected_index is None:
            return

        self.events.insert(
            self.selected_index + 1,
            self.events[self.selected_index].copy()
        )

        self.selected_index += 1

        self.refresh()

        self.on_select()

    #
    # DRAG
    #

    def on_drag_start(self, event):

        item = self.tree.identify_row(
            event.y
        )

        if item:
            self.drag_item = int(item)

    def on_drag_motion(self, event):

        item = self.tree.identify_row(
            event.y
        )

        if item:
            self.tree.selection_set(item)

    def on_drag_drop(self, event):

        if self.drag_item is None:
            return

        target = self.tree.identify_row(
            event.y
        )

        if not target:
            return

        target = int(target)

        event_obj = self.events.pop(
            self.drag_item
        )

        self.events.insert(
            target,
            event_obj
        )

        self.drag_item = None

        self.refresh()

    #
    # REFRESH
    #

    def refresh(self):

        selected = self.selected_index

        DISPLAY_NAMES = {
            "click": "🖱 Mouse Click",
            "wait": "⏱ Wait",
            "keypress": "⌨ Key Press",
            "click_image": "🖼 Click Image",
            "wait_image": "👁 Wait For Image"
        }

        self.tree.delete(
            *self.tree.get_children()
        )

        for i, event in enumerate(
            self.events
        ):

            details = ""

            if event["type"] == "click":

                details = (
                    f"{event['x']},{event['y']}"
                )

                offset = event.get(
                    "random_offset",
                    0
                )

                if offset > 0:
                    details += (
                        f"  ±{offset}px"
                    )

            elif event["type"] == "wait":

                base = event["duration"]

                variance = event.get(
                    "random_variance",
                    0
                )

                details = (
                    f"{base}ms"
                )

                if variance > 0:
                    details += (
                        f" ±{variance}ms"
                    )


            elif event["type"] == "keypress":

                details = event["key"]

            elif event["type"] in (
                "click_image",
                "wait_image"
            ):

                image = event.get(
                    "image",
                    "None"
                )

                confidence = event.get(
                    "confidence",
                    0.85
                )

                region = event.get(
                    "region",
                    ""
                )

                details = image

                if region:
                    details += f" [{region}]"

                details += f" ({confidence:.2f})"

            event_name = DISPLAY_NAMES.get(
                event["type"],
                event["type"]
            )

            self.tree.insert(
                "",
                "end",
                iid=str(i),
                values=(
                    i + 1,
                    event_name,
                    details
                )
            )

        if (
                selected is not None
                and str(selected) in self.tree.get_children()
        ):
            self.tree.selection_set(
                str(selected)
            )

            self.tree.focus(
                str(selected)
            )

            self.tree.see(
                str(selected)
            )

            self.selected_index = selected
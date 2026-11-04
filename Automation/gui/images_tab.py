import json
import tkinter as tk
import customtkinter as ctk
import os

from PIL import Image
from tkinter import filedialog
from core.image_analyzer import ImageAnalyzer


class ImagesTab(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.images = {}
        self.load()

        self.analyzer = ImageAnalyzer()

        self.build_ui()

    def build_ui(self):

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(1, weight=1)

        #
        # Title
        #

        title = ctk.CTkLabel(
            self,
            text="Image Library",
            font=("Segoe UI", 20, "bold")
        )

        title.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=10
        )

        #
        # LEFT PANEL
        #

        left_frame = ctk.CTkFrame(self)

        left_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(10, 5),
            pady=10
        )

        ctk.CTkLabel(
            left_frame,
            text="Images",
            font=("Segoe UI", 16, "bold")
        ).pack(
            pady=(10, 5)
        )

        self.image_list = tk.Listbox(
            left_frame,
            bg="#1b1b1b",
            fg="white",
            selectbackground="#2d6ca2",
            selectforeground="white",
            borderwidth=0,
            highlightthickness=0,
            font=("Segoe UI", 11)
        )

        self.image_list.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        self.image_list.bind(
            "<<ListboxSelect>>",
            self.on_image_select
        )

        #
        # RIGHT PANEL
        #

        right_frame = ctk.CTkScrollableFrame(self)

        right_frame.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(5, 10),
            pady=10
        )

        ctk.CTkLabel(
            right_frame,
            text="Preview",
            font=("Segoe UI", 16, "bold")
        ).pack(
            pady=(10, 5)
        )

        #
        # Image Preview Placeholder
        #

        self.preview_frame = ctk.CTkFrame(
            right_frame
        )

        self.preview_frame.pack(
            fill="both",
            padx=10,
            pady=5
        )

        self.preview_label = ctk.CTkLabel(
            self.preview_frame,
            text="No Image Selected"
        )

        self.preview_label.pack(
            fill="both",
            expand=True
        )

        #
        # Image Information
        #

        self.alias_label = ctk.CTkLabel(
            right_frame,
            text="Alias: None"
        )

        self.alias_label.pack(
            pady=(5, 2)
        )

        self.path_label = ctk.CTkLabel(
            right_frame,
            text="Path: None",
            wraplength=450
        )

        self.path_label.pack(
            padx=10,
            pady=2
        )

        self.size_label = ctk.CTkLabel(
            right_frame,
            text="Resolution: -"
        )

        self.size_label.pack(
            pady=2
        )

        self.analysis_label = ctk.CTkLabel(
            right_frame,
            text="Match Quality: Not Tested",
            justify="left"
        )

        self.analysis_label.pack(
            padx=10,
            pady=10
        )

        self.region_label = ctk.CTkLabel(
            right_frame,
            text="Analysis Region"
        )

        self.region_label.pack(
            pady=(5, 0)
        )

        regions = self.load_regions()

        region_values = [
            "Entire Screen"
        ]

        region_values.extend(
            regions.keys()
        )

        self.region_combo = ctk.CTkComboBox(
            right_frame,
            values=region_values
        )

        self.region_combo.pack(
            padx=10,
            pady=5
        )

        self.region_combo.set(
            "Entire Screen"
        )

        #
        # Actions
        #

        ctk.CTkLabel(
            right_frame,
            text="Actions",
            font=("Segoe UI", 16, "bold")
        ).pack(
            pady=(15, 5)
        )

        buttons_frame = ctk.CTkFrame(
            right_frame,
            fg_color="transparent"
        )

        buttons_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        ctk.CTkButton(
            buttons_frame,
            text="📁 Add Image",
            command=self.add_image
        ).pack(
            fill="x",
            pady=2
        )

        ctk.CTkButton(
            buttons_frame,
            text="🔄 Replace Image",
            command=self.replace_image
        ).pack(
            fill="x",
            pady=2
        )

        ctk.CTkButton(
            buttons_frame,
            text="🔍 Analyze Match",
            command=self.analyze_match
        ).pack(
            fill="x",
            pady=2
        )

        ctk.CTkButton(
            buttons_frame,
            text="🗑 Delete Image",
            command=self.delete_image,
            fg_color="#AA3333",
            hover_color="#882222"
        ).pack(
            fill="x",
            pady=2
        )

        self.refresh()

    def refresh(self):

        self.image_list.delete(
            0,
            "end"
        )

        for alias in sorted(
                self.images.keys()
        ):
            self.image_list.insert(
                "end",
                alias
            )

        if self.image_list.size() > 0:
            self.image_list.selection_set(0)

            self.on_image_select()

    def save(self):

        with open(
            "images.json",
            "w"
        ) as f:

            json.dump(
                self.images,
                f,
                indent=4
            )

    def add_image(self):

        path = filedialog.askopenfilename(
            filetypes=[
                (
                    "Images",
                    "*.png *.jpg *.jpeg"
                )
            ]
        )

        if not path:
            return

        alias = os.path.splitext(
            os.path.basename(path)
        )[0]

        self.images[alias] = path

        self.save()

        self.refresh()

    def replace_image(self):

        selection = self.image_list.curselection()

        if not selection:
            return

        alias = self.image_list.get(
            selection[0]
        )

        path = filedialog.askopenfilename(
            filetypes=[
                (
                    "Images",
                    "*.png *.jpg *.jpeg"
                )
            ]
        )

        if not path:
            return

        self.images[alias] = path

        self.save()

        self.refresh()

    def delete_image(self):

        selection = self.image_list.curselection()

        if not selection:
            return

        alias = self.image_list.get(
            selection[0]
        )

        del self.images[alias]

        self.save()

        self.refresh()

        self.preview_label.configure(
            image=None,
            text="No Image Selected"
        )

        self.alias_label.configure(
            text="Alias: None"
        )

        self.path_label.configure(
            text="Path: None"
        )

        self.size_label.configure(
            text="Resolution: -"
        )

    def on_image_select(self, event=None):

        selection = self.image_list.curselection()

        if not selection:
            return

        alias = self.image_list.get(
            selection[0]
        )

        path = self.images.get(alias)

        self.alias_label.configure(
            text=f"Alias: {alias}"
        )

        self.path_label.configure(
            text=f"Path: {path}"
        )

        try:

            img = Image.open(path)

            width, height = img.size

            self.size_label.configure(
                text=f"Resolution: {width} x {height}"
            )

            self.update_idletasks()

            preview_width = max(
                self.preview_frame.winfo_width() - 20,
                100
            )

            preview_height = max(
                self.preview_frame.winfo_height() - 20,
                100
            )

            img.thumbnail(
                (
                    preview_width,
                    preview_height
                )
            )

            preview = ctk.CTkImage(
                light_image=img,
                dark_image=img,
                size=img.size
            )

            self.preview_label.configure(
                image=preview,
                text=""
            )

            self.preview_label.image = preview

        except Exception as e:

            print(
                "Preview error:",
                e
            )

    def load(self):

        try:

            with open(
                "images.json",
                "r"
            ) as f:

                self.images = json.load(f)

        except:

            self.images = {}

    def load_regions(self):
        try:
            with open(
                    "regions.json",
                    "r"
            ) as f:
                return json.load(f)
        except:
            return {}

    def analyze_match(self):

        selection = self.image_list.curselection()

        if not selection:
            return

        alias = self.image_list.get(
            selection[0]
        )

        image_path = self.images.get(
            alias
        )

        regions = self.load_regions()

        region_name = (
            self.region_combo.get()
        )

        region = None

        if (
                region_name
                != "Entire Screen"
        ):
            region = regions.get(
                region_name
            )

        confidence = self.analyzer.analyze(
            image_path,
            region
        )

        if confidence is None:
            self.analysis_label.configure(
                text=
                "❌ Unable to analyze image"
            )

            return

        if confidence >= 0.90:
            status = "✅ Excellent"

        elif confidence >= 0.75:
            status = "✅ Good"

        elif confidence >= 0.60:
            status = "⚠ Acceptable"

        elif confidence >= 0.40:
            status = "⚠ Weak"

        else:
            status = "❌ Replace Image"

        recommended_threshold = max(
            0.40,
            round(
                confidence - 0.05,
                2
            )
        )

        if confidence < 0.40:

            recommendation = (
                "Replace image.\n"
                "Match quality extremely poor."
            )

        elif confidence < 0.60:

            recommendation = (
                "Capture more context.\n"
                "Include slot borders."
            )

        elif confidence < 0.75:

            recommendation = (
                "Usable but may miss detections."
            )

        else:

            recommendation = (
                "Image quality acceptable."
            )

        self.analysis_label.configure(

            text=
            f"Confidence: {confidence:.3f}\n\n"
            f"{status}\n\n"
            f"Recommended Threshold: "
            f"{recommended_threshold}\n\n"
            f"{recommendation}"
        )
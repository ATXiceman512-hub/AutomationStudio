import customtkinter as ctk
import time
from PIL import Image


from tkinter import filedialog
from tkinter import END

from gui.macro_editor import MacroEditor
from gui.status_overlay import StatusOverlay

from gui.images_tab import ImagesTab
from gui.regions_tab import RegionsTab

from core.macro_engine import MacroEngine
from core.macro_storage import MacroStorage


class MainWindow:

    def __init__(self, root):

        self.root = root
        self.start_time = None
        self.pause_start = None

        self.root.title(
            "Automation Studio"
        )

        self.root.geometry(
            "900x700+50+50"
        )

        self.bg_image = ctk.CTkImage(
            light_image=Image.open(
                "assets/background.png"
            ),
            dark_image=Image.open(
                "assets/background.png"
            ),
            size=(1400, 900)
        )

        self.engine = MacroEngine()
        self.engine.executor.log_callback = self.log
        self.engine.on_finished = self.macro_finished
        self.engine.on_action = self.update_action

        self.status_var = ctk.StringVar(
            value="Ready"
        )

        self.action_var = ctk.StringVar(
            value="Action: None"
        )

        self.timer_var = ctk.StringVar(
            value="00:00:00"
        )

        self.build_ui()

        self.overlay_visible = False

        self.monitor_window_state()

    def monitor_window_state(self):

        try:

            is_minimized = (
                    self.root.state() == "iconic"
            )

            if (
                    is_minimized
                    and not self.overlay_visible
            ):

                self.overlay.deiconify()

                self.overlay.lift()

                self.overlay_visible = True

            elif (
                    not is_minimized
                    and self.overlay_visible
            ):

                self.overlay.withdraw()

                self.overlay_visible = False

        except Exception as e:

            print(
                "Overlay Error:",
                e
            )

        self.root.after(
            500,
            self.monitor_window_state
        )

    def log(self, message):

        timestamp = time.strftime(
            "%H:%M:%S"
        )

        self.log_box.configure(
            state="normal"
        )

        self.log_box.insert(
            "end",
            f"[{timestamp}] {message}\n"
        )

        self.log_box.see("end")

        self.log_box.configure(
            state="disabled"
        )

    def macro_finished(self):

        self.root.after(
            0,
            self._macro_finished_ui
        )

    def _macro_finished_ui(self):

        self.status_var.set(
            "Stopped"
        )

        self.action_var.set(
            "Action: None"
        )

        self.timer_var.set(
            "00:00:00"
        )

        self.start_time = None

    def update_action(self, event):

        event_type = event.get(
            "type",
            "Unknown"
        )

        display_names = {

            "click": "🖱 Mouse Click",
            "wait": "⏱ Wait",
            "keypress": "⌨ Key Press",
            "click_image": "🖼 Click Image",
            "wait_image": "👁 Wait For Image"

        }

        action_text = display_names.get(
            event_type,
            event_type
        )

        self.root.after(
            0,
            lambda:
            self.action_var.set(
                f"Action: {action_text}"
            )
        )

        self.overlay.action_label.configure(
            text=action_text
        )

    def build_ui(self):

        self.bg_label = ctk.CTkLabel(
            self.root,
            image=self.bg_image,
            text=""
        )

        self.bg_label.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )

        self.tabs = ctk.CTkTabview(
            self.root
        )

        self.tabs.add(
            "Workflow"
        )

        self.tabs.add(
            "Images"
        )

        self.tabs.add(
            "Regions"
        )

        self.tabs.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.editor = MacroEditor(
            self.tabs.tab(
                "Workflow"
            )
        )

        self.editor.pack(
            fill="both",
            expand=True
        )

        self.images = ImagesTab(
            self.tabs.tab(
                "Images"
            )
        )

        self.images.pack(
            fill="both",
            expand=True
        )

        self.regions = RegionsTab(
            self.tabs.tab(
                "Regions"
            )
        )

        self.regions.pack(
            fill="both",
            expand=True
        )

        #
        # Bottom Controls
        #

        controls = ctk.CTkFrame(
            self.root,
            fg_color="#222222"
        )

        controls.pack(
            fill="x",
            padx=10,
            pady=5
        )

        ctk.CTkButton(
            controls,
            text="▶ Run (F5)",
            command=self.run_macro
        ).pack(side="left", padx=5)

        self.root.bind(
            "<F5>",
            lambda e: self.run_macro()
        )

        ctk.CTkButton(
            controls,
            text="⏸ Pause (F6)",
            command=self.pause_macro
        ).pack(side="left", padx=5)

        self.root.bind(
            "<F6>",
            lambda e: self.pause_macro()
        )

        ctk.CTkButton(
            controls,
            text="▶ Resume (F7)",
            command=self.resume_macro
        ).pack(side="left", padx=5)

        self.root.bind(
            "<F7>",
            lambda e: self.resume_macro()
        )

        ctk.CTkButton(
            controls,
            text="■ Stop (F8)",
            fg_color="red",
            command=self.stop_macro
        ).pack(side="left", padx=5)

        self.root.bind(
            "<F8>",
            lambda e: self.stop_macro()
        )

        ctk.CTkButton(
            controls,
            text="💾 Save (Ctrl+S)",
            command=self.save_macro
        ).pack(side="right", padx=5)

        self.root.bind(
            "<Control-s>",
            lambda e: self.save_macro()
        )

        ctk.CTkButton(
            controls,
            text="📂 Load (Ctrl+O)",
            command=self.load_macro
        ).pack(side="right", padx=5)

        self.root.bind(
            "<Control-o>",
            lambda e: self.load_macro()
        )

        self.log_box = ctk.CTkTextbox(
            self.root,
            height=120
        )

        self.log_box.pack(
            fill="x",
            padx=10,
            pady=(0, 5)
        )

        self.log_box.insert(
            "end",
            "[SYSTEM] Logger initialized\n"
        )

        self.log_box.configure(
            state="disabled"
        )

        status_bar = ctk.CTkFrame(
            self.root,
            height=30
        )

        status_bar.pack(
            fill="x",
            side="bottom",
            padx=10,
            pady=(0, 5)
        )

        ctk.CTkLabel(
            status_bar,
            textvariable=self.status_var
        ).pack(
            side="left",
            padx=10
        )

        ctk.CTkLabel(
            status_bar,
            textvariable=self.action_var
        ).pack(
            side="right",
            padx=10
        )

        ctk.CTkLabel(
            status_bar,
            textvariable=self.timer_var
        ).pack(
            side="right",
            padx=10
        )

        self.overlay = StatusOverlay(
            self.root
        )

        self.overlay.withdraw()

    def run_macro(self):

        macro = {
            "events": self.editor.events
        }

        self.engine.start(macro)

        self.status_var.set("Running")

        self.start_time = time.time()

        self.update_timer()

        self.log(
            "Macro Started"
        )

        self.overlay.status_label.configure(
            text="✅ Running"
        )

    def update_timer(self):

        if not self.engine.running:
            return

        elapsed = int(
            time.time() - self.start_time
        )

        hours = elapsed // 3600
        minutes = (elapsed % 3600) // 60
        seconds = elapsed % 60

        self.timer_var.set(
            f"{hours:02}:{minutes:02}:{seconds:02}"
        )

        self.root.after(
            1000,
            self.update_timer
        )

    def stop_macro(self):

        self.engine.stop()

        self.status_var.set(
            "Stopped"
        )

        self.action_var.set(
            "Action: None"
        )

        self.timer_var.set(
            "00:00:00"
        )

        self.start_time = None

        self.log(
            "Macro Stopped"
        )

        self.overlay.status_label.configure(
            text="⛔ Stopped"
        )

    def pause_macro(self):

        self.engine.pause()

        self.pause_start = time.time()

        self.status_var.set(
            "Paused"
        )

        self.overlay.status_label.configure(
            text="⏸ Paused"
        )

    def resume_macro(self):

        self.engine.resume()

        if self.pause_start:
            paused_time = (
                    time.time()
                    - self.pause_start
            )

            self.start_time += paused_time

            self.pause_start = None

        self.status_var.set(
            "Running"
        )

    def save_macro(self):

        path = filedialog.asksaveasfilename(
            defaultextension=".json"
        )

        if not path:
            return

        MacroStorage.save(
            path,
            self.editor.events
        )

        self.status_var.set(
            "Macro Saved"
        )

    def load_macro(self):

        path = filedialog.askopenfilename(
            filetypes=[
                ("JSON", "*.json")
            ]
        )

        if not path:
            return

        data = MacroStorage.load(
            path
        )

        self.editor.events = data.get(
            "events",
            []
        )

        self.editor.refresh()

        self.status_var.set(
            "Macro Loaded"
        )
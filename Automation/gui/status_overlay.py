import customtkinter as ctk


class StatusOverlay(ctk.CTkToplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.parent = parent

        self.title("Automation Studio")

        self.geometry(
            "220x200+20+20"
        )

        self.attributes(
            "-topmost",
            True
        )

        self.resizable(
            False,
            False
        )

        #
        # Title
        #

        ctk.CTkLabel(
            self,
            text="Automation Studio",
            font=("Segoe UI", 14, "bold")
        ).pack(
            pady=(5, 2)
        )

        #
        # Status
        #

        self.status_label = ctk.CTkLabel(
            self,
            text="⛔ Stopped",
            font=("Segoe UI", 13, "bold"),
            text_color="#FF5252"
        )

        self.status_label.pack(
            pady=(2, 1)
        )

        #
        # Current Action
        #

        self.action_label = ctk.CTkLabel(
            self,
            text="Idle"
        )

        self.action_label.pack(
            pady=1
        )

        #
        # Runtime / Event Count
        #

        self.info_label = ctk.CTkLabel(
            self,
            text="⏱ 00:00:00 | 0/0"
        )

        self.info_label.pack(
            pady=1
        )

        #
        # Buttons
        #

        buttons_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        buttons_frame.pack(
            fill="x",
            padx=5,
            pady=(3, 5)
        )

        self.pause_button = ctk.CTkButton(
            buttons_frame,
            text="⏸",
            width=40
        )

        self.pause_button.pack(
            side="left",
            expand=True,
            padx=2
        )

        self.stop_button = ctk.CTkButton(
            buttons_frame,
            text="■",
            width=40,
            fg_color="red"
        )

        self.stop_button.pack(
            side="left",
            expand=True,
            padx=2
        )

        self.open_button = ctk.CTkButton(
            buttons_frame,
            text="🖥",
            width=40,
            command=self.restore_main
        )

        self.open_button.pack(
            side="left",
            expand=True,
            padx=2
        )

        #
        # Prevent destruction
        #

        self.protocol(
            "WM_DELETE_WINDOW",
            self.withdraw
        )

    def restore_main(self):

        self.parent.deiconify()

        self.parent.lift()

        self.parent.focus_force()

        self.withdraw()
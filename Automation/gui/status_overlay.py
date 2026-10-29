import customtkinter as ctk


class StatusOverlay(ctk.CTkToplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.parent = parent


    def __init__(self, parent):

        super().__init__(parent)

        self.title("Automation Status")

        self.geometry("250x120+20+20")

        self.attributes(
            "-topmost",
            True
        )

        self.resizable(
            False,
            False
        )

        self.status_label = ctk.CTkLabel(
            self,
            text="Stopped"
        )

        self.status_label.pack(
            pady=10
        )

        self.action_label = ctk.CTkLabel(
            self,
            text="Idle"
        )

        self.action_label.pack(
            pady=5
        )

        ctk.CTkButton(
            self,
            text="Open Studio",
            command=self.restore_main
        ).pack(
            pady=10
        )

    def restore_main(self):
        self.parent.deiconify()

        self.withdraw()
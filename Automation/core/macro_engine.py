import threading
import time

from core.event_executor import EventExecutor


class MacroEngine:

    def __init__(self):

        self.running = False
        self.paused = False

        self.executor = EventExecutor()

        self.on_action = None
        self.on_finished = None

    def start(self, macro):

        if self.running:
            return

        self.running = True

        threading.Thread(
            target=self.run,
            args=(macro,),
            daemon=True
        ).start()

    def stop(self):

        self.running = False

    def pause(self):

        self.paused = True

    def resume(self):

        self.paused = False

    def run(self, macro):

        while self.running:

            for event in macro["events"]:

                if not self.running:
                    break

                while self.paused:

                    if not self.running:
                        break

                    time.sleep(0.1)

                try:

                    if self.on_action:
                        self.on_action(event)

                except Exception as e:

                    print(
                        "ACTION CALLBACK ERROR:",
                        e
                    )

                print(
                    "EXECUTING EVENT:",
                    event
                )

                try:

                    self.executor.execute(
                        event
                    )

                except Exception as e:

                    print(
                        "EXECUTOR ERROR:",
                        e
                    )

                    import traceback

                    traceback.print_exc()

                print(
                    "EVENT COMPLETE"
                )

        self.running = False

        if self.on_finished:
            self.on_finished()
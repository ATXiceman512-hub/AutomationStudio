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

                if self.on_action:
                    self.on_action(event)

                self.executor.execute(event)

        self.running = False

        if self.on_finished:
            self.on_finished()
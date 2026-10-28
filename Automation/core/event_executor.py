import json
import time
import random

import pyautogui

from core.detector import Detector


class EventExecutor:

    def __init__(self):

        self.detector = Detector()

        self.log_callback = None

    def log(self, message):

        if self.log_callback:
            self.log_callback(message)

    def load_image_path(self, alias):

        try:

            with open(
                "images.json",
                "r"
            ) as f:

                images = json.load(f)

            return images.get(alias)

        except:

            return None

    def load_region(self, name):

        if not name:
            return None

        try:

            with open(
                "regions.json",
                "r"
            ) as f:

                regions = json.load(f)

            return regions.get(name)

        except:

            return None

    def execute(self, event):

        event_type = event.get("type")

        #
        # Mouse Events
        #

        if event_type == "click":

            offset = event.get(
                "random_offset",
                0
            )

            click_x = (
                    event["x"]
                    + random.randint(
                -offset,
                offset
            )
            )

            click_y = (
                    event["y"]
                    + random.randint(
                -offset,
                offset
            )
            )

            self.log(
                f"Mouse Click -> ({click_x}, {click_y})"
            )

            pyautogui.click(
                click_x,
                click_y,
            )

            time.sleep(2)

        elif event_type == "double_click":

            pyautogui.doubleClick(
                event["x"],
                event["y"]
            )

        elif event_type == "right_click":

            pyautogui.rightClick(
                event["x"],
                event["y"]
            )

        elif event_type == "move_mouse":

            pyautogui.moveTo(
                event["x"],
                event["y"],
                duration=0.25
            )

        #
        # Keyboard Events
        #

        elif event_type == "keypress":

            self.log(
                f"Key Press -> {event['key']}"
            )

            pyautogui.press(
                event["key"]
            )

        elif event_type == "write":

            pyautogui.write(
                event["text"]
            )

        elif event_type == "hotkey":

            pyautogui.hotkey(
                *event["keys"]
            )

        #
        # Wait
        #

        elif event_type == "wait":

            self.log(
                f"Waiting {event['duration']}ms"
            )

            time.sleep(
                event["duration"] / 1000
            )

        #
        # Scroll
        #

        elif event_type == "scroll":

            pyautogui.scroll(
                event["amount"]
            )

        #
        # Image Events
        #

        elif event_type == "wait_image":

            image_path = self.load_image_path(
                event["image"]
            )

            if not image_path:
                return

            region = self.load_region(
                event.get(
                    "region",
                    ""
                )
            )

            self.log(
                f"Waiting For Image -> {event['image']}"
            )

            while True:

                pos = self.detector.find_image(
                    image_path=image_path,
                    confidence=event.get(
                        "confidence",
                        0.85
                    ),
                    region=region
                )

                if pos:
                    self.log(
                        f"Image Found -> {event['image']}"
                    )

                    break

                time.sleep(0.1)

        elif event_type == "click_image":

            image_path = self.load_image_path(
                event["image"]
            )

            if not image_path:
                return

            region = self.load_region(
                event.get(
                    "region",
                    ""
                )
            )

            pos = self.detector.find_image(
                image_path=image_path,
                confidence=event.get(
                    "confidence",
                    0.85
                ),
                region=region
            )

            if pos:
                self.log(
                    f"Image Found -> {event['image']}"
                )

                pyautogui.click(
                    pos[0],
                    pos[1]
                )

                self.log(
                    f"Clicked Image -> ({pos[0]}, {pos[1]})"
                )
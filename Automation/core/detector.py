import cv2
import mss
import numpy as np


class Detector:

    def __init__(self):

        self.sct = mss.mss()

    def find_image(
        self,
        image_path,
        confidence=0.85,
        region=None
    ):

        template = cv2.imread(image_path)

        if template is None:
            return None

        if region:

            monitor = {
                "left": region["x"],
                "top": region["y"],
                "width": region["width"],
                "height": region["height"]
            }

        else:

            monitor = self.sct.monitors[1]

        screenshot = np.array(
            self.sct.grab(monitor)
        )

        screenshot = cv2.cvtColor(
            screenshot,
            cv2.COLOR_BGRA2BGR
        )

        result = cv2.matchTemplate(
            screenshot,
            template,
            cv2.TM_CCOEFF_NORMED
        )

        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val < confidence:
            return None

        h, w = template.shape[:2]

        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2

        #
        # Offset coordinates if using a region
        #

        if region:

            center_x += region["x"]
            center_y += region["y"]

        return center_x, center_y
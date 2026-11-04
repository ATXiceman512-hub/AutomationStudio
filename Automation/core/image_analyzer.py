import cv2
import mss
import numpy as np


class ImageAnalyzer:

    def analyze(
        self,
        image_path,
        region=None
    ):

        template = cv2.imread(
            image_path
        )

        if template is None:
            return None

        sct = mss.mss()

        if region:

            monitor = {
                "left": region["x"],
                "top": region["y"],
                "width": region["width"],
                "height": region["height"]
            }

        else:

            monitor = sct.monitors[1]

        screenshot = np.array(
            sct.grab(monitor)
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

        _, max_val, _, _ = cv2.minMaxLoc(
            result
        )

        return round(
            float(max_val),
            3
        )
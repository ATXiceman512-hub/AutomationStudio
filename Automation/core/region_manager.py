import json
import os


class RegionManager:

    def __init__(self):

        self.file = "regions.json"

        self.regions = {}

        self.load()

    def load(self):

        if not os.path.exists(self.file):

            self.regions = {}

            return

        with open(
            self.file,
            "r"
        ) as f:

            self.regions = json.load(f)

    def save(self):

        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                self.regions,
                f,
                indent=4
            )

    def add_region(
        self,
        name,
        x,
        y,
        width,
        height
    ):

        self.regions[name] = {

            "x": int(x),
            "y": int(y),
            "width": int(width),
            "height": int(height)
        }

        self.save()

    def delete_region(
        self,
        name
    ):

        if name in self.regions:

            del self.regions[name]

            self.save()

    def get_region(
        self,
        name
    ):

        return self.regions.get(name)

    def get_names(self):

        return list(
            self.regions.keys()
        )
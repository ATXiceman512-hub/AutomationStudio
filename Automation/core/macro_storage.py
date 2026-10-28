import json


class MacroStorage:

    @staticmethod
    def save(path, events):

        data = {
            "events": events
        }

        with open(path, "w") as f:

            json.dump(
                data,
                f,
                indent=4
            )

    @staticmethod
    def load(path):

        with open(path, "r") as f:

            return json.load(f)
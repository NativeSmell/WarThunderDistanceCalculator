import os


class ParamsReader:

    def __init__(self, name="settings.ini"):
        self.params = {}
        self.name = name

    def update_param(self, key, value):
        self.params[key] = value

    def get_param(self, key, _type=str):
        if key in self.params:
            return _type(self.params[key])
        return

    def load_params(self):
        if os.path.isfile(self.name):
            with open("settings.ini", "rt") as f:
                for line in f:
                    line = line.replace(" ", "").replace("\n", "")
                    if line[0] != "#" and line.count("=") == 1:
                        key, value = line.split("=")
                        self.params.update({key: value})

    def save_params(self):
        with open(self.name, "wt") as f:
            for key,value in self.params.items():
                f.write(str(key) + "=" + str(value) + "\n")



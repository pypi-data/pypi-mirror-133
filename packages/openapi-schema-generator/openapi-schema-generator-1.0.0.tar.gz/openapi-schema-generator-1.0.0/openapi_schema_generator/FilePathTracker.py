import os
import yaml
import json


class FilePathTracker(object):
    def __init__(self, path):
        self.slash = "/"
        self.path = os.path.abspath(path).replace("\\", self.slash)
        self.base_path = self.get_base_path()
        self.memorial_base_path = self.base_path
        self.curr_key = None
        self.last_file = None

    def get_base_path(self):
        temp_list = self.path.split(self.slash)
        return self.slash.join(temp_list[:len(temp_list) - 1])

    def get_root_data(self):
        return self.read_file(self.path)

    # ********************************** FETCH DATA ****************************** #
    @staticmethod
    def read_file(path):
        if "yml" in path or "yaml" in path:
            with open(path, "r", encoding='utf8') as f:
                return yaml.load(f, yaml.FullLoader)
        if "json" in path:
            with open(path, "r", encoding='utf8') as f:
                return json.load(f)

    def fetch_node_data(self, name):
        full_path = self.track_after_path(name)
        return self.read_file(full_path)

    # ******************************* TRACK FILE PATH ****************************** #

    @staticmethod
    def count_folder_backward(path):
        counter = 0
        for elem in path.split("/"):
            if elem == "..":
                counter += 1
            else:
                break
        return counter

    def count_folder_we_went_forward(self):
        return len(self.memorial_base_path.split("/")) - len(self.base_path.split("/"))

    @staticmethod
    def get_file_name(path):
        return path.split("/")[-1]

    def track_after_path(self, name):
        if not name:
            return self.last_file
        name = name.replace("\\", "/")
        if name[0] == "." and name[1] != ".":
            list_of_dirs = name.split(self.slash)[1:-1]
            if len(list_of_dirs) > 0:
                if self.count_folder_we_went_forward() < 0:
                    self.base_path = \
                        self.slash.join(self.base_path.split(self.slash)[:self.count_folder_we_went_forward()])
                self.base_path = f"{self.base_path}{self.slash}{self.slash.join(list_of_dirs)}"
            return f"{self.base_path}{self.slash}{self.get_file_name(name)}"

        if name[0] == "." and name[1] == ".":
            num_of_back_fold = self.count_folder_backward(name)
            temp_base_path = self.slash.join(self.base_path.split(self.slash)[:num_of_back_fold * -1])
            temp_base_path = f"{temp_base_path}{self.slash}" \
                             f"{self.slash.join(name.split(self.slash)[num_of_back_fold:-1])}"
            return f"{temp_base_path}{self.slash}{self.get_file_name(name)}"
        return f"{self.base_path}{self.slash}{name}"

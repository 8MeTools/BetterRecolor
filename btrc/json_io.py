import json
import os

import json5


def list_layout_json_files(root_dir):
    layout_files = []
    for root, _, files in os.walk(root_dir):
        for f in files:
            if f.endswith((".json", ".json5")):
                layout_files.append(os.path.join(root, f))
    return layout_files


def read_layout_json(path):
    with open(path, "r", encoding="utf-8") as f:
        if str(path).endswith(".json"):
            return json.load(f)
        return json5.load(f)


def write_layout_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        if str(path).endswith(".json"):
            json.dump(data, f, ensure_ascii=False, indent=2)
        else:
            json5.dump(data, f, indent=2)


list_json_files = list_layout_json_files
read_json = read_layout_json
write_json = write_layout_json

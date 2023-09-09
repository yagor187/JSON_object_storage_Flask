import json
import os.path
import time

STORAGE_FILE = "files/data1.json"

def open_file():
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                print("JSON-файл пустой или содержит неверный формат данных.")
                return {}
    else:
        return {}

def write_file(object_storage):
    with open(STORAGE_FILE, "w", encoding="utf-8") as file:
        json.dump(object_storage, file, indent=4)


def check_ttl(object_storage):
    while True:
        lst_del = []
        for key in object_storage.keys():
            if "expires_time" in object_storage[key]:
                if object_storage[key]["expires_time"] is not None and object_storage[key]["expires_time"] <= int(time.time()):
                    lst_del.append(key)
        for key in lst_del:
            del object_storage[key]
        write_file(object_storage)
        time.sleep(10)

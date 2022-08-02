from uuid import uuid4


def uuid_namer(instance, file_name):
    name, ext = file_name.split(".")
    return name + str(uuid4()) + f".{ext}"

def write_to_file(data: bytes, path: str):
    with open(path, "w") as file:
        file.write(data)

def read_from_file(path: str) -> bytes:
    try:
        with open(path, "r") as file:
            return file.read()
    except:
        return None
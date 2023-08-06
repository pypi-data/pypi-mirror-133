import json

def stream_load(f):
    """Load JSON data as steam

    From <https://stackoverflow.com/questions/6886283/how-i-can-i-lazily-read-multiple-json-values-from-a-file-stream-in-python>
    """
    start_pos = 0

    while True:
        try:
            obj = json.load(f)
            yield obj

            return
        except json.JSONDecodeError as exc:
            f.seek(start_pos)
            json_str = f.read(exc.pos)
            obj = json.loads(json_str)
            start_pos += exc.pos
            yield obj



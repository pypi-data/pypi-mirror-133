import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def string():
    try:
        with open(os.path.join(BASE_DIR, "VERSION"), "r", encoding="utf-8") as fh:
            version = fh.read().strip()
            if version:
                return version
    except:
        pass
    return "unknown (git checkout)"

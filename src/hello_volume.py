import pathlib
from typing import cast

import modal

app = modal.App("Hello, Volumes")
volume = modal.Volume.from_name("hello-volume")

FOO_FILE = "foo.txt"

@app.function(gpu=None, image=modal.Image.debian_slim(), volumes={"/my_vol": volume})
def square(x: int) -> int:
    import os
    print("This code is running on a remote worker!")
    print("OS: ", os.name)
    import sys
    print("Python: ", sys.version)
    import pathlib
    p = pathlib.Path("/my_vol") / FOO_FILE
    print(f"Writing file {p}", )
    p.write_text("FOO", encoding="utf-8")
    print(f"Issuing commit...", )
    volume.commit()  # This persists the file
    return x ** 2


@app.local_entrypoint()
def main():
    print("Running remote function...")
    print(">> ", square.remote(42))
    # When we run locally, the volume is not mounted, so we use its API instead
    print("Volume reload...")
    files = volume.listdir("/")
    print("Files: ", files)
    print(f">> cat {FOO_FILE}")
    # `read_file` returns a Generator so we can read in chunks to save memory
    for chunk in volume.read_file(FOO_FILE):
        print(chunk.decode("utf-8"), end="")
    print()
    print("You can download the file from the CLI:")
    print(f"    uv run modal volume get hello-volume {FOO_FILE}")
    print("Done.")

import modal

app = modal.App("Hello, World")

@app.function()
def square(x):
    import os
    import sys
    print("This code is running on a remote worker!")
    print("OS: ", os.name)
    import sys
    print("Python: ", sys.version)
    return x**2

@app.local_entrypoint()
def main():
    print("Running remote function...")
    print(">> ", square.remote(42))
    print("Done.")
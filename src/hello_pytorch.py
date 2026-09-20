import modal

app = modal.App("Hello, PyTorch")


# Provision a GPU (make sure your account has payment method registered to use GPUs)
# Nvidia T4 is currently the cheapest GPU on offer, see https://modal.com/pricing
# Note that we have to pick a container Image with pytorch here
@app.function(gpu="T4", image=modal.Image.debian_slim().uv_pip_install("torch").uv_pip_install("numpy"))
def square(x: int) -> int:
    import os
    print("This code is running on a remote worker!")
    print("OS: ", os.name)
    import sys
    print("Python: ", sys.version)
    import torch
    print("PyTorch: ", torch.__version__)
    print("PyTorch CUDA version: ", torch.version.cuda)
    print("PyTorch CUDA available: ", torch.cuda.is_available())
    result = torch.square(torch.tensor(x))
    return int(result.item())


@app.local_entrypoint()
def main():
    print("Running remote function...")
    print(">> ", square.remote(42))
    print("Done.")

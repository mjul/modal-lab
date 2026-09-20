# Modal Lab

Testing Modal serverless GPU compute.

## Setup

First, run the Modal setup.
Create an account, then run this. Unlike the Modal docs, we use `uv`:

```
uv add modal        # Add modal to the project, requires previous `uv init`
uv run modal setup  # Authorize and sets the auth token in the user home directory
```

We need the modal client library in the project, otherwise we could even run setup like this:

```
uv run --with modal modal setup
```

## Hello, World

Now run a Python script ([hello_world.py](./src/hello_world.py)) in the Modal cloud like this:

```
uv run modal run --timestamps src/hello_world.py    
```

I get some deprecation warnings from the Modal library,

    DeprecationWarning: 'asyncio.WindowsSelectorEventLoopPolicy' is deprecated and slated for removal in Python 3.16 

It is safe to ignore this for now.

You will see it calculating $42^2$ on the remote instance and some print
statements showing the os and Python version, e.g.

```
2026-09-20 14:08:22+02:00 This code is running on a remote worker!
2026-09-20 14:08:22+02:00 OS:  posix
2026-09-20 14:08:22+02:00 Python:  3.14.2 (main, Dec  8 2025, 23:38:13) [GCC 12.2.0]
```

Hello world does not set up the Python version, everything is default, so we see the default is **Python 3.14**.

## Hello, PyTorch

Let's try again, but with PyTorch, see [hello_pytorch.py](./src/hello_pytorch.py)

Note that we have to add two new declarations:

- install `numpy` and `pytorch` on the GPU instance
- provision a GPU (you can run the code without this, but in that case PyTorch runs on CPU)

```python
@app.function(gpu=None, image=modal.Image.debian_slim().uv_pip_install("torch").uv_pip_install("numpy"))
def square(x: int) -> int:
    # ...
```

Now run it:

```
uv run modal run --timestamps src/hello_pytorch.py
```

And you can see something like this:

```
2026-09-20 14:55:18+02:00 PyTorch:  2.14.0+cu130
2026-09-20 14:55:18+02:00 PyTorch CUDA version:  13.0
2026-09-20 14:55:18+02:00 PyTorch CUDA available:  False
```

We have to provision a gpu other than `None` to enable CUDA, T4 is the cheapest instance:

```python
@app.function(gpu="T4", image=modal.Image.debian_slim().uv_pip_install("torch").uv_pip_install("numpy"))
def square(x: int) -> int:
    # ...
```

Run it again, now CUDA is available:

```
2026-09-20 15:03:53+02:00 PyTorch:  2.14.0+cu130
2026-09-20 15:03:53+02:00 PyTorch CUDA version:  13.0
2026-09-20 15:03:53+02:00 PyTorch CUDA available:  True
```

## Hello Volumes

Let's try to add a persistent disk image, called a Volume. See [hello_volume.py](./src/hello_volume.py)

First, we have to create the Volume in Modal (in your default environment):

```
uv run modal volume create hello-volume
```

It creates the volume and shows how to use it:
```python
@app.function(volumes={"/my_vol": modal.Volume.from_name("hello-volume")})                                                                                                                                                                                                                                          
def some_func():                                                                                                                                                                                                                                                                                                    
    os.listdir("/my_vol")                                                                                                                                                                                                                                                                                           
```

We can write to the volume in the remote function and access the volume from the local function.

We can also download files from the volume from the CLI:

```
uv run modal volume get hello-volume foo.txt
```


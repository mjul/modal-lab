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

Now run it in the Modal cloud like this:

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


Jumper
======

A jump and run game with puzzle solving elements written in Python.

Setup
-----

In addition to Python 3, the following libraries must be installed manually.
Unfortunately, there is no way to automate this using pip currently. On
Windows, you can use the installers by Christoph Gohlke. Make sure to select
the versions that match your Python installation in both version number and
address model.

Library     | Description                  | Download
----------- | ---------------------------- | ----------------------
[Pygame][1] | Multimedia and game library. | [Windows installer][2]

[1]: http://www.pygame.org/
[2]: http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame

To set up the repository, create a virtual environment in its root and install
dependencies from the requirements file.

    virtualenv .
    Scripts/activate
    pip install -r requirements.txt

On Windows, you can run the `environment.bat` instead, which will open a
command promt inside the environment. This script will also create the
environment and install requirements on first use.

To start the game, run `python src/main.py` inside the virtual environment. On
Windows, use the `application.bat` script.

Controls
--------

Key     | Function
------- | ----------
`A`     | Move left
`D`     | Move right
`Space` | Jump

You can only jump when you are on the ground. However, you can move sideways
while you are in the air.

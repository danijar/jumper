Jumper
======

A jump and run game with puzzle solving elements written in Python.

![Screenshot](screenshot/2014-12-15.png?raw=true)

Instructions
------------

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

Function            | Player 1 | Player 2 |
------------------- |:--------:|:--------:|
Move left           | A        | Left     |
Move right          | D        | Right    |
Jump                | W        | Up       |
Attack other player | Space    | Return   |

While you are in the air, you have a second jump and you can move sideways. Hit
enemies by jumping ontop of them.

Attribution
-----------

This game uses modified assets from [Sithjester's RMXP Resources][3].

[3]: http://untamed.wild-refuge.net/rmxpresources.php?characters

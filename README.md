# Slippi Analysis

This is a collection of scripts that analyze Super Smash Brothers Melee replays to provide a more analytical perspective to prevalent arguments within the community. If you would like to learn more, take a look at [Project Slippi's website](https://slippi.gg/) and their [replay file spec](https://github.com/project-slippi/project-slippi/wiki/Replay-File-Spec).

If you would like to do replay analysis, take a look at replayprocessor.py. This script processes replays into dictionary data structures. It is created according to Slippi v2.0.0, but should work with previous versions, though some dictionary fields will be empty. It should also work with future versions, though it will not process any new data fields. Note that replayprocessor.py uses the py-ubjson library, which allows for conversion of ubjson to JSON.

# idle-power-automate
Automation scripts for the play store game app called Idle Power. Written in python and calls adb commands.

# Setup
You need python and adb installed.
[Python Installer](https://www.python.org/downloads/)
[ADB Introduction](https://developer.android.com/tools/adb)

You will also need to enable developer options on your android phone but this one is also described under adb's page.

I made it for my screen size and may and probably won't work for you. Go into the scripts and modify the coordinate definitions.

Always check python scripts for more info.

# Tap to spawn batteries
This script is the most basic. Sadly this method of calling adb is really slow and you can easily get more taps manually. I could barely get 300 taps in 30 seconds.

Examples:
```python tap.py 100```
Tap 100 times
```python tap.py 250```
Tap 250 times

# Combine batteries
[Demo video](https://youtu.be/bQ8E7XuEgXQ)

This script combines batteries. You need to give the index of the starting cell.

Examples:
```python combine.py 5```
Starts the combination on cell index 5 assuming a battery level of 0. Stops before every loop and waits for user input.
```python combine.py 5 3```
Starts on cell 5 with assming that the battery there is 3 levels higher than baseline.
```python combine.py 5 3 7```
Same as before, but instead of waiting for user input to start the next loop, it runs for 7 rounds non stop, increasing the level of the cell 5 battery by 7.

# Spin the wheels
This one spins the generators and switches between them. You can give the number of generators that you have. You need to start the script on solar.

Examples
```python spin.py 4```


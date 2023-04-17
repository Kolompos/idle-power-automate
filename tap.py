import os
import sys
import time

# this is really slow, maxes out at around 350 on my setup. Pressign manually is faster...

print('\n')

if len(sys.argv) < 2:
    print('You need to provide the number of taps')
    sys.exit(1)

clicks = int(sys.argv[1])

if clicks > 2000:
    print('WoW man, change the code on your own responsibility')
    sys.exit(1)

if clicks < 0:
    print('Can\'t press button negative times')
    sys.exit(1)

# Define the center of the OK button
ok_point = (550, 1850)      #550, 1850
start_point = (550, 1670)   #550, 1670

x, y = ok_point

# Press OK button
os.system(f"adb shell input tap {x} {y}")

x, y = start_point
print(f"Starting script, tapping {clicks} times on point ({x},{y})")

# Press START button
os.system(f"adb shell input tap {x} {y}")

# Press argument times
for i in range(clicks):
    os.system(f"adb shell input tap {x} {y}")
    if (i + 1) % 100 == 0:
        print(f"Tapped {i + 1} times...")

print('\nGG\n')
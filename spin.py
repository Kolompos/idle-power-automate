import os
import sys
import time

# --- Examples ---

# python spin.py --- Spins the generators one by one, cycling trough all of them, assuming that you have unlocked all of them. You need to start the script on solar.

# python spin.py 3 --- Spins the generators one by one, cycling trough 3 of them. You need to start on solar.

# --- Examples ---

# --- Parameters ---

# -- 1: Optional, the number of generators unlocked

# - Sometimes the swipe misses if it's too fast. If it does, increase this time.
sleep_ms = 150

# TODO: check if ADB can query screen size as I think the proportional position is the same...
# - Define the top-left point of the grid, when if you are already in dev options, turn on the helper bar that shows the coordinates of your touch. Makes acquiring coordinates trivial.
left_arrow = (195, 1365) # center coordinates of left arrow
right_arrow = (0, 0) # center coordinates of right arrow

# - Theese should work for you too, but if not, modify them too.
swipe_up = (0, 0)
swipe_down = (0, 0)

# --- Parameters ---

print('\n')

number_of_generators = 6
if len(sys.argv) > 1:

    number_of_generators = int(sys.argv[1])

    if number_of_generators > 6:
        print('That number of generators is not possible.')
        sys.exit(1)

    if number_of_generators < 0:
        print('Negative number of generators is non sense')
        sys.exit(1)

        
print('All right, lets get to it...')
print(f'Number of generators {number_of_generators} set')

(x1, y1), (x2, y2) = swipe_up, swipe_down

def do_the_swipe():
    os.system(f"adb shell input swipe {x1} {y1} {x2} {y2} {sleep_ms}")
    # Wait a but just to be sure
    time.sleep(sleep_ms / 1000)

(lx, ly), (rx, ry) = left_arrow, right_arrow
def switch_generator(right):
    
    if right:
        os.system(f"adb shell input tap {rx} {ry}")
    else:
        os.system(f"adb shell input tap {lx} {ly}")
    # Wait for the animation to complete
    time.sleep(sleep_ms / 1000)

while True:

    do_the_swipe()
    for i in range(number_of_generators):
        switch_generator(True)
        do_the_swipe()
    
    for i in range(number_of_generators, 0, -1):
        switch_generator(False)
    
    print('Competed a loop, ctrl-c to escape...\n')
    
print('\nGG\n')
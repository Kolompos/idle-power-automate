import os
import sys
import time
import array
import time

# --- Examples ---

# python combine.py 5  --- Starts the combination on cell index 5 assuming a battery level of 0. Stops before every loop and waits for user input.
# python combine.py 5 3 --- Starts on cell 5 with assming that the battery there is 3 levels higher than baseline.
# python combine.py 5 3 7 --- Same as before, but instead of waiting for user input to start the next loop, it runs for 7 rounds non stop, increasing the level of the cell 5 battery by 7.

# when starting from zero, you would try
# py combine 0 0 15 --- this is the max amount, but be aware that it will take a looong time.

# --- Examples ---

# --- Parameters ---

# -- 1: Give the zero based index of the first grid cell as an argument
#   0   1   2   3
#   4   5   6   7
#   8   9   10  11
#   12  13  14  15 -- 15 can't be..

# -- 2: Give the power of the battery on the first grid cell if higher than baseline
# If you started from a non baseline level, provide it. By default it is 0
# Onve level above the baseline would be one, two level above two and so on...
# (Baselime os the battery that gets spawned
# The sum of this and param 1 must be less than 15

# -- 3: Give the number of loops you want to make.
# You can ommit this one, then it will stop loop by loop.
# The sum of this and param 1 + 2 must be less than 16

# - Sometimes the swipe misses if it's too fast. If it does, increase this time.
sleep_ms = 150

# TODO: check if ADB can query screen size as I think the proportional position is the same...
# - Define the top-left point of the grid, when if you are already in dev options, turn on the helper bar that shows the coordinates of your touch. Makes acquiring coordinates trivial.
base_point = (195, 1365) # center coordinates of cell 0
grid_size = 230 # the center to center or corner to corner distance of the grid cells

# --- Parameters ---

print('\n')

if len(sys.argv) < 2:
    print('You need to provide the start index')
    sys.exit(1)

start_index = int(sys.argv[1])

if start_index > 14:
    print('That start index would be problematic')
    sys.exit(1)

if start_index < 0:
    print('Negative start index is non sense')
    sys.exit(1)

battery_power = 0
number_of_loops = -1

if len(sys.argv) > 2:
    battery_power = int(sys.argv[2])
    
    if battery_power < 0:
        print('Negative battery power level is non sense')
        sys.exit(1)
    
    if battery_power + start_index > 14:
        print('The sum of start index and number of loops can\'t be > 14')
        sys.exit(1)
    
    if len(sys.argv) > 3:
        number_of_loops = int(sys.argv[3])
        
        if number_of_loops < 1:
            print('Zero or negative number of loops is non sense')
            sys.exit(1)
        
        if number_of_loops + start_index + battery_power > 15:
            print('The sum of start index, number of loops and battery_power can\'t be > 15')
            sys.exit(1)
        
print('All right, lets get to it...')
print(f'Start cell index: {start_index}, battery power level: {battery_power}, number of loops: {number_of_loops} (-1 is default, stops before each loop)')
# Define the grid of points
grid = []
for y in range(4):
    for x in range(4):
        point = (base_point[0] + x * grid_size, base_point[1] + y * grid_size)
        grid.append(point)
    
def generate_steps(battery_power, last_steps):

    number_of_steps = 2 ** battery_power
    steps = array.array('i', [0]*number_of_steps)
    
    # The first part of the array is the same as the last_steps. 0 end already removed
    for i in range(len(last_steps)):
        steps[i] = last_steps[i]
    
    # The second part of  the array is the last_steps + 1
    offset = (2 ** (battery_power - 1)) - 1
    for i in range(len(last_steps)):
        steps[i + offset] = last_steps[i] + 1
    
    # Print for debug
    print('\n-------------------------------------------------------')
    print(f'Battery level {battery_power}, generated {number_of_steps} steps')
    print(f"Steps array: {steps.tolist()}")
    
    seconds = 0
    three = sleep_ms * 2.5 / 333
    one = sleep_ms * 2.5 / 1000
    for step in steps:
        grid_index = start_index + step
        if (grid_index + 1) % 4 == 0:
            seconds += three
        else:
            seconds += one
            
    print(f'This would take about {seconds:.1f} seconds or {(seconds / 60):.2f} minutes to complete\n')
    return steps

def do_the_loop(wait, battery_power, last_steps):

    steps = generate_steps(battery_power, last_steps)
    
    # Wait for the user to press a key
    if wait:
        input('Press Enter to start, ctrl-c to escape...\n')
    else:
        print('ctrl-c to escape...\n')
        
    # Start the stopwatch
    start_time = time.time()
    
    step_number = 1
    len_steps = len(steps)
    for step in steps:
        grid_index = start_index + step
        if grid_index == 15:
            # out of space, buy higher tier batteries.
            sys.exit(1)
        # set swiper coordinates
        x1, y1 = grid[grid_index + 1]
        x2, y2 = grid[grid_index]
        # set swipe time
        sleep_time = sleep_ms
        if (grid_index + 1) % 4 == 0:
            sleep_time = sleep_ms * 3
        # do the swipe
        print(f"Step {step_number}/{len_steps}, moving cell {grid_index + 1} to {grid_index}")
        os.system(f"adb shell input swipe {x1} {y1} {x2} {y2} {sleep_time}")
        time.sleep(sleep_time / 1000)
        step_number += 1
    
    # Stop the stopwatch
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'\nElapsed time: {elapsed_time:.2f} seconds\n')
    return steps

last_steps = []

if battery_power > 0:
    print('\nBattery power non zero, generating steps leading up to correct level...')
    for i in range(battery_power):
        number_of_steps = 2 ** i
        last_steps = generate_steps(i, last_steps)

if number_of_loops == -1:
    while battery_power + start_index < 15:
        last_steps = do_the_loop(True, battery_power, last_steps)
        battery_power += 1
    print('\nRan out of space to build next level...')
else:
    for loop_index in range(number_of_loops):
        last_steps = do_the_loop(False, battery_power, last_steps)
        battery_power += 1

print('\nGG\n')
from pygame import *
import time
#import smbus2

screen_size = (1000, 1000)
screen = display.set_mode(screen_size)
init()

tickRate = 60
ticksToStop = 10
t0 = time.time()

oldPos = [screen_size[0]//2, screen_size[1]//2]
tickTimer = time.time()
running = True

#bus = smbus2.SMBus(1)

address_1 = 0x62
address_2 = 0x63

SENSITIVITY = 1

max_mouse = 500
min_mouse = -max_mouse


min_output = 0
max_output = 2700

x_mapped = max_output//2
y_mapped = max_output//2
last = [x_mapped, y_mapped]

# bus.write_i2c_block_data(address_1, 0x40, [(x_mapped >> 4) & 0xFF, (x_mapped << 4) & 0xFF])
# bus.write_i2c_block_data(address_2, 0x40, [(y_mapped >> 4) & 0xFF, (y_mapped << 4) & 0xFF])


def map_value(x):
    if x == 0:
        return max_output//2
    return (x - min_mouse) * (max_output - min_output) / (max_mouse - min_mouse) + min_output


def updateMouse():
    mouse_position = mouse.get_pos()
    dx = -(oldPos[0] - mouse_position[0])
    dy = oldPos[1] - mouse_position[1]
    mouse.set_pos(oldPos)
    return dx, dy


def mapForBus(dx, dy):
    current_x_duty = dx * SENSITIVITY
    current_y_duty = dy * SENSITIVITY

    x_mapped = map_value(current_x_duty)
    y_mapped = map_value(current_y_duty)

    if x_mapped < 0:
        x_mapped = 0
    elif x_mapped > 2700:
        x_mapped = 2700

    if y_mapped < 0:
        y_mapped = 0
    elif y_mapped > 2700:
        y_mapped = 2700

    x_mapped = int(x_mapped)
    y_mapped = int(y_mapped)

    return x_mapped, y_mapped


def writeToBus(last, new):
    if last == new:
        return False
    else:
        print(new)
        x_mapped_ = new[0]
        y_mapped_ = new[1]
        # bus.write_i2c_block_data(address_1, 0x40, [(x_mapped_ >> 4) & 0xFF, (x_mapped_ << 4) & 0xFF])
        # bus.write_i2c_block_data(address_2, 0x40, [(y_mapped_ >> 4) & 0xFF, (y_mapped_ << 4) & 0xFF])
        return True


while running:
    for events in event.get():
        if events.type == QUIT:
            running = False
        if events.type == KEYDOWN:
            if events.key == K_SPACE:
                running = False

    if time.time() - tickTimer > 1 / tickRate:
        dx, dy = updateMouse()
        x_mapped, y_mapped = mapForBus(dx, dy)
        new = [x_mapped, y_mapped]
        if new == [0, 0] and time.time() - tickTimer < ticksToStop/tickRate:
            continue
        tickTimer = time.time()
        if writeToBus(last, new):
            last[0] = new[0]
            last[1] = new[1]
    display.update()
display.quit()
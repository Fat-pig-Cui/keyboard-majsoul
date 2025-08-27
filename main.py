from math import floor
from time import sleep
from pynput import mouse, keyboard


def pre_input():
    print('雀魂: 使用键盘代替鼠标操作, 只适用于全屏游戏和下列分辨率的情况')
    print('=============== 键位说明 ===============')
    print('WASD: 上左下右')
    print('E: 鼠标点击左键')
    print('Q: 鼠标点击右键(客户端的过牌/摸切)')
    print('R: 点击"自动和牌", 然后鼠标位置快速复原')
    print('F: 点击"不吃碰杠", 然后鼠标位置快速复原')
    print('V: 点击"自动摸切", 然后鼠标位置快速复原')
    print('C: 点击小局结束后的"确定"按钮, 然后鼠标位置快速复原')
    print('F12: 暂停功能')
    print('ESC: 退出程序')
    print('========================================')
    print('Please select resolution (default: 2560x1440):')
    print('1. 3840x2160 (4K)')
    print('2. 2560x1440 (2K)')
    print('3. 1920x1080 (1K)')
    input_option = input()
    if input_option == '1':
        resolution = [3840, 2160]
    elif input_option == '3':
        resolution = [1920, 1080]
    else:
        resolution = [2560, 1440]

    print('Resolution: {}x{}\n'.format(resolution[0], resolution[1]))
    print('Script is working...')

    tile_local_position_y = 0.922
    tile_local_position_xs = [0.139, 0.189, 0.238, 0.287, 0.336, 0.385, 0.435, 0.484, 0.533, 0.582, 0.632, 0.681, 0.730,
                              0.797]
    for i in range(0, len(tile_local_position_xs)):
        tiles_position.append([tile_local_position_xs[i], tile_local_position_y])
    for i in range(0, len(tiles_position)):
        tiles_position[i][0] = floor(tiles_position[i][0] * resolution[0])
        tiles_position[i][1] = floor(tiles_position[i][1] * resolution[1])

    buttons_local_position_xs = [0.666, 0.533, 0.400]
    buttons_local_position_ys = [0.757, 0.650]
    for j in range(0, len(buttons_local_position_ys)):
        for i in range(0, len(buttons_local_position_xs)):
            buttons_position.append([buttons_local_position_xs[i], buttons_local_position_ys[j]])
    for i in range(0, len(buttons_position)):
        buttons_position[i][0] = floor(buttons_position[i][0] * resolution[0])
        buttons_position[i][1] = floor(buttons_position[i][1] * resolution[1])

    button_hu_position.extend([floor(0.0188 * resolution[0]), floor(0.538 * resolution[1])])
    button_ming_position.extend([floor(0.0188 * resolution[0]), floor(0.599 * resolution[1])])
    button_qie_position.extend([floor(0.0188 * resolution[0]), floor(0.660 * resolution[1])])
    button_resume_position.extend([floor(0.914 * resolution[0]), floor(0.924 * resolution[1])])


def mouse_move_up():
    global tile_mode, current_tile_index, current_button_index
    if tile_mode:
        ms.position = (buttons_position[current_button_index][0], buttons_position[current_button_index][1])
        tile_mode = False
    else:
        if current_button_index < 3:
            current_button_index += 3
            ms.position = (buttons_position[current_button_index][0], buttons_position[current_button_index][1])


def mouse_move_down():
    global tile_mode, current_tile_index, current_button_index
    if not tile_mode:
        if current_button_index < 3:
            ms.position = (tiles_position[current_tile_index][0], tiles_position[current_tile_index][1])
            tile_mode = True
        else:
            current_button_index -= 3
            ms.position = (buttons_position[current_button_index][0], buttons_position[current_button_index][1])


def mouse_move_left():
    global tile_mode, current_tile_index, current_button_index
    if tile_mode:
        current_tile_index = (current_tile_index - 1 + len(tiles_position)) % len(tiles_position)
        ms.position = (tiles_position[current_tile_index][0], tiles_position[current_tile_index][1])
    else:
        current_button_index = (current_button_index + 1) % len(buttons_position)
        ms.position = (buttons_position[current_button_index][0], buttons_position[current_button_index][1])


def mouse_move_right():
    global tile_mode, current_tile_index, current_button_index
    if tile_mode:
        current_tile_index = (current_tile_index + 1) % len(tiles_position)
        ms.position = (tiles_position[current_tile_index][0], tiles_position[current_tile_index][1])
    else:
        current_button_index = (current_button_index - 1 + len(buttons_position)) % len(buttons_position)
        ms.position = (buttons_position[current_button_index][0], buttons_position[current_button_index][1])


def quick_click(button_position):
    (tmp_x, tmp_y) = ms.position
    ms.position = (button_position[0], button_position[1])
    ms.click(mouse.Button.left, 1)
    sleep(sleep_time)
    ms.position = (tmp_x, tmp_y)


def on_press(key):
    if is_enabled and hasattr(key, 'char'):
        if key.char == 'w':
            mouse_move_up()
        elif key.char == 'a':
            mouse_move_left()
        elif key.char == 's':
            mouse_move_down()
        elif key.char == 'd':
            mouse_move_right()
        elif key.char == 'e':
            ms.click(mouse.Button.left, 1)
        elif key.char == 'q':
            ms.click(mouse.Button.right, 1)
        elif key.char == 'r':
            quick_click(button_hu_position)
        elif key.char == 'f':
            quick_click(button_ming_position)
        elif key.char == 'v':
            quick_click(button_qie_position)
        elif key.char == 'c':
            quick_click(button_resume_position)


def on_release(key):
    global is_enabled
    if key == keyboard.Key.esc:
        return False
    if key == keyboard.Key.f12:
        if is_enabled:
            print('Script paused...')
        else:
            print('Script resume...')
        is_enabled = not is_enabled
    return True


if __name__ == '__main__':
    tiles_position = []
    buttons_position = []
    button_hu_position = []
    button_ming_position = []
    button_qie_position = []
    button_resume_position = []

    current_tile_index = 13
    current_button_index = 1
    tile_mode = True
    is_enabled = True
    sleep_time = 0.02

    pre_input()
    ms = mouse.Controller()

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    listener.join()

    print('\nProgram ended')
    input('Press any key to exit...')

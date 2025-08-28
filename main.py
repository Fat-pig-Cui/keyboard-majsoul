from time import sleep
from pynput import mouse, keyboard


def pre_input():
    print('雀魂: 使用键盘代替鼠标操作, 只适用于全屏游戏和指定分辨率的情况')
    print('=============== 键位说明 ===============')
    print('WASD: 上左下右')
    print('E: 鼠标点击左键')
    print('Q: 鼠标点击右键(客户端的过牌/摸切)')
    print('R: 快速点击"自动和牌"(之后位置复原, 下同)')
    print('F: 快速点击"不吃碰杠"')
    print('V: 快速点击"自动拔北"')
    print('C: 快速点击"确认"(右下角)')
    print('Z: 快速点击"自动摸切"')
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

    tile_ratio_y = 0.922
    tile_ratio_xs = [0.139, 0.189, 0.238, 0.287, 0.336, 0.385, 0.435, 0.484, 0.533, 0.582, 0.632, 0.681, 0.730, 0.797]
    for i in range(0, len(tile_ratio_xs)):
        tiles_position.append([tile_ratio_xs[i], tile_ratio_y])
    for i in range(0, len(tiles_position)):
        tiles_position[i][0] = tiles_position[i][0] * resolution[0]
        tiles_position[i][1] = tiles_position[i][1] * resolution[1]

    buttons_ratio_xs = [0.666, 0.533, 0.400]
    buttons_ratio_ys = [0.757, 0.650]
    for j in range(0, len(buttons_ratio_ys)):
        for i in range(0, len(buttons_ratio_xs)):
            btns_position.append([buttons_ratio_xs[i], buttons_ratio_ys[j]])
    for i in range(0, len(btns_position)):
        btns_position[i][0] = btns_position[i][0] * resolution[0]
        btns_position[i][1] = btns_position[i][1] * resolution[1]

    sidebar_ratio_x = 0.0195
    btn_hu_position.extend([sidebar_ratio_x * resolution[0], 0.553 * resolution[1]])
    btn_ming_position.extend([sidebar_ratio_x * resolution[0], 0.609 * resolution[1]])
    btn_qie_position.extend([sidebar_ratio_x * resolution[0], 0.669 * resolution[1]])
    btn_ba_position.extend([sidebar_ratio_x * resolution[0], 0.724 * resolution[1]])
    btn_resume_position.extend([0.914 * resolution[0], 0.924 * resolution[1]])


def mouse_move_up():
    global tile_mode, cur_tile_index, cur_button_index, tile_index2btn_index, btn_index2tile_index
    if tile_mode:
        cur_button_index = tile_index2btn_index[cur_tile_index]
        btn_index2tile_index[cur_button_index] = cur_tile_index
        ms.position = (btns_position[cur_button_index][0], btns_position[cur_button_index][1])
        tile_mode = False
    else:
        if cur_button_index < 3:
            cur_button_index += 3
            ms.position = (btns_position[cur_button_index][0], btns_position[cur_button_index][1])


def mouse_move_down():
    global tile_mode, cur_tile_index, cur_button_index, tile_index2btn_index, btn_index2tile_index
    if not tile_mode:
        if cur_button_index < 3:
            cur_tile_index = btn_index2tile_index[cur_button_index]
            ms.position = (tiles_position[cur_tile_index][0], tiles_position[cur_tile_index][1])
            tile_mode = True
        else:
            cur_button_index -= 3
            ms.position = (btns_position[cur_button_index][0], btns_position[cur_button_index][1])


def mouse_move_left():
    global tile_mode, cur_tile_index, cur_button_index
    if tile_mode:
        cur_tile_index = (cur_tile_index - 1 + len(tiles_position)) % len(tiles_position)
        ms.position = (tiles_position[cur_tile_index][0], tiles_position[cur_tile_index][1])
    else:
        if cur_button_index < 5 and cur_button_index != 2:
            cur_button_index += 1
        ms.position = (btns_position[cur_button_index][0], btns_position[cur_button_index][1])


def mouse_move_right():
    global tile_mode, cur_tile_index, cur_button_index
    if tile_mode:
        cur_tile_index = (cur_tile_index + 1) % len(tiles_position)
        ms.position = (tiles_position[cur_tile_index][0], tiles_position[cur_tile_index][1])
    else:
        if cur_button_index > 0 and cur_button_index != 3:
            cur_button_index -= 1
        ms.position = (btns_position[cur_button_index][0], btns_position[cur_button_index][1])


def quick_click(button_position):
    (tmp_x, tmp_y) = ms.position
    ms.position = (button_position[0], button_position[1])
    ms.click(mouse.Button.left, 1)
    sleep(sleep_time)
    ms.position = (tmp_x, tmp_y)


def on_press(key):
    global is_first_press
    if is_enabled and hasattr(key, 'char'):
        if is_first_press:
            ms.position = (tiles_position[13][0], tiles_position[13][1])
            is_first_press = False
            return
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
            quick_click(btn_hu_position)
        elif key.char == 'f':
            quick_click(btn_ming_position)
        elif key.char == 'v':
            quick_click(btn_ba_position)
        elif key.char == 'c':
            quick_click(btn_resume_position)
        elif key.char == 'z':
            quick_click(btn_qie_position)


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
    btns_position = []
    btn_hu_position = []
    btn_ming_position = []
    btn_qie_position = []
    btn_ba_position = []
    btn_resume_position = []

    cur_tile_index = 13
    cur_button_index = 0
    btn_index2tile_index = [11, 8, 5]
    tile_mode = True
    is_enabled = True
    is_first_press = True

    # constant
    sleep_time = 0.02
    tile_index2btn_index = [2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 0, 0, 0, 0]

    pre_input()
    ms = mouse.Controller()

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    listener.join()

    print('\nProgram ended')
    input('Press any key to exit...')

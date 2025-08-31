from time import sleep
from pynput import mouse, keyboard


def pre_input():
    global start_pos
    print('雀魂: 使用键盘代替鼠标操作')
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
    print('请选择分辨率 (默认: 2560x1440 全屏):')
    print('1. 3840x2160 全屏 (4K)')
    print('2. 2560x1440 全屏 (2K)')
    print('3. 1920x1080 全屏 (1K)')
    print('4. 自定义分辨率 (高级, 可以窗口化但仍然只能是 16:9 格式)')
    input_option = input()

    def custom_resolution():
        global start_pos
        print('\n你已经进入自定义分辨率阶段, 请按照以下步骤操作')
        print('========================================')
        print('1. 打开雀魂, 将雀魂窗口调整到最适合你游玩的位置, 要求将画面完整展现在屏幕上')
        print('2. 全屏幕截图(如 PrintScreen 键, 如有多个屏幕只截取含有雀魂界面的显示器的完整屏幕)')
        print('3. 打开 Windows 自带的画图, Ctrl V 粘贴(如用的是其他截图工具, 则使用画图打开保存截图')
        print('4. 在画图的左下角会显示鼠标当前位置像素的坐标, 记录下面两个顶点的坐标(需要足够精准, 可以按右下角的放大)')
        print('4.1 顶点1: 雀魂画面界面矩形(不含窗口边框)的左上角')
        print('4.2 顶点2: 雀魂画面界面矩形(不含窗口边框)的右下角')
        print('========================================')
        print('请输入顶点1的坐标(按格式输入, 否则会闪退, 中间用"x"隔开, 如默认的"0x0"): ')
        text = input()
        if text.strip() != '':
            start_pos = [int(text.split('x')[0]), int(text.split('x')[1])]
        print('请输入顶点2的坐标(按格式输入, 否则会闪退, 中间用"x"隔开, 如默认的"2560x1440"): ')
        text = input()
        end_pos = [2560, 1440]
        if text.strip() != '':
            end_pos = [int(text.split('x')[0]), int(text.split('x')[1])]
        return [end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]]

    if input_option == '1':
        resolution = [3840, 2160]
    elif input_option == '3':
        resolution = [1920, 1080]
    elif input_option == '4':
        resolution = custom_resolution()
    else:
        resolution = [2560, 1440]

    print('游戏分辨率: {}x{}'.format(resolution[0], resolution[1]))
    print('起始位置: {}x{}\n'.format(start_pos[0], start_pos[1]))
    print('Script is working...')

    tile_ratio_y = 0.922
    tile_ratio_xs = [0.139, 0.189, 0.238, 0.287, 0.336, 0.385, 0.435, 0.484, 0.533, 0.582, 0.632, 0.681, 0.730, 0.797]
    for i in range(0, len(tile_ratio_xs)):
        tiles_pos.append([tile_ratio_xs[i], tile_ratio_y])
    for i in range(0, len(tiles_pos)):
        tiles_pos[i][0] = start_pos[0] + tiles_pos[i][0] * resolution[0]
        tiles_pos[i][1] = start_pos[1] + tiles_pos[i][1] * resolution[1]

    buttons_ratio_xs = [0.666, 0.533, 0.400]
    buttons_ratio_ys = [0.757, 0.650]
    for j in range(0, len(buttons_ratio_ys)):
        for i in range(0, len(buttons_ratio_xs)):
            btns_pos.append([buttons_ratio_xs[i], buttons_ratio_ys[j]])
    for i in range(0, len(btns_pos)):
        btns_pos[i][0] = start_pos[0] + btns_pos[i][0] * resolution[0]
        btns_pos[i][1] = start_pos[1] + btns_pos[i][1] * resolution[1]

    sidebar_ratio_x = 0.0195
    btn_hu_pos.extend([start_pos[0] + sidebar_ratio_x * resolution[0], start_pos[1] + 0.553 * resolution[1]])
    btn_ming_pos.extend([start_pos[0] + sidebar_ratio_x * resolution[0], start_pos[1] + 0.609 * resolution[1]])
    btn_qie_pos.extend([start_pos[0] + sidebar_ratio_x * resolution[0], start_pos[1] + 0.669 * resolution[1]])
    btn_ba_pos.extend([start_pos[0] + sidebar_ratio_x * resolution[0], start_pos[1] + 0.724 * resolution[1]])
    btn_resume_pos.extend([start_pos[0] + 0.914 * resolution[0], start_pos[1] + 0.924 * resolution[1]])


def mouse_move_up():
    global tile_mode, cur_tile_index, cur_button_index, tile_index2btn_index, btn_index2tile_index
    if tile_mode:
        cur_button_index = tile_index2btn_index[cur_tile_index]
        btn_index2tile_index[cur_button_index] = cur_tile_index
        ms.position = (btns_pos[cur_button_index][0], btns_pos[cur_button_index][1])
        tile_mode = False
    else:
        if cur_button_index < 3:
            cur_button_index += 3
            ms.position = (btns_pos[cur_button_index][0], btns_pos[cur_button_index][1])


def mouse_move_down():
    global tile_mode, cur_tile_index, cur_button_index, tile_index2btn_index, btn_index2tile_index
    if not tile_mode:
        if cur_button_index < 3:
            cur_tile_index = btn_index2tile_index[cur_button_index]
            ms.position = (tiles_pos[cur_tile_index][0], tiles_pos[cur_tile_index][1])
            tile_mode = True
        else:
            cur_button_index -= 3
            ms.position = (btns_pos[cur_button_index][0], btns_pos[cur_button_index][1])


def mouse_move_left():
    global tile_mode, cur_tile_index, cur_button_index
    if tile_mode:
        cur_tile_index = (cur_tile_index - 1 + len(tiles_pos)) % len(tiles_pos)
        ms.position = (tiles_pos[cur_tile_index][0], tiles_pos[cur_tile_index][1])
    else:
        if cur_button_index < 5 and cur_button_index != 2:
            cur_button_index += 1
        ms.position = (btns_pos[cur_button_index][0], btns_pos[cur_button_index][1])


def mouse_move_right():
    global tile_mode, cur_tile_index, cur_button_index
    if tile_mode:
        cur_tile_index = (cur_tile_index + 1) % len(tiles_pos)
        ms.position = (tiles_pos[cur_tile_index][0], tiles_pos[cur_tile_index][1])
    else:
        if cur_button_index > 0 and cur_button_index != 3:
            cur_button_index -= 1
        ms.position = (btns_pos[cur_button_index][0], btns_pos[cur_button_index][1])


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
            ms.position = (tiles_pos[13][0], tiles_pos[13][1])
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
            quick_click(btn_hu_pos)
        elif key.char == 'f':
            quick_click(btn_ming_pos)
        elif key.char == 'v':
            quick_click(btn_ba_pos)
        elif key.char == 'c':
            quick_click(btn_resume_pos)
        elif key.char == 'z':
            quick_click(btn_qie_pos)


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
    start_pos = [0, 0]
    tiles_pos = []
    btns_pos = []
    btn_hu_pos = []
    btn_ming_pos = []
    btn_qie_pos = []
    btn_ba_pos = []
    btn_resume_pos = []

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

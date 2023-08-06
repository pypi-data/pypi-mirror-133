import time, pynput

special_keys = {'Key.' + key: eval(f"pynput.keyboard.Key.{key}") for key in dir(pynput.keyboard.Key)}

def on_keyboard_press(_data, key):
    if _data.is_closed: return False
    current_time = time.time()

    if key == pynput.keyboard.Key.esc:
        _data.is_closed = True
        return False
    try:
        _out: dict = {"time": current_time, "action": "press_key", "key": key.char}
    except AttributeError:
        _out: dict = {"time": current_time, "action": "press_key", "key": str(key)}

    _data.macro_data.append(_out)

def on_keyboard_release(_data, key):
    if _data.is_closed: return False
    current_time = time.time()

    if key == pynput.keyboard.Key.esc:
        return False
    try:
        _out: dict = {"time": current_time, "action": "release_key", "key": key.char}
    except AttributeError:
        _out: dict = {"time": current_time, "action": "release_key", "key": str(key)}

    _data.macro_data.append(_out)
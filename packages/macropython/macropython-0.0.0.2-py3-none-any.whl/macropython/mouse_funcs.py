import time, pynput

def on_mouse_click(_data, x, y, button, pressed):
    if _data.is_closed: return False
    current_time = time.time()

    _data.macro_data.append({"time": current_time, "action":'mouse_press' if pressed else 'mouse_release', "button": str(button), "x_pos": x, "y_pos": y})

def on_mouse_scroll(_data, x, y, dx, dy):
    if _data.is_closed: return False
    current_time = time.time()
    _data.macro_data.append({"time": current_time, "action": "mouse_scroll", "vertical_direction": int(dy), "horizontal_direction": int(dx), "x_pos": x, "y_pos": y})

def on_mouse_move(_data, x, y):
    if _data.is_closed: return False
    if len(_data.macro_data) > 0:
        current_time = time.time()
        if (_data.macro_data[-1]['action'] == "mouse_press" and _data.macro_data[-1]['button'] == "Button.left") or (_data.macro_data[-1]['action'] == "mouse_moved" and (current_time - _data.macro_data[-1]['time']) > 0.02):
            _data.macro_data.append({"time": current_time, "action": "mouse_moved", "x_pos":x, "y_pos":y})

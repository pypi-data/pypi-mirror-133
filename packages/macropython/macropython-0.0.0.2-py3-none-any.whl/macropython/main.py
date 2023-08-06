import os
import time, pynput
from .mouse_funcs import on_mouse_click, on_mouse_move, on_mouse_scroll
from .keyboard_funcs import on_keyboard_press, on_keyboard_release
from .functions import save_file, load_file, make_line
from matplotlib import pyplot
special_keys = {'Key.' + key: eval(f"pynput.keyboard.Key.{key}") for key in dir(pynput.keyboard.Key)}

class Record:
    def __init__(self, _filename: str = "My Macro.txt", _delay: float = 5.0):
        self.macro_data: list = []

        if os.path.isfile(_filename) or os.path.isdir(_filename):
            raise FileExistsError(f"File '{_filename}' already exists.")

        self.filename: str = _filename
        self.keyboard_listener = pynput.keyboard.Listener(
            on_press = lambda key: on_keyboard_press(self, key),
            on_release = lambda key: on_keyboard_release(self, key)
        )
        self.mouse_listener = pynput.mouse.Listener(
            on_click = lambda x, y, button, pressed: on_mouse_click(self, x, y, button, pressed),
            on_scroll = lambda x, y, dx, dy: on_mouse_scroll(self, x, y, dx, dy),
            on_move = lambda x, y: on_mouse_move(self, x, y)
        )
        if _delay < 0:
            raise ValueError("_delay must be a positive float number.")
        self.delay = _delay
        self.is_closed = False

    def start(self):
        time.sleep(self.delay)

        self.keyboard_listener.start()
        self.mouse_listener.start()
        self.keyboard_listener.join()
        self.mouse_listener.join()

        if self.macro_data == []:
            print("No Data To Save")
        else:
            print(f"Saving {len(self.macro_data)} Inputs")
            save_file(self.filename, self.macro_data)
            print(f"Saved {len(self.macro_data)} Inputs")


class Play:
    def __init__(self, _filename: str = "My Macro.txt", _delay: float = 5.0):
        if not os.path.isfile(_filename):
            raise FileNotFoundError(f"File '{_filename}' was not found.")
        self.filename = _filename
        if _delay < 0:
            raise ValueError("_delay must be a positive float number.")
        self.delay = _delay
        self.macro_data: list = load_file(_filename)

    def play(self):

        time.sleep(self.delay)

        self.keyboard_controller = pynput.keyboard.Controller()
        self.mouse_controller = pynput.mouse.Controller()

        for i in range(len(self.macro_data)):
            current_data = self.macro_data[i]
            future_data = None
            try: future_data = self.macro_data[i+1]
            except: pass
            before_data = None
            if not i == 0:
                before_data = self.macro_data[i-1]
            skip_wait = False
            skip_tts = False

            if current_data['action'] in ["release_key", "press_key"]:
                key = current_data['key'] if 'Key.' not in current_data['key'] else special_keys[current_data['key']]
                if current_data['action'] == "press_key":
                    self.keyboard_controller.press(key)
                elif current_data['action'] == "release_key":
                    self.keyboard_controller.release(key)

            if current_data['action'] in ["mouse_press", "mouse_release", "mouse_scroll"]:
                
                coords = make_line(self.mouse_controller.position[0], self.mouse_controller.position[1], current_data['x_pos'], current_data['y_pos'])
                time_to_sleep = 0
                if not future_data == None:
                    if future_data['action'] in ["mouse_press", "mouse_release", "mouse_scroll"]:
                        time_to_sleep = (future_data['time'] - current_data['time'])/len(coords)

                if time_to_sleep < 0.001:
                    skip_tts = True

                for x, y in coords:
                    if not skip_tts: time.sleep(time_to_sleep)
                    self.mouse_controller.position = (int(x), int(y))

                if current_data['action'] == "mouse_press":
                    self.mouse_controller.press(pynput.mouse.Button.left if current_data['button'] == "Button.left" else pynput.mouse.Button.right)
                elif current_data['action'] == "mouse_release":
                    self.mouse_controller.release(pynput.mouse.Button.left if current_data['button'] == "Button.left" else pynput.mouse.Button.right)
                elif current_data['action'] == "mouse_scroll":
                    self.mouse_controller.scroll(current_data['horizontal_direction'], current_data['vertical_direction'])
            if not future_data == None:
                if not skip_wait:
                    time.sleep(future_data['time'] - current_data['time'])
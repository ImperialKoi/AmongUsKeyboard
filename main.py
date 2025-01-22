from pynput import keyboard, mouse
import threading
import sys 

mouse_controller = mouse.Controller()
mouse_clicker = mouse.Button.left

positions = {
    'w': (173, 750),
    'a': (117, 803),
    's': (173, 850),
    'd': (237, 803),
    'wd': (237, 750),  # Diagonal up-right
    'wa': (117, 750),  # Diagonal up-left
    'sd': (237, 850),  # Diagonal down-right
    'sa': (117, 850),  # Diagonal down-left
    'q': (1250, 650),  # Kill
    'm': (1300, 50),   # Map
    'r': (1100, 800),  # Report
    'e': (1250, 800),  # Use
    'c': (1100, 650),  # Vent
    'f': (950, 800),   # Sabotage
    'v': (950, 650)    # Vent (engineer only)
}

keys_pressed = set()
clicking = False
toggle_active = True 

def get_position_from_keys():
    if 'w' in keys_pressed and 'd' in keys_pressed:
        return positions['wd']
    if 'w' in keys_pressed and 'a' in keys_pressed:
        return positions['wa']
    if 's' in keys_pressed and 'd' in keys_pressed:
        return positions['sd']
    if 's' in keys_pressed and 'a' in keys_pressed:
        return positions['sa']
    # Single
    for key in keys_pressed:
        if key in positions:
            return positions[key]
    return None

def move_and_click():
    global clicking
    while clicking:
        position = get_position_from_keys()
        if position:
            mouse_controller.position = position
            mouse_controller.press(mouse_clicker)
        else:
            mouse_controller.release(mouse_clicker)
        threading.Event().wait(0.1)  # Reduce lag

def on_press(key):
    global clicking, toggle_active
    try:
        # Quit the program if `=` key is pressed
        if key.char == '=':
            print("Quitting the program...")
            sys.exit()

        # Check for toggle key (` key)
        if key.char == '`':
            toggle_active = not toggle_active
            if not toggle_active:
                keys_pressed.clear()
                clicking = False
                mouse_controller.release(mouse_clicker)
            return

        if toggle_active and key.char in positions:
            keys_pressed.add(key.char)
            if not clicking:
                clicking = True
                threading.Thread(target=move_and_click, daemon=True).start()
    except AttributeError:
        pass

def on_release(key):
    global clicking
    try:
        if toggle_active and key.char in positions:
            keys_pressed.discard(key.char)
            if not keys_pressed:
                clicking = False
                mouse_controller.release(mouse_clicker)
    except AttributeError:
        pass

def main():
    print("Press and hold keys for movement and mouse click-and-hold.")
    print("Supported keys: w, a, s, d, q, m, r, e, c.")
    print("Press ` to toggle functionality ON/OFF.")
    print("Press = to quit.")
    print("Press 'Ctrl+C' to stop.")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()

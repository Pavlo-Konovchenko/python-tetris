import tetrisplay
from pynput import keyboard
import time
import textualinterface

grid = tetrisplay.build_clean_grid()

def game_loop():
    time_passed = time.time()
    while True:
        if tetrisplay.check_for_game_over(grid):
            break
        elif time_passed + 0.5 < time.time():
            tetrisplay.drop_block(grid)
            time_passed = time.time()
        tetrisplay.show_dropping_block(grid)
    tetrisplay.display_grid(grid)
    print("Game Over")


def process_on_press(key):
    if key == keyboard.Key.left:
        tetrisplay.move_block(grid, -1)
    if key == keyboard.Key.right:
        tetrisplay.move_block(grid, 1)


#listener = keyboard.Listener( on_press=process_on_press )
#listener.start()

def main():
    textualinterface.start(grid)
    # game_loop()


if __name__=="__main__":
    main()

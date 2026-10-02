"""Play Sudoku in a pygame window, typing moves in the terminal.

Usage:
    python play.py              # standard Sudoku, 25 given numbers
    python play.py --filled 35  # easier board
    python play.py --diag       # diagonal Sudoku (both diagonals must be 1-9 too)
"""
import argparse
import builtins
import queue
import sys
import threading

import pygame

from sudoku_helper import sudoku_action


def _input_keeping_window_alive(prompt=""):
    """Read a terminal line while letting the pygame window stay responsive."""
    print("\n" + prompt)
    lines = queue.Queue()
    threading.Thread(target=lambda: lines.put(sys.stdin.readline()), daemon=True).start()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "done"
        try:
            line = lines.get(timeout=0.05).strip()
        except queue.Empty:
            continue
        return line or "help"


def _wait_for_window_close():
    print("Close the board window to exit.")
    while pygame.display.get_init() and pygame.display.get_surface():
        if any(e.type == pygame.QUIT for e in pygame.event.get()):
            break
        pygame.time.wait(50)
    pygame.quit()


def main():
    parser = argparse.ArgumentParser(description="Play Sudoku.")
    parser.add_argument("--filled", type=int, default=25, help="number of given cells (default 25)")
    parser.add_argument("--diag", action="store_true", help="play diagonal Sudoku")
    args = parser.parse_args()

    builtins.input = _input_keeping_window_alive
    sudoku_action(n=args.filled, diag=args.diag)
    _wait_for_window_close()


if __name__ == "__main__":
    main()

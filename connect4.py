#!/usr/bin/env python
import curses

class Game():

    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.grid = dict()

    def token(self, color):
        return color

    def drop(self, token, column):

        row = max([k[0] if k[1] == column else -1 for k in self.grid] + [-1])
        if row < self.height - 1:
            self.grid[(row+1, column)] = token
        else:
            raise Exception()

    def cellState(self, row, column):
        return self.grid.get((row, column), None)

    def over(self):
        for k in self.grid:
            vertical = [self.grid.get((k[0]+offset, k[1]), False) for offset in range(4)]
            horizontal = [self.grid.get((k[0], k[1]+offset), False) for offset in range(4)]
            diagonal_right = [self.grid.get((k[0]+offset, k[1]+offset), False) for offset in range(4)]
            diagonal_left = [self.grid.get((k[0]+offset, k[1]-offset), False) for offset in range(4)]
            if any([all(e == l[0] for e in l) for l in [vertical, horizontal, diagonal_right, diagonal_left]]):
                return True
        return False

class UI():
    def __init__(self):
        stdscr = curses.initscr()

def main_ui(stdscr):
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    state = "new"

    game = Game(6, 6)
    red = game.token('r')
    black = game.token('b')

    players_list = [red, black]

    selected_column = 0
    turn = 0
    while True:
        if state == "new":
            stdscr.addstr(0, 0, 'Press "t" for test' )
            stdscr.addstr(1, 0, 'Press "d" for divide' )
            stdscr.addstr(2, 0, 'Press "g" for game' )

        c = stdscr.getch()


        if c == ord('t'):
            stdscr.clear()
            state = "testing"
            stdscr.addstr("test")

        if c == ord('d'):
            state = "dividing"
            stdscr.clear()
            stdscr.addstr(1, 0, '10 divided by {} is {}'.format(1, 10/1))
            stdscr.addstr(7, 0, '10 divided by {} is {}'.format(1, 10/1))
            
        if c == ord('g'):
            state = "gaming"

        if state == "gameover" and c == ord('r'):
            state = "gaming"
            game = Game(6, 6)

        if c == curses.KEY_RIGHT:
            selected_column += 1
            selected_column = min(selected_column, game.width-1)

        if c == curses.KEY_LEFT:
            selected_column -= 1
            selected_column = max(selected_column, 0)

        if c == curses.KEY_DOWN and state == "gaming":
            game.drop(players_list[turn%len(players_list)], selected_column)
            turn += 1

        if state == "gaming":
            stdscr.clear()
            stdscr.addstr(0, selected_column, 'v')
            stdscr.addstr(1, 0, '_'*game.width)
            stdscr.addstr(8, 0, '~'*game.width)

            for k in game.grid:
                stdscr.addstr(game.height-k[0]+1, k[1], game.grid[k])

        if game.over():
            state = "gameover"
            stdscr.addstr(10, 0, 'GAME OVER ....')
            stdscr.addstr(11, 0, 'Press:')
            stdscr.addstr(12, 0, '       r) restart')
            stdscr.addstr(13, 0, '       q) quit')
            # stdscr.addstr(10, 0, ' _________    _______    _      _    _____   ')
            # stdscr.addstr(11, 0, '|  _______|  |  ___  |  | \    / |  |  ___|  ')
            # stdscr.addstr(12, 0, '| |    ___   | |___| |  |  \  /  |  | |___   ')
            # stdscr.addstr(13, 0, '| |   |_  |  |  ___  |  |   \/   |  |  ___|  ')
            # stdscr.addstr(14, 0, '| |_____| |  | |   | |  | |\  /| |  | |___   ')
            # stdscr.addstr(15, 0, '|_________|  |_|   |_|  |_| \/ |_|  |_____|  ')

            # stdscr.addstr(17, 0, ' ________   __        __   _____    _____    ')
            # stdscr.addstr(18, 0, '|  ____  |  \ \      / /  |  ___|  |  _  |   ')
            # stdscr.addstr(19, 0, '| |    | |   \ \    / /   | |___   | |_| |   ')
            # stdscr.addstr(20, 0, '| |    | |    \ \  / /    |  ___|  |    _|   ')
            # stdscr.addstr(21, 0, '| |____| |     \ \/ /     | |___   | |\ \    ')
            # stdscr.addstr(22, 0, '|________|      \__/      |_____|  |_| \_\   ')
            stdscr.refresh()

        if c == ord('q'):
            break
        
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


if __name__ == "__main__":
    curses.wrapper(main_ui)
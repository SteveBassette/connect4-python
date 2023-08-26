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

class GAME_STATES():
    PLAYING = 'playing'
    gaming = 'playing'
    gameover = 'gameover'

class CliGame(Game):

    def __init__(self, stdscr):
        super().__init__(6,6)

        self.stdscr = stdscr

        self.gameState = GAME_STATES.PLAYING
        self.selected_column = 0
        self.turn = 0

        red = self.token('r')
        black = self.token('b')
        self.players_list = [red, black]

    def drop(self):
        super().drop(self.players_list[self.turn%len(self.players_list)], self.selected_column)
        self.turn += 1

    def paintGameBoard(self, stdscr, selected_column):
        stdscr.clear()
        stdscr.addstr(0, selected_column, 'v')
        stdscr.addstr(1, 0, '_'*self.width)
        stdscr.addstr(8, 0, '~'*self.width)

        for k in self.grid:
            stdscr.addstr(self.height-k[0]+1, k[1], self.grid[k])

        stdscr.refresh()

    def paintGameOver(self, stdscr):
        self.gameState = GAME_STATES.gameover
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

    def main(self):
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

        self.paintGameBoard(self.stdscr, self.selected_column)
        while True:

            c = self.stdscr.getch()

            if c == ord('g'):
                self.gameState = GAME_STATES.gaming

            if self.gameState == GAME_STATES.gameover and c == ord('r'):
                self.gameState = GAME_STATES.gaming
                self.grid = dict()

            if c == curses.KEY_RIGHT:
                self.selected_column += 1
                self.selected_column = min(self.selected_column, self.width-1)

            if c == curses.KEY_LEFT:
                self.selected_column -= 1
                self.selected_column = max(self.selected_column, 0)

            if c == curses.KEY_DOWN and self.gameState == GAME_STATES.gaming:
                self.drop()

            if self.gameState == GAME_STATES.gaming:
                self.paintGameBoard(self.stdscr, self.selected_column)

            if self.over():
                self.paintGameOver(self.stdscr)

            if c == ord('q'):
                break
            
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

def main_ui(stdscr):
    game = CliGame(stdscr)
    game.main()

if __name__ == "__main__":
    curses.wrapper(main_ui)
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

    def _getTopRowWithToken(self, column):
        return max([k[0] if k[1] == column else -1 for k in self.grid] + [-1])

    def columnFull(self, column):
        row = self._getTopRowWithToken(column)
        return row >= self.height - 1
    
    def reset(self):
        self.grid = dict()

class GAME_STATES():
    PLAYING = 'playing'
    gaming = 'playing'
    gameover = 'gameover'

class Screen():

    def __init__(self, width=1, height=1, background=' '):
        self.width = width
        self.height = height
        self.background = background
        self.content = [[self.background for c in range(self.width)] for r in range(self.height)]

    def addstr(self, y, x, content):

        if x+1 > self.width:
            raise Exception()

        if y+1 > self.height:
            raise Exception()

        for index, s in enumerate(content):
            self.content[y][x+index] = s

    def refresh(self):
        pass

    def clear(self):
        self.content = [[self.background for c in range(self.width)] for r in range(self.height)]

    def __str__(self):
        return '\n'.join([''.join(l) for l in self.content])

class GameRunner():

    def __init__(self, game):
        self.game = game
        self.methods = {
            ord('q'): lambda: "quit",
            ord('>'): game.shiftRight,
            ord('<'): game.shiftLeft,
            ord('v'): game.drop,
            ord('r'): game.reset,
            curses.KEY_RIGHT: game.shiftRight,
            curses.KEY_LEFT: game.shiftLeft,
            curses.KEY_DOWN: game.drop,
        }

    def runSequential(self, screen):
        self.game.paintGameBoard()
        while True:
            command = screen.getch()
            if "quit" == self.methods[command]():
                return
            self.game.paintGameBoard()

    def run(self, command_sequence=None):
        for command in command_sequence:
            self.methods[command if not isinstance(command, str) else ord(command)]()



class CliGame(Game):

    def __init__(self, stdscr):
        super().__init__(6,6)
        self.stdscr = stdscr
        self.selected_column = 0
        red = self.token('r')
        black = self.token('b')
        self.players_list = [red, black]
        self.turn = 0

    def paintGameBoard(self):
        self.stdscr.clear()
        self.stdscr.addstr(0, self.selected_column, 'v')
        self.stdscr.addstr(8, 0, '~'*self.width)
        self.stdscr.addstr(1, 0, '_'*self.width)

        for k in self.grid:
            self.stdscr.addstr(self.height-k[0]+1, k[1], self.grid[k])

        if self.over():
            self.paintGameOver()

    def paintGameOver(self):
        self.stdscr.addstr(10, 0, 'GAME OVER ...')
        self.stdscr.addstr(11, 0, 'Press:')
        self.stdscr.addstr(12, 4, 'r) restart')
        self.stdscr.addstr(13, 4, 'q) quit')
        # self.stdscr.addstr(10, 0, ' _________    _______    _      _    _____   ')
        # self.stdscr.addstr(11, 0, '|  _______|  |  ___  |  | \    / |  |  ___|  ')
        # self.stdscr.addstr(12, 0, '| |    ___   | |___| |  |  \  /  |  | |___   ')
        # self.stdscr.addstr(13, 0, '| |   |_  |  |  ___  |  |   \/   |  |  ___|  ')
        # self.stdscr.addstr(14, 0, '| |_____| |  | |   | |  | |\  /| |  | |___   ')
        # self.stdscr.addstr(15, 0, '|_________|  |_|   |_|  |_| \/ |_|  |_____|  ')

        # self.stdscr.addstr(17, 0, ' ________   __        __   _____    _____    ')
        # self.stdscr.addstr(18, 0, '|  ____  |  \ \      / /  |  ___|  |  _  |   ')
        # self.stdscr.addstr(19, 0, '| |    | |   \ \    / /   | |___   | |_| |   ')
        # self.stdscr.addstr(20, 0, '| |    | |    \ \  / /    |  ___|  |    _|   ')
        # self.stdscr.addstr(21, 0, '| |____| |     \ \/ /     | |___   | |\ \    ')
        # self.stdscr.addstr(22, 0, '|________|      \__/      |_____|  |_| \_\   ')

    def drop(self):
        if not self.columnFull(self.selected_column) and not self.over():
            super().drop(self.players_list[self.turn%len(self.players_list)], self.selected_column)
            self.turn += 1

    def shiftRight(self):
        self.selected_column += 1
        self.selected_column = min(self.selected_column, self.width-1)

    def shiftLeft(self):
        self.selected_column -= 1
        self.selected_column = max(self.selected_column, 0)

    def reset(self):
        super().reset()
        self.selected_column = 0

def main_ui(stdscr):
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    game = CliGame(stdscr)
    runner = GameRunner(game)
    runner.runSequential(stdscr)
    
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

if __name__ == "__main__":
    curses.wrapper(main_ui)
import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        horizontal = "+"
        for i in range(self.life.cols):
            horizontal += "-"
        horizontal += "+"
        screen.addstr(0, 0, horizontal)
        for i in range (1,self.life.rows):
            screen.addstr(i, 0, "|")
            screen.addstr(i, self.life.cols+1, "|")
        screen.addstr(self.life.rows, 0, horizontal)


    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for i in range(len(self.life.curr_generation)-1):
            for j in range(len(self.life.curr_generation[i])-1):
                grid=self.life.curr_generation[i][j]
                if grid == 1:
                    screen.addstr(i+1,j+1,"*")
                else:
                    screen.addstr(i+1,j+1," ")

    def run(self) -> None:
        screen = curses.initscr()
        while (self.life.is_max_generations_exceeded and self.life.is_changing):
            self.draw_borders(screen)
            self.draw_grid(screen)
            self.life.step()
            curses.napms(400)
            screen.refresh()
        curses.endwin()


life = GameOfLife((24, 80), max_generations=10)
ui = Console(life)
ui.run()

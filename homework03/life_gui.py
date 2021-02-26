import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 20, speed: int = 5) -> None:
        super().__init__(life)
        self.cell_size=cell_size
        self.speed=speed
        self.height=self.life.rows * self.cell_size
        self.width=self.life.cols * self.cell_size
        self.size=self.width, self.height
        self.screen=pygame.display.set_mode(self.size)

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))
        pass

    def draw_grid(self) -> None:
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                x = j * self.cell_size
                y = i * self.cell_size
                if self.life.curr_generation[i][j] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('green'),(x+1,y+1,self.cell_size-1,self.cell_size-1))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'),
                                     (x + 1, y + 1, self.cell_size - 1, self.cell_size - 1))

        pass

    def run(self) -> None:
        # Copy from previous assignment
        pygame.init()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        if self.life.randomize == False:
            pause = True
        else:
            pause = False
        running = True
        self.draw_lines()
        self.draw_grid()
        self.life.step()
        pygame.display.flip()
        while (running and self.life.is_max_generations_exceeded):
            for event in pygame.event.get():
                if event.type == QUIT:
                    running=False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pause = not pause
                if pause:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button==1:
                            x, y = pygame.mouse.get_pos()
                            x=x//self.cell_size
                            y=y//self.cell_size
                            self.life.curr_generation=self.life.prev_generation
                            if self.life.curr_generation[y][x]==0:
                                self.life.curr_generation[y][x]=1
                            else:
                                self.life.curr_generation[y][x]=0
                            self.draw_lines()
                            self.draw_grid()
                            pygame.display.flip()
            if pause == False:
                self.draw_lines()
                self.draw_grid()
                self.life.step()
                pygame.display.flip()
                pygame.time.Clock().tick(self.speed)
        pygame.quit()


life = GameOfLife((20, 20), randomize=True, max_generations=200)
ui = GUI(life)
ui.run()
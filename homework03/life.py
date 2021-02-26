import pathlib
import random
import typing as tp
import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1
        self.randomize=randomize

    def create_grid(self, randomize: bool = True) -> Grid:
        # Copy from previous assignment
        grid = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                if randomize:
                    row.append(random.randint(0, 1))
                else:
                    row.append(0)
            grid.append(row)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment
        neighbours_cells = []
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i < 0 or i >= self.rows):
                    continue
                if (j < 0 or j >= self.cols):
                    continue
                if (i == cell[0] and j == cell[1]):
                    continue
                neighbours_cells.append(self.curr_generation[i][j])
        return neighbours_cells

    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        next_grid = self.create_grid()
        for i in range(self.rows):
            for j in range(self.cols):
                if self.curr_generation[i][j] == 0:
                    if (sum(self.get_neighbours((i, j))) == 3):
                        next_grid[i][j] = 1
                    else:
                        next_grid[i][j] = 0
                else:
                    if (not 2 <= sum(self.get_neighbours((i, j))) <= 3):
                        next_grid[i][j] = 0
                    else:
                        next_grid[i][j] = 1
        return next_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if ( self.generations > self.max_generations ):
            return (False)
        else:
            return (True)

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if (self.curr_generation == self.prev_generation):
            return (False)
        else:
            return(True)

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, "r") as file:
            list_1 = [i.split() for i in file]
            list_2 = [list(str(list_1[i][0])) for i in range(len(list_1))]
            list_3 = [[int(j) for j in list_2[i]] for i in range(len(list_2))]
            file.close()
            return (list_3)

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        file = open(filename, "w")
        num_1 = ["".join(map(str, self.curr_generation[i])) for i in range(len(self.curr_generation))]
        num_2 = "\n".join(num_1)
        file.write(str(num_2))
        file.close()

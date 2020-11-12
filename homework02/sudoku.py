import pathlib
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    
    return ( [values[n*k:n*(k+1)] for k in range (n)])     


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
  
    return (grid[pos[0]])


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
   
    a=[]
    for i in range (len(grid)):
        a.append(grid[i][pos[1]])
    return (a)


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
   
    a=pos[0]//3*3
    b=pos[1]//3*3
    sq=[]
    for i in range (3):
        for j in range (3):
            sq.append(grid[a+i][b+j])
    return(sq)

def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    
    for i in range (len(grid)):
        for j in range (len(grid[i])):
            if (grid[i][j]=='.'):
                return (i, j)
    return (0)
        
def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
   
    a=set()
    for j in range (1,10):
        i=str(j)
        if (i not in get_block(grid, pos)) and (i not in get_row(grid, pos)) and (i not in get_col(grid, pos)):
            a.add(i)    
    return(a)


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    
    def check(grid: tp.List[tp.List[str]]):
        liz=find_empty_positions(grid)
        if (liz==0):
            return (True)
        else:
            sett=find_possible_values(grid, (liz[0], liz[1]))
            listt=list(sett)
            if (len(listt))==0:
                return (False)
            else:
                for i in listt:
                    grid[liz[0]][liz[1]]=i
                    if check(grid)==True:
                        return(True)
                    else:
                        grid[liz[0]][liz[1]]="."
    check(grid)
    return(grid)     

def check_solution(solution: tp.List[tp.List[str]]) -> bool:

    for i in range (len(solution)):
        for j in range (len(solution)):
            ij=(i,j)
            col=set(get_col(solution, ij))
            row=set(get_row(solution, ij))
            block=set(get_block(solution, ij))
            if (len(col)!=9 or len(row)!=9 or len(block)!=9 or ("." in col) or ("." in row) or ("." in block) ):
                return (False)
    return (True)
            
        
        
def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    pass


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)

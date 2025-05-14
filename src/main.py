from __future__ import annotations
from pathlib import Path
from game import Game
from thing import Thing
import solve
from tabulate import tabulate

def print_solution(sol: list[list[Thing]]) -> None:
    headers = ['Set'] + list(range(1, len(sol) + 1))
    kinds = list(t.kind for t in sol[0])
    cols = [kinds[:], *[g[:] for g in sol]]

    rows = [[] for _ in kinds]

    for col in cols:
        for (i, item) in enumerate(col):
            rows[i].append(item)

    print(tabulate(rows, headers=headers, tablefmt="rounded_grid"))

def print_solutions(solutions: list[list[list[Thing]]]) -> None:
    if not solutions:
        input('Press Enter to quit')
        return

    pad = len(str(len(solutions)))

    i = 0

    choice = input('\nPress Enter to view the first one or Q to quit: ').strip().upper()
    while (choice != 'Q') and (i < len(solutions)):
        print(f'\nSolution # {i+1:>{pad}}/{len(solutions)}')
        print_solution(solutions[i])
        i += 1

        if i < (len(solutions)):
            choice = input('\nPress Enter to view next or Q to quit: ').strip().upper()
        else:
            input('\nAll solutions viewed. Press Enter to finish')

    print('Finished')

def pick_path(L: list[Path]) -> Path:
    choices = sorted(L)
    choice_str = ''
    for (i, path) in enumerate(choices):
        choice_str += f'{i + 1:>2}: {path.stem}\n'
        
    print(f'Games found:\n\n{choice_str}')
    number = int(input('Selection (enter number): '))
    return choices[number - 1]

def run() -> None:
    paths = Path('src/games/').glob('*.json')
    path = pick_path(paths)

    g = Game.parse_json(path)
    g.optimize_clues()
    solutions = solve.find_solutions(g)

    print(f'\nFound {len(solutions)} solution(s).')
    print_solutions(solutions)

if __name__ == '__main__':
    run()

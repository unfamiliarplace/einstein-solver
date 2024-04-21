from __future__ import annotations
from pathlib import Path
from game import Game
from thing import Thing
import solve

def print_solution(sol: list[list[Thing]]) -> None:
    print(sol) # TODO

def print_solutions(solutions: list[list[list[Thing]]]) -> None:
    i = 0
    choice = input('Hit Enter to view the first one or Q to quit: ').strip().upper()
    while (choice != 'Q') and (i < len(solutions)):
        print_solution(solutions[i])
        i += 1
        choice = input('Hit Enter to view next or Q to quit: ').strip().upper()

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
    solutions = solve.find_solutions(g)
    print(f'Found {len(solutions)} solution(s).')
    print_solutions(solutions)

if __name__ == '__main__':
    run()

# TODO Table output
# TODO New game :)

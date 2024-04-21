from __future__ import annotations
import itertools
from pathlib import Path
from thing import Thing
from game import Game

def get_expanded_worlds(worlds: list[list[Thing]], items: set[Thing]):
    for world in worlds:
        for perm in itertools.permutations(items):        
            expanded = []   
            for (base, add) in zip(world, perm):
                item = base[:] + [add]
                expanded.append(item)
            yield expanded

def get_all_worlds(g: Game) -> list[list[Thing]]:
    first, *groups = list(g.sets.values())
    worlds = [[[t] for t in first]]

    for group in groups:
        worlds = list(w for w in get_expanded_worlds(worlds, group))

    return worlds

def realize_world(world: list[list[Thing]]) -> None:
    for group in world:
        first, *rest = group
        for t in rest:
            first.relate(t)

def pick_path(L: list[Path]) -> Path:
    choices = sorted(L)
    choice_str = ''
    for (i, path) in enumerate(choices):
        choice_str += f'{i + 1:>2}: {path.stem}\n'
        
    print(f'Games found:\n\n{choice_str}')
    number = int(input('Selection (enter number): '))
    return choices[number - 1]

def find_solutions(g: Game) -> list[list[Thing]]:
    solutions = []

    g.reset_relationships()

    good = 0
    for world in get_all_worlds(g):
        realize_world(world)

        if g.validate_all_clues():
            solutions.append(world)
        
        g.reset_relationships()
        
    return solutions

def print_solution(sol: list[list[Thing]]) -> None:
    print(sol)

def run() -> None:
    paths = Path('src/games/').glob('*.json')
    path = pick_path(paths)

    g = Game.parse_json(path)
    solutions = find_solutions(g)
    print(f'Found {len(solutions)} solution(s).')

    i = 0
    choice = input('Hit Enter to view the first one or Q to quit: ').strip().upper()
    while (choice != 'Q') and (i < len(solutions)):
        print_solution(solutions[i])
        i += 1
        choice = input('Hit Enter to view next or Q to quit: ').strip().upper()

    print('Finished')

if __name__ == '__main__':
    run()

# TODO Table output
# TODO New game :)

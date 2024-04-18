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

def test_all(g: Game) -> int:
    g.reset_relationships()

    good = 0
    for world in get_all_worlds(g):
        realize_world(world)

        if g.validate_all_clues():
            good += 1
        
        g.reset_relationships()
        
    return good
                    
if __name__ == '__main__':
    g = Game.parse_json(Path('src/games/restaurant.json'))
    n = test_all(g)
    print(f'Found {n} solution(s). Debug to investigate')

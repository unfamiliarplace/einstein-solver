from __future__ import annotations
import itertools
from thing import Thing
import game

def validate_all_clues() -> bool:
    for clue in game.clues:
        if not clue():
            # print(clue.__name__)
            return False
    
    return True

def get_expanded_worlds(worlds: list[list[Thing]], items: set[Thing]):
    for world in worlds:
        for perm in itertools.permutations(items):        
            expanded = []   
            for (base, add) in zip(world, perm):
                item = base[:] + [add]
                expanded.append(item)
            yield expanded

def get_all_worlds() -> list[list[Thing]]:
    worlds = [[[p] for p in game.t1s]]
    worlds = list(w for w in get_expanded_worlds(worlds, game.t2s))
    worlds = list(w for w in get_expanded_worlds(worlds, game.t3s))
    worlds = list(w for w in get_expanded_worlds(worlds, game.t4s))
    return worlds

def realize_world(world: list[list[Thing]]) -> None:
    for group in world:
        t1, t2, t3, t4 = group
        t1.add_t2(t2)
        t1.add_t3(t3)
        t1.add_t4(t4)

def reset_world() -> None:
    for t in game.things:
        t.reset()

def test_all() -> int:
    reset_world()

    good = 0
    for world in get_all_worlds():
        realize_world(world)

        if validate_all_clues():
            good += 1
        
        reset_world()
        
    return good
                    
if __name__ == '__main__':
    n = test_all()
    print(f'Found {n} solution(s). Debug to investigate')

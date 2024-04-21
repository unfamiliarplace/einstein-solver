
import itertools
from thing import Thing
from game import Game

def expand_worlds(worlds: list[list[Thing]], items: set[Thing]):
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
        worlds = list(w for w in expand_worlds(worlds, group))

    return worlds

def realize_world(world: list[list[Thing]]) -> None:
    for group in world:
        first, *rest = group
        for t in rest:
            first.relate(t)

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

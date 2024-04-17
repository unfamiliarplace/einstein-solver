from __future__ import annotations
from thing import Thing
from pathlib import Path
import json

class Symbol:
    name: str

    def __init__(self: Symbol, name: str) -> None:
        self.name = name

    def resolve(self: Symbol, g: Game) -> Thing:
        pass

    def __hash__(self: Symbol) -> int:
        return hash(self.name)

class Rule:
    func: function
    symbols: set[Symbol]

    def __init__(self: Rule) -> None:
        self.func = None
        self.symbols = set()

class Clue:
    rules: list[Rule]

    def __init__(self: Clue) -> None:
        self.rules = []

class Game:
    keys: dict[str, Thing]
    kinds: list[str]
    t1s: set[Thing]
    t2s: set[Thing]
    t3s: set[Thing]
    t4s: set[Thing]
    sets = list[set[Thing]]
    clues: list[function]

    def __init__(self: Game) -> None:
        self.keys = dict()
        self.kinds = list()
        self.t1s = set()
        self.t2s = set()
        self.t3s = set()
        self.t4s = set()
        self.sets = [self.t1s, self.t2s, self.t3s, self.t4s]
        self.clues = list()

    def things(self: Game) -> set[Thing]:
        return self.t1s.union(self.t2s).union(self.t3s).union(self.t4s)

    def __repr__(self: Game) -> str:
        s = ''
        n = len(max(self.kinds, key=len))
        for i in range(len(self.sets)):
            s += f'{self.kinds[i]:{n}} {self.sets[i]}\n'
        
        return s
    
def parse_game(path: Path) -> Game:
    g = Game()

    with open(path, 'r') as f:
        data = json.loads(f.read())
    
    for (i, group) in enumerate(data['kinds']):
        name, things = group['name'], group['things']
        g.kinds.append(name)
        for thing in things:
            t = Thing(thing, name)
            g.sets[i].add(t)
            g.keys[thing] = t

    for (i, group) in enumerate(data['clues']):
        pass
    
    return g
    
g = parse_game(Path('src/games/restaurant.json'))
print(g)

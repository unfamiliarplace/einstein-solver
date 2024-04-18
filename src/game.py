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
    sets: dict[str, set[Thing]]
    clues: list[function]

    def __init__(self: Game) -> None:
        self.keys = dict()
        self.sets = dict()
        self.clues = list()

    def things(self: Game) -> set[Thing]:
        return set(self.keys.values())
    
    def reset_relationships(self: Game) -> None:
        for t in self.things():
            t.reset_relationships()

    def validate_all_clues(self: Game) -> bool:
        for clue in self.clues:
            if not clue():
                # print(clue.__name__)
                return False
        
        return True

    def __repr__(self: Game) -> str:
        s = ''
        n = len(max(self.sets, key=len))
        for (kind, things) in self.sets.items():
            s += f'{kind:{n}} {things}\n'
        
        return s
    
    @staticmethod
    def parse_json(path: Path) -> Game:
        g = Game()

        with open(path, 'r') as f:
            data = json.loads(f.read())
        
        for group in data['kinds']:
            name, things = group['name'], group['things']
            s = set()
            for thing in things:
                t = Thing(thing, name)
                s.add(t)
                g.keys[thing] = t
            g.sets[name] = things

        for (i, group) in enumerate(data['clues']):
            pass
        
        return g

if __name__ == '__main__':
    g = parse_game(Path('src/games/restaurant.json'))
    print(g)

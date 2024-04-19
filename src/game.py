from __future__ import annotations
from thing import Thing
from pathlib import Path
import json

class Symbol:
    name: str

    def __init__(self: Symbol, name: str) -> None:
        self.name = name

    def resolve(self: Symbol, g: Game) -> Thing:
        if '::' not in self.name:
            return g.keys[self.name]
        
        else:
            # TODO Can only do a depth of 1
            key, relationship = self.name.split('::')
            t = g.keys[key]
            return t.relationships[relationship]

    def __hash__(self: Symbol) -> int:
        return hash(self.name)

class Rule:
    json: dict[str, object]
    func: function
    symbols: set[Symbol]
    subrules: list[Rule]

    def __init__(self: Rule, json: dict[str, object]) -> None:
        self.json = json
        self.func, self.symbols, self.subrules = None, set(), list()

        f, args = json['func'], json['args']

        def _and(g: Game) -> bool:
            for r in self.subrules:
                print(r)
                print(r.evaluate(g))
                print()
                return sum(r.evaluate(g) for r in self.subrules) == len(self.subrules)

        def _xor(g: Game) -> bool:
            for r in self.subrules:
                print(r)
                print(r.evaluate(g))
                print()
                return sum(r.evaluate(g) for r in self.subrules) == 1

        match f:
            case 'pair':
                self.func = lambda g: Thing.is_pair(*self.resolve_symbols(g))
            case '-pair':
                self.func = lambda g: not Thing.is_pair(*self.resolve_symbols(g))
            case 'same':
                self.func = lambda g: Thing.is_same(*self.resolve_symbols(g))
            case '-same':
                self.func = lambda g: not Thing.is_same(*self.resolve_symbols(g))

            case 'or':
                self.func = lambda g: any(r.evaluate(g) for r in self.subrules)
            case 'and':
                self.func = _and
                # self.func = lambda g: all(r.evaluate(g) for r in self.subrules)
            case 'xor':
                self.func = _xor
                # self.func = lambda g: sum(r.evaluate(g) for r in self.subrules) == 1
            case 'nand':
                self.func = lambda g: sum(r.evaluate(g) for r in self.subrules) < len(self.subrules)
            case 'nor':
                self.func = lambda g: not any(r.evaluate(g) for r in self.subrules)
        
        base = f in {'pair', '-pair', 'same', '-same'}

        if base:
            self.symbols = set(Symbol(arg) for arg in args)

        else:
            self.subrules = list(Rule(arg) for arg in args)
    
    def evaluate(self: Rule, g: Game) -> bool:
        return self.func(g)
    
    def resolve_symbols(self: Rule, g: Game) -> set[Thing]:
        return set(s.resolve(g) for s in self.symbols)
    
    def __repr__(self: Rule) -> str:
        return repr(self.json)
        # if self.symbols:
        #     return f'{self.func}({",".join((str(s) for s in self.symbols))})'
        # else:
        #     return f'{self.func}({",".join((str(r) for r in self.subrules))})'

class Clue:
    rules: list[Rule]

    def __init__(self: Clue) -> None:
        self.rules = []

    def validate(self: Clue, g: Game) -> bool:
        for r in self.rules:
            if not r.evaluate(g):
                # print(r)
                return False
        else:
            return True
    
    def __repr__(self: Clue) -> str:
        return '\n'.join((str(r) for r in self.rules))

class Game:
    keys: dict[str, Thing]
    sets: dict[str, set[Thing]]
    clues: list[Clue]

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
            if not clue.validate(self):
                # print(clue)
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
            g.sets[name] = s

        for clue in data['clues']:
            c = Clue()
            for json_rule in clue:
                r = Rule(json_rule)
                c.rules.append(r)
            g.clues.append(c)
        
        return g

if __name__ == '__main__':
    g = Game.parse_json(Path('src/games/restaurant.json'))
    # print(g)

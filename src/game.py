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
            key, relationship = self.name.split('::')
            t = g.keys[key]
            return t.relationships[relationship]

    def __hash__(self: Symbol) -> int:
        return hash(self.name)
    
    def __repr__(self: Symbol) -> str:
        return self.name

class Rule:
    json: dict[str, object]
    func: function
    symbols: list[Symbol]
    subrules: list[Rule]

    def __init__(self: Rule, json: dict[str, object]) -> None:
        self.json = json
        self.func, self.symbols, self.subrules = None, list(), list()

        f, args = json['func'], json['args']

        match f:
            case 'link':
                self.func = lambda g: Thing.are_linked(self.resolve_symbols(g))
            case '-link':
                self.func = lambda g: not Thing.are_linked(self.resolve_symbols(g))
            case 'same':
                self.func = lambda g: len(set(self.resolve_symbols(g))) == 1
            case '-same':
                self.func = lambda g: len(set(self.resolve_symbols(g))) > 1

            case "<":
                self.func = lambda g: Thing.are_ascending(self.resolve_symbols(g))
            case ">":
                self.func = lambda g: Thing.are_descending(self.resolve_symbols(g))

            case 'or':
                self.func = lambda g: any(r.evaluate(g) for r in self.subrules)
            case 'and':
                self.func = lambda g: all(r.evaluate(g) for r in self.subrules)
            case 'xor':
                self.func = lambda g: sum(r.evaluate(g) for r in self.subrules) == 1
            case 'nand':
                self.func = lambda g: sum(r.evaluate(g) for r in self.subrules) < len(self.subrules)
            case 'nor' | 'not':
                self.func = lambda g: not any(r.evaluate(g) for r in self.subrules)
        
        basic = f in {'link', '-link', 'same', '-same', '<', '>'}

        if basic:
            self.symbols = list(Symbol(arg) for arg in args)

        else:
            self.subrules = list(Rule(arg) for arg in args)
    
    def evaluate(self: Rule, g: Game) -> bool:
        return self.func(g)
    
    def resolve_symbols(self: Rule, g: Game) -> set[Thing]:
        return [s.resolve(g) for s in self.symbols]
    
    def __repr__(self: Rule) -> str:
        if self.symbols:
            return f'{self.json["func"]}({",".join((str(s) for s in self.symbols))})'
        else:
            return f'{self.json["func"]}({",".join((str(r) for r in self.subrules))})'

class Clue:
    rules: list[Rule]

    def __init__(self: Clue) -> None:
        self.rules = []

    def validate(self: Clue, g: Game) -> bool:
        for r in self.rules:
            if not r.evaluate(g):
                # print('RULE FAILED:', str(r)[:40])
                return False
        
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
                # print('CLUE FAILED:', clue)
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

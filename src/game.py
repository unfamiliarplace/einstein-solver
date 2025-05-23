from __future__ import annotations
from thing import Thing, ThingSort, ThingMath
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

        # Extract the operation argument if it's math
        math = f in {'+', '-', '*', '/', '!+', '!-', '!*', '!/'}
        if math:
            math_result = float(args[0])
            args = args[1:]

        match f:

            # Link
            case 'link':
                self.func = lambda g: Thing.are_linked(self.resolve_symbols(g))
            case '!link':
                self.func = lambda g: not Thing.are_linked(self.resolve_symbols(g))

            # Same
            case 'same':
                self.func = lambda g: len(set(self.resolve_symbols(g))) == 1
            case '!same':
                self.func = lambda g: len(set(self.resolve_symbols(g))) > 1

            # Ascending, descending
            case "<":
                self.func = lambda g: ThingSort.are_ascending(self.resolve_symbols(g))
            case ">":
                self.func = lambda g: ThingSort.are_descending(self.resolve_symbols(g))
            case "!<":
                self.func = lambda g: not ThingSort.are_ascending(self.resolve_symbols(g))
            case "!>":
                self.func = lambda g: not ThingSort.are_descending(self.resolve_symbols(g))

            # Ascending, descending (non-strict)
            case "<=":
                self.func = lambda g: ThingSort.are_ascending_or_equal(self.resolve_symbols(g))
            case ">=":
                self.func = lambda g: ThingSort.are_descending_or_equal(self.resolve_symbols(g))
            case "!<=":
                self.func = lambda g: not ThingSort.are_ascending_or_equal(self.resolve_symbols(g))
            case "!>=":
                self.func = lambda g: not ThingSort.are_descending_or_equal(self.resolve_symbols(g))

            # Ascending, descending (alpha)
            case "<A":
                self.func = lambda g: ThingSort.are_ascending_alpha(self.resolve_symbols(g))
            case ">A":
                self.func = lambda g: ThingSort.are_descending_alpha(self.resolve_symbols(g))
            case "!<A":
                self.func = lambda g: not ThingSort.are_ascending_alpha(self.resolve_symbols(g))
            case "!>A":
                self.func = lambda g: not ThingSort.are_descending_alpha(self.resolve_symbols(g))

            # Ascending, descending (non-strict alpha)
            case "<=A":
                self.func = lambda g: ThingSort.are_ascending_or_equal_alpha(self.resolve_symbols(g))
            case ">=A":
                self.func = lambda g: ThingSort.are_descending_or_equal_alpha(self.resolve_symbols(g))
            case "!<=A":
                self.func = lambda g: not ThingSort.are_ascending_or_equal_alpha(self.resolve_symbols(g))
            case "!>=A":
                self.func = lambda g: not ThingSort.are_descending_or_equal_alpha(self.resolve_symbols(g))

            # Immediately adjacent, whether ascending, descending, or ambivalent
            case "adj":
                self.func = lambda g: ThingSort.are_adjacent(self.resolve_symbols(g))
            case "!adj":
                self.func = lambda g: not ThingSort.are_adjacent(self.resolve_symbols(g))
            case "adj<":
                self.func = lambda g: ThingSort.are_adjacent_ascending(self.resolve_symbols(g))
            case "adj>":
                self.func = lambda g: ThingSort.are_adjacent_descending(self.resolve_symbols(g))
            case "!adj<":
                self.func = lambda g: not ThingSort.are_adjacent_ascending(self.resolve_symbols(g))
            case "!adj>":
                self.func = lambda g: not ThingSort.are_adjacent_descending(self.resolve_symbols(g))

            # Immediately adjacent, whether ascending, descending, or ambivalent (alpha)
            case "adjA":
                self.func = lambda g: ThingSort.are_adjacent_alpha(self.resolve_symbols(g))
            case "!adjA":
                self.func = lambda g: not ThingSort.are_adjacent_alpha(self.resolve_symbols(g))
            case "adj<A":
                self.func = lambda g: ThingSort.are_adjacent_ascending_alpha(self.resolve_symbols(g))
            case "adj>A":
                self.func = lambda g: ThingSort.are_adjacent_descending_alpha(self.resolve_symbols(g))
            case "!adj<A":
                self.func = lambda g: not ThingSort.are_adjacent_ascending_alpha(self.resolve_symbols(g))
            case "!adj>A":
                self.func = lambda g: not ThingSort.are_adjacent_descending_alpha(self.resolve_symbols(g))

            # Math
            case "+":
                self.func = lambda g: ThingMath.sum_is(math_result, self.resolve_symbols(g))
            case "-":
                self.func = lambda g: ThingMath.difference_is(math_result, self.resolve_symbols(g))
            case "*":
                self.func = lambda g: ThingMath.product_is(math_result, self.resolve_symbols(g))
            case "/":
                self.func = lambda g: ThingMath.quotient_is(math_result, self.resolve_symbols(g))
            case "!+":
                self.func = lambda g: not ThingMath.sum_is(math_result, self.resolve_symbols(g))
            case "!-":
                self.func = lambda g: not ThingMath.difference_is(math_result, self.resolve_symbols(g))
            case "!*":
                self.func = lambda g: not ThingMath.product_is(math_result, self.resolve_symbols(g))
            case "!/":
                self.func = lambda g: not ThingMath.quotient_is(math_result, self.resolve_symbols(g))

            # Meta relationships
            case 'or':
                self.func = lambda g: any(r.evaluate(g) for r in self.subrules)
            case 'and':
                self.func = lambda g: all(r.evaluate(g) for r in self.subrules)
            case 'xor':
                self.func = lambda g: sum(r.evaluate(g) for r in self.subrules) == 1
            case 'nand':
                self.func = lambda g: sum(r.evaluate(g) for r in self.subrules) < len(self.subrules)
            case 'nor' | 'not' | '!':
                self.func = lambda g: not any(r.evaluate(g) for r in self.subrules)
        
        basic = f not in {'or', 'and', 'xor', 'nand', 'nor', 'not', '!'}

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
    
    def get_complexity(self: Rule) -> int:
        """
        Return a number indicating the complexity (a function of the subrules).
        The 'link' function is also slower than others, so score it higher.
        """
        return 1 + ('link' in self.json['func']) + sum(r.get_complexity() for r in self.subrules)

class Clue:
    rules: list[Rule]

    def __init__(self: Clue) -> None:
        self.rules = []

    def validate(self: Clue, g: Game) -> bool:
        return all(r.evaluate(g) for r in self.rules)
    
    def __repr__(self: Clue) -> str:
        return '\n'.join((str(r) for r in self.rules))
    
    def optimize_rules(self: Clue) -> None:
        """
        Sort rules by ascending complexity to optimize evaluation.
        """
        self.rules.sort(key=lambda r: r.get_complexity())

    def get_complexity(self: Clue) -> int:
        """
        Return the sum of the complexity of this Clue's Rules.
        """
        return sum(r.get_complexity() for r in self.rules)

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
    
    def optimize_clues(self: Game) -> None:
        """
        Sort Clues by ascending complexity to optimize evaluation.
        """
        for clue in self.clues:
            clue.optimize_rules()
        self.clues.sort(key=lambda c: c.get_complexity())
    
    @staticmethod
    def parse_json(path: Path) -> Game:
        g = Game()

        with open(path, 'r') as f:
            data = json.loads(f.read())
        
        # Parse groups of things
        for group in data['kinds']:
            name, things = group['name'], group['things']
            s = set()
            for thing in things:
                t = Thing(thing, name)
                s.add(t)
                g.keys[thing] = t
            g.sets[name] = s

        # Make each thing aware of its fellows in the kind
        for kind in g.sets:
            for thing in g.sets[kind]:
                thing.fellows = g.sets[kind]

        # Parse clues
        for clue in data['clues']:
            c = Clue()
            for json_rule in clue:
                r = Rule(json_rule)
                c.rules.append(r)
            g.clues.append(c)
        
        return g

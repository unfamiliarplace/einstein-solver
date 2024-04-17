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
    
def parse_game_2(path: Path) -> Game:
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
    
    return g
    
def parse_game(path: Path) -> Game:

    with open(path, 'r') as f:
        g = Game()

        state = 0
        ti = 0
        depth = 0
        rules = []

        for line in map(str.strip, f.readlines()):
            if state == 0:
                k, v = line.split('::')
                if k == 'kind':
                    state = 1
                    g.kinds.append(v)

                elif k == 'clue':
                    state = 2
                    c = Clue()
                    g.clues.append(c)
            
            elif state == 1:
                if not line:
                    state = 0
                    ti += 1

                else:
                    t = Thing(line, g.kinds[ti])
                    g.sets[ti].add(t)
                    g.keys[line] = t
            
            elif state == 2:
                if not line:
                    state = 0
                
                else:
                    pass
            

    return g

g = parse_game_2(Path('src/games/restaurant.json'))
print(g)


# def clue_1() -> bool:
#     return not any((
#         Thing.is_pair(P_Yvette, R_Lyon),
#         Thing.is_pair(P_Yvette, C_14),
#     ))

# def clue_2() -> bool:
#     return not any((
#         Thing.is_pair(C_16, R_Irene),
#         Thing.is_pair(C_16, R_Lyon)
#     ))

# def clue_3() -> bool:
#     if any((
#         Thing.is_pair(R_Lyon, C_17), Thing.is_pair(P_Leon, F_Pork)
#     )):
#         return False
    
#     a = Thing.is_pair(P_Leon, C_17) and Thing.is_pair(F_Pork, R_Lyon)
#     b = Thing.is_pair(P_Leon, R_Lyon) and Thing.is_pair(F_Pork, C_17)

#     return (a + b) == 1

# def clue_4() -> bool:
#     return (R_Charlie.t4, F_Chicken.t4) in (
#         (C_14, C_15),
#         (C_15, C_16),
#         (C_16, C_17)
#     )

# def clue_5() -> bool:
#     if Thing.is_pair(P_Yvette, R_Irene):
#         return False
    
#     return any((
#         Thing.is_pair(F_Pork, P_Yvette),
#         Thing.is_pair(F_Pork, R_Irene)
#     ))

# def clue_6() -> bool:
#     return Thing.is_pair(P_Isac, F_Chicken)

# clues = [
#     clue_1,
#     clue_2,
#     clue_3,
#     clue_4,
#     clue_5,
#     clue_6
# ]

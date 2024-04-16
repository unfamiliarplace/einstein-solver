# This damn thing https://www.ahapuzzles.com/logic/logic-puzzles/christmas-dinner/

from __future__ import annotations
import itertools

class Thing:
    id: str

    food: Thing
    resto: Thing
    person: Thing
    cost: Thing

    def __init__(self: Thing, id: str) -> None:
        self.id = id

        self.resto = None
        self.food = None
        self.cost = None
        self.person = None

    def __hash__(self: Thing) -> int:
        return hash(str(self))
    
    def __repr__(self: Thing) -> str:
        return f'{self.id}'
    
    def __eq__(self: Thing, other: Thing) -> bool:
        return str(self) == str(other)
    
    def things(self: Thing) -> set[Thing]:
        return {self.person, self.cost, self.food, self.resto}
    
    def add_resto(self: Thing, resto: Thing) -> bool:
        self.resto = resto
        resto.person = self

        return True
    
    def add_food(self: Thing, food: Thing) -> bool:
        self.food = food
        food.person = self

        food.resto = self.resto
        self.resto.food = self.food

        return True
    
    def add_cost(self: Thing, cost: Thing) -> bool:
        self.cost = cost
        cost.person = self

        self.food.cost = cost
        cost.food = self.food

        self.resto.cost = cost
        cost.resto = self.resto

        return True

    @staticmethod
    def is_pair(a: Thing, b: Thing) -> bool:
        return any((
            any(((t is b) and (t is not None)) for t in a.things()),
            any(((t is a) and (t is not None)) for t in b.things())
        ))

P_Leon = Thing('Leon')
P_Yvette = Thing('Yvette')
P_Isac = Thing('Isac')
P_Eric = Thing('Eric')
PS = {P_Isac, P_Eric, P_Leon, P_Yvette}

R_Greg = Thing('Greg\'s')
R_Irene = Thing('Irene\'s')
R_Charlie = Thing('Charlie\'s')
R_Lyon = Thing('Lyon\'s')
RS = {R_Greg, R_Irene, R_Charlie, R_Lyon}

F_Ham = Thing('Ham')
F_Turkey = Thing('Turkey')
F_Chicken = Thing('Chicken')
F_Pork = Thing('Pork')
FS = {F_Chicken, F_Ham, F_Pork, F_Turkey}

C_14 = Thing('14.99')
C_15 = Thing('15.99')
C_16 = Thing('16.99')
C_17 = Thing('17.99')
CS = {C_14, C_15, C_16, C_17}

TS = PS.union(CS).union(FS).union(RS)

def validate_clue_1() -> bool:
    return not any((
        Thing.is_pair(P_Yvette, R_Lyon),
        Thing.is_pair(P_Yvette, C_14),
        # Thing.is_pair(C_14, R_Lyon) # Removing this assumption from first clue
    ))

def validate_clue_2() -> bool:
    return not any((
        Thing.is_pair(C_16, R_Irene),
        Thing.is_pair(C_16, R_Lyon)
    ))

def validate_clue_3() -> bool:
    if any((
        Thing.is_pair(R_Lyon, C_17), Thing.is_pair(P_Leon, F_Pork)
    )):
        return False
    
    a = Thing.is_pair(P_Leon, C_17) and Thing.is_pair(F_Pork, R_Lyon)
    b = Thing.is_pair(P_Leon, R_Lyon) and Thing.is_pair(F_Pork, C_17)

    return (a + b) == 1

def validate_clue_4() -> bool:
    return (R_Charlie.cost, F_Chicken.cost) in (
        (C_14, C_15),
        (C_15, C_16),
        (C_16, C_17)
    )

def validate_clue_5() -> bool:
    if Thing.is_pair(P_Yvette, R_Irene):
        return False
    
    return any((
        Thing.is_pair(F_Pork, P_Yvette),
        Thing.is_pair(F_Pork, R_Irene)
    ))

def validate_clue_6() -> bool:
    return Thing.is_pair(P_Isac, F_Chicken)

def validate_all_clues() -> bool:
    for clue in (
        validate_clue_1,
        validate_clue_2,
        validate_clue_3,
        validate_clue_4,
        validate_clue_5,
        validate_clue_6,
    ):
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
    worlds = [[[p] for p in PS]]
    worlds = list(w for w in get_expanded_worlds(worlds, RS))
    worlds = list(w for w in get_expanded_worlds(worlds, FS))
    worlds = list(w for w in get_expanded_worlds(worlds, CS))
    return worlds                            

def realize_world(world: list[list[Thing]]) -> None:
    for group in world:
        p, r, f, c = group
        p.add_resto(r)
        p.add_food(f)
        p.add_cost(c)

def reset_world() -> None:
    for t in TS:
        t.resto = None
        t.food = None
        t.cost = None
        t.person = None

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

from __future__ import annotations

class Thing:
    id: str
    kind: str

    t1: Thing
    t2: Thing
    t3: Thing
    t4: Thing

    def __init__(self: Thing, id: str, kind: str) -> None:
        self.id = id
        self.kind = kind

        self.t1 = None
        self.t2 = None
        self.t3 = None
        self.t4 = None

    def __hash__(self: Thing) -> int:
        return hash(str(self))
    
    def __repr__(self: Thing) -> str:
        return f'{self.id}'
    
    def __eq__(self: Thing, other: Thing) -> bool:
        return str(self) == str(other)
    
    def things(self: Thing) -> set[Thing]:
        return {self.t1, self.t2, self.t3, self.t4}
    
    def reset(self: Thing) -> None:
        self.t1 = None
        self.t2 = None
        self.t3 = None
        self.t4 = None

    def add_t2(self: Thing, t2: Thing) -> bool:
        self.t2 = t2
        t2.t1 = self

        return True
    
    def add_t3(self: Thing, t3: Thing) -> bool:
        self.t3 = t3
        t3.t1 = self

        t3.t2 = self.t2
        self.t2.t3 = self.t3

        return True
    
    def add_t4(self: Thing, t4: Thing) -> bool:
        self.t4 = t4
        t4.t1 = self

        self.t2.t4 = t4
        t4.t2 = self.t2

        self.t3.t4 = t4
        t4.t3 = self.t3

        return True

    @staticmethod
    def is_pair(a: Thing, b: Thing) -> bool:
        return any((
            any(((t is b) and (t is not None)) for t in a.things()),
            any(((t is a) and (t is not None)) for t in b.things())
        ))

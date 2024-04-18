from __future__ import annotations

class Thing:
    id: str
    kind: str
    relationships: dict[str, Thing]

    def __init__(self: Thing, id: str, kind: str) -> None:
        self.id = id
        self.kind = kind
        self.reset()

    def __hash__(self: Thing) -> int:
        return hash(str(self))
    
    def __repr__(self: Thing) -> str:
        return f'{self.id}'
    
    def __eq__(self: Thing, other: Thing) -> bool:
        return str(self) == str(other)
    
    def relations(self: Thing) -> set[Thing]:
        return set(self.relationships.values())
    
    def reset(self: Thing) -> None:
        self.relationships = {
            self.kind: self
        }

    def get(self: Thing, key: str) -> Thing:
        return self.relationships.get(key)
    
    def set(self: Thing, key: str, val: Thing) -> None:
        self.relationships[key] = val

    def relate(self: Thing, other: Thing) -> bool:

        def _pollinate(t1: Thing, t2: Thing) -> None:
            for key in t1.relationships:
                g1 = t1.get(key)
                g2 = t2.get(key)
                if g2 and (g2 is not g1):
                    raise Exception('Conflicting key already exists')
                    # return False
                else:
                    t2.set(key, g1)
        
        success1 = _pollinate(self, other)
        success2 = _pollinate(other, self)
        
        return success1 and success2

    @staticmethod
    def is_pair(a: Thing, b: Thing) -> bool:
        return (b.get(a.kind) is a) and (a.get(b.kind) is a)

    @staticmethod
    def is_same(a: Thing, b: Thing) -> bool:
        return a is b

from __future__ import annotations

class Thing:
    id: str
    kind: str
    relationships: dict[str, Thing]

    def __init__(self: Thing, id: str, kind: str) -> None:
        self.id = id
        self.kind = kind
        self.reset_relationships()

    def __hash__(self: Thing) -> int:
        return hash(str(self))
    
    def __repr__(self: Thing) -> str:
        return f'{self.id}'
    
    def __eq__(self: Thing, other: Thing) -> bool:
        return str(self) == str(other)
    
    def relations(self: Thing) -> set[Thing]:
        return set(self.relationships.values())
    
    def reset_relationships(self: Thing) -> None:
        self.relationships = {
            self.kind: self
        }

    def get(self: Thing, key: str) -> Thing:
        return self.relationships.get(key)
    
    def set(self: Thing, key: str, val: Thing) -> None:
        self.relationships[key] = val

    @staticmethod
    def populate_relationships(d1: dict[str, Thing], d2: dict[str, Thing]) -> dict[str, Thing]:
        for (k, v) in d1.items():
            if d2.get(k) not in (None, v):
                raise Exception('Conflicting key already exists')
            else:
                d2[k] = v

    @staticmethod
    def merge_relationships(d1: dict[str, Thing], d2: dict[str, Thing]) -> dict[str, Thing]:
        d3 = {}
        Thing.populate_relationships(d1, d3)
        Thing.populate_relationships(d2, d3)
        return d3

    def relate(self: Thing, other: Thing) -> bool:
        things = set()
        relationships = {}

        def _compile(t: Thing) -> None:
            for (k, t2) in t.relationships.items():
                if t2 not in things:
                    if relationships.get(k) not in (None, t2):
                        raise Exception('Conflicting key already exists')
                    else:
                        things.add(t2)
                        relationships[k] = t2
                        _compile(t2)
        
        _compile(self)
        _compile(other)

        for t in things:
            for (k, t2) in relationships.items():
                t.relationships[k] = t2        

    @staticmethod
    def is_pair(a: Thing, b: Thing) -> bool:
        return (b.get(a.kind) is a) and (a.get(b.kind) is a)

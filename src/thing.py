from __future__ import annotations
import itertools

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

    def relate(self: Thing, other: Thing) -> bool:
        things = set()
        relationships = {}

        def _compile(t: Thing) -> None:
            for (k, t2) in t.relationships.items():
                if t2 not in things:
                    things.add(t2)
                    relationships[k] = t2
                    _compile(t2)
        
        _compile(self)
        _compile(other)

        for t in things:
            for (k, t2) in relationships.items():
                t.set(k, t2)

    def get_numerical_value(self: Thing) -> int:
        return int(''.join(c for c in self.id if c.isdigit()))

    @staticmethod
    def are_linked(ts: list[Thing]) -> bool:
        """"
        Return True iff the given Things list each other under the respective kinds.
        For example, John and Apples are linked iff John::Food == Apples
        and Apples::Person == John. The linkage must be bidirectional.

        Where there are more than two items, ANY link counts as a link for the list.
        False is returned iff no item is linked with any other.
        """
        for (t1, t2) in itertools.combinations(ts, 2):
            if (t1.get(t2.kind) is t2) and (t2.get(t1.kind) is t1):
                return True
        return False
    
    @staticmethod
    def are_ascending(ts: list[Thing]) -> bool:
        """Strict: every item must actually be lt than the next."""
        nums = list(t.get_numerical_value() for t in ts)
        for i in range(len(nums) - 1):
            if not (nums[i] < nums[i + 1]):
                return False
        return True
    
    @staticmethod
    def are_descending(ts: list[Thing]) -> bool:
        """Strict: every item must actually be gt than the next."""
        nums = list(t.get_numerical_value() for t in ts)
        for i in range(len(nums) - 1):
            if not (nums[i] > nums[i + 1]):
                return False
        return True

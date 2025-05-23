from __future__ import annotations
import itertools
import math

class Thing:
    id: str
    kind: str
    relationships: dict[str, Thing]
    fellows: set[Thing]

    def __init__(self: Thing, id: str, kind: str) -> None:
        self.id = id
        self.kind = kind
        self.fellows = set()
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

    def get_numerical_value(self: Thing) -> int:
        return int(''.join(c for c in self.id if c.isdigit()))

    def get_alphabetical_value(self: Thing) -> int:
        return ''.join(c.casefold() for c in self.id)

class ThingMath:
    epsilon: float = 0.001

    @staticmethod
    def is_near(expected: int|float, result: int|float) -> bool:
        return abs(result - expected) < ThingMath.epsilon
    
    @staticmethod
    def get_numerical_values(ts: list[Thing]) -> list[int]:
        return list(t.get_numerical_value() for t in ts)

    @staticmethod
    def sum_is(expected: int|float, ts: list[Thing]) -> bool:
        return ThingMath.is_near(expected, sum(ThingMath.get_numerical_values(ts)))

    @staticmethod
    def difference_is(expected: int|float, ts: list[Thing]) -> bool:
        result = ts[0].get_numerical_value()
        for t in ts[1:]:
            result -= t.get_numerical_value()

        return ThingMath.is_near(expected, result)

    @staticmethod
    def product_is(expected: int|float, ts: list[Thing]) -> bool:
        return ThingMath.is_near(expected, math.prod(ThingMath.get_numerical_values(ts)))

    @staticmethod
    def quotient_is(expected: int|float, ts: list[Thing]) -> bool:
        result = ts[0].get_numerical_value()
        for t in ts[1:]:
            result /= t.get_numerical_value()

        return ThingMath.is_near(expected, result)

class ThingSort:

    @staticmethod
    def are_ascending(ts: list[Thing]) -> bool:
        """Strict: every item must actually be lt than the next."""
        nums = list(t.get_numerical_value() for t in ts)
        for i in range(len(nums) - 1):
            if not (nums[i] < nums[i + 1]):
                return False
        return True
    
    @staticmethod
    def are_ascending_or_equal(ts: list[Thing]) -> bool:
        nums = list(t.get_numerical_value() for t in ts)
        for i in range(len(nums) - 1):
            if not (nums[i] <= nums[i + 1]):
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
    
    @staticmethod
    def are_descending_or_equal(ts: list[Thing]) -> bool:
        nums = list(t.get_numerical_value() for t in ts)
        for i in range(len(nums) - 1):
            if not (nums[i] >= nums[i + 1]):
                return False
        return True
    
    @staticmethod
    def are_ascending_alpha(ts: list[Thing]) -> bool:
        """Strict: every item must actually be lt than the next."""
        vals = list(t.id for t in ts)
        for i in range(len(vals) - 1):
            if not (vals[i] < vals[i + 1]):
                return False
        return True
    
    @staticmethod
    def are_ascending_or_equal_alpha(ts: list[Thing]) -> bool:
        """Strict: every item must actually be lt than the next."""
        vals = list(t.id for t in ts)
        for i in range(len(vals) - 1):
            if not (vals[i] <= vals[i + 1]):
                return False
        return True
    
    @staticmethod
    def are_descending_alpha(ts: list[Thing]) -> bool:
        """Strict: every item must actually be gt than the next."""
        vals = list(t.id for t in ts)
        for i in range(len(vals) - 1):
            if not (vals[i] > vals[i + 1]):
                return False
        return True
    
    @staticmethod
    def are_descending_or_equal_alpha(ts: list[Thing]) -> bool:
        """Strict: every item must actually be gt than the next."""
        vals = list(t.id for t in ts)
        for i in range(len(vals) - 1):
            if not (vals[i] >= vals[i + 1]):
                return False
        return True

    @staticmethod
    def are_adjacent(ts: list[Thing]) -> bool:
        nums = list(t.get_numerical_value() for t in ts)
        nums_ordered = sorted(list(t.get_numerical_value() for t in ts[0].fellows))
        for i in range(len(nums) - 1):
            ia = nums_ordered.index(nums[i])
            ib = nums_ordered.index(nums[i + 1])
            if abs(ia - ib) > 1:
                return False
        return True

    @staticmethod
    def are_adjacent_ascending(ts: list[Thing]) -> bool:
        nums = list(t.get_numerical_value() for t in ts)
        nums_ordered = sorted(list(t.get_numerical_value() for t in ts[0].fellows))
        for i in range(len(nums) - 1):
            ia = nums_ordered.index(nums[i])
            ib = nums_ordered.index(nums[i + 1])
            if (ib - ia) != 1:
                return False
        return True
    
    @staticmethod
    def are_adjacent_descending(ts: list[Thing]) -> bool:
        nums = list(t.get_numerical_value() for t in ts)
        nums_ordered = sorted(list(t.get_numerical_value() for t in ts[0].fellows))
        for i in range(len(nums) - 1):
            ia = nums_ordered.index(nums[i])
            ib = nums_ordered.index(nums[i + 1])
            if (ia - ib) != 1:
                return False
        return True

    @staticmethod
    def are_adjacent_alpha(ts: list[Thing]) -> bool:
        vals = list(t.get_alphabetical_value() for t in ts)
        vals_ordered = sorted(list(t.get_alphabetical_value() for t in ts[0].fellows))
        for i in range(len(vals) - 1):
            ia = vals_ordered.index(vals[i])
            ib = vals_ordered.index(vals[i + 1])
            if abs(ia - ib) > 1:
                return False
        return True

    @staticmethod
    def are_adjacent_ascending_alpha(ts: list[Thing]) -> bool:
        vals = list(t.get_alphabetical_value() for t in ts)
        vals_ordered = sorted(list(t.get_alphabetical_value() for t in ts[0].fellows))
        for i in range(len(vals) - 1):
            ia = vals_ordered.index(vals[i])
            ib = vals_ordered.index(vals[i + 1])
            if (ib - ia) != 1:
                return False
        return True
    
    @staticmethod
    def are_adjacent_descending_alpha(ts: list[Thing]) -> bool:
        vals = list(t.get_alphabetical_value() for t in ts)
        vals_ordered = sorted(list(t.get_alphabetical_value() for t in ts[0].fellows))
        for i in range(len(vals) - 1):
            ia = vals_ordered.index(vals[i])
            ib = vals_ordered.index(vals[i + 1])
            if (ia - ib) != 1:
                return False
        return True

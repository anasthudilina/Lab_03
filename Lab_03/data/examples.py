"""
Демонстрація iterable/iterator, власного iterator class,
generator functions, yield, yield from, generator expression, itertools.
"""

from itertools import islice, count, accumulate, pairwise, chain


# === 1. Власний iterator class ===
class AccountNumberIterator:
    """Iterator, що генерує послідовні номери рахунків UA0000000001..UA000000000N."""

    def __init__(self, start: int, stop: int) -> None:
        self.current = start
        self.stop = stop

    def __iter__(self):
        return self

    def __next__(self) -> str:
        if self.current >= self.stop:
            raise StopIteration
        number = f"UA{self.current:010d}"
        self.current += 1
        return number


class AccountNumberRange:
    """Iterable (не iterator): кожен виклик iter() створює новий iterator."""

    def __init__(self, start: int, stop: int) -> None:
        self.start = start
        self.stop = stop

    def __iter__(self):
        return AccountNumberIterator(self.start, self.stop)


# === 2. Generator function ===
def generate_operations(limit: int):
    for i in range(limit):
        yield ("deposit", 100.0 + i)
        yield ("withdraw", 50.0 + i)


# === 3. yield from ===
def flatten(nested):
    for value in nested:
        if isinstance(value, list):
            yield from flatten(value)
        else:
            yield value


# === 4. Generator expression vs list comprehension ===
squares_gen = (x * x for x in range(10))
squares_list = [x * x for x in range(10)]


# === 5. itertools ===
def itertools_demo():
    print("islice(count(1), 5) =", list(islice(count(1), 5)))

    balances = [1000, 500, 2000, 700]
    print("accumulate =", list(accumulate(balances)))

    print("pairwise differences:")
    for prev, curr in pairwise(balances):
        print(f"  {prev} -> {curr} (diff={curr - prev})")

    print("chain =", list(chain([1, 2], [3, 4], [5])))


if __name__ == "__main__":
    print("=== Custom iterator ===")
    rng = AccountNumberRange(1, 4)
    print("First pass: ", list(rng))
    print("Second pass:", list(rng))  # iterable -> можна проходити повторно

    iterator = iter(rng)
    print("iter(iterator) is iterator:", iter(iterator) is iterator)
    print("list(iterator):", list(iterator))
    print("list(iterator) again (one-shot):", list(iterator))

    print("\n=== Generator function ===")
    for op in generate_operations(2):
        print(op)

    print("\n=== yield from (flatten) ===")
    nested = [1, [2, 3], [4, [5, 6]]]
    print(list(flatten(nested)))

    print("\n=== Generator expr vs list comp ===")
    print("squares_list:         ", squares_list)
    print("squares_gen (consumed):", list(squares_gen))
    print("squares_gen again:    ", list(squares_gen))  # exhausted

    print("\n=== itertools ===")
    itertools_demo()
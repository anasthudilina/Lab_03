from itertools import islice, count, accumulate, pairwise, chain


class AccountNumberIterator:
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
    def __init__(self, start: int, stop: int) -> None:
        self.start = start
        self.stop = stop

    def __iter__(self):
        return AccountNumberIterator(self.start, self.stop)


def generate_operations(limit: int):
    for i in range(limit):
        yield ("deposit", 100.0 + i)
        yield ("withdraw", 50.0 + i)


def flatten(nested):
    for value in nested:
        if isinstance(value, list):
            yield from flatten(value)
        else:
            yield value


if __name__ == "__main__":
    print("=== Custom iterator ===")
    rng = AccountNumberRange(1, 4)
    print("First pass: ", list(rng))
    print("Second pass:", list(rng))

    iterator = iter(rng)
    print("iter(iterator) is iterator:", iter(iterator) is iterator)
    print("list(iterator):", list(iterator))
    print("list(iterator) again (one-shot):", list(iterator))

    print("\\n=== Generator function ===")
    for op in generate_operations(2):
        print(op)

    print("\\n=== yield from (flatten) ===")
    print(list(flatten([1, [2, 3], [4, [5, 6]]])))

    print("\\n=== itertools ===")
    print("islice(count(1), 5) =", list(islice(count(1), 5)))
    print("accumulate =", list(accumulate([1000, 500, 2000, 700])))
    for prev, curr in pairwise([1000, 500, 2000, 700]):
        print(f"  {prev} -> {curr} (diff={curr - prev})")
    print("chain =", list(chain([1, 2], [3, 4], [5])))

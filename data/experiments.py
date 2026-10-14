"""
Порівняння eager та lazy підходів:
- elapsed time
- peak memory (tracemalloc)
- time-to-first-result
"""

import csv
import time
import tracemalloc
from itertools import islice
from pathlib import Path

from stream_processor.pipeline import build_pipeline


# ---------- Eager: матеріалізує весь dataset ----------
def eager_load(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


# ---------- Lazy: споживає pipeline повністю ----------
def lazy_consume(path: Path) -> int:
    count = 0
    for _ in build_pipeline(path, min_balance=0):
        count += 1
    return count


# ---------- Lazy: тільки перший результат ----------
def lazy_first_result(path: Path):
    pipeline = build_pipeline(path, min_balance=0)
    return next(iter(pipeline))


# ---------- Eager: перший результат ----------
def eager_first_result(path: Path):
    data = eager_load(path)
    return data[0] if data else None


def measure(func, *args):
    tracemalloc.start()
    t0 = time.perf_counter()
    result = func(*args)
    elapsed = time.perf_counter() - t0
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return result, elapsed, peak


def main() -> None:
    print(f"{'Records':>10} | {'Eager s':>8} | {'Lazy s':>8} | "
          f"{'Eager MB':>9} | {'Lazy MB':>9} | "
          f"{'Eager t2first':>14} | {'Lazy t2first':>13}")
    print("-" * 95)

    for n in (10_000, 100_000, 500_000):
        path = Path(f"data/accounts_{n}.csv")
        if not path.exists():
            print(f"skip {path} (not found)")
            continue

        # повне споживання
        _, eager_time, eager_mem = measure(eager_load, path)
        _, lazy_time, lazy_mem = measure(lazy_consume, path)

        # time-to-first-result
        _, eager_t2f, _ = measure(eager_first_result, path)
        _, lazy_t2f, _ = measure(lazy_first_result, path)

        print(
            f"{n:>10} | "
            f"{eager_time:>8.3f} | {lazy_time:>8.3f} | "
            f"{eager_mem / 1e6:>9.2f} | {lazy_mem / 1e6:>9.2f} | "
            f"{eager_t2f:>14.6f} | {lazy_t2f:>13.6f}"
        )


if __name__ == "__main__":
    main()
from itertools import islice
from pathlib import Path

from stream_processor.pipeline import build_pipeline
from stream_processor.analytics import (
    calculate_statistics,
    find_account,
    top_n_by_balance,
)
from stream_processor.batches import batched


def main() -> None:
    path = Path("data/accounts.csv")

    print("=== First 5 operations with new_balance >= 5000 ===")
    pipeline = build_pipeline(path, min_balance=5000)
    for rec in islice(pipeline, 5):
        print(rec)

    print("\\n=== Statistics ===")
    pipeline = build_pipeline(path, min_balance=0)
    stats = calculate_statistics(pipeline)
    for key, value in stats.items():
        print(f"{key}: {value}")

    print("\\n=== Top 5 accounts by new balance ===")
    pipeline = build_pipeline(path, min_balance=0)
    for rec in top_n_by_balance(pipeline, 5):
        print(rec)

    print("\\n=== Batch processing (batch_size=3) ===")
    pipeline = build_pipeline(path, min_balance=0)
    for i, batch in enumerate(batched(pipeline, 3)):
        print(f"Batch {i + 1}:")
        for rec in batch:
            print(f"  {rec}")
        if i >= 2:
            break


if __name__ == "__main__":
    main()

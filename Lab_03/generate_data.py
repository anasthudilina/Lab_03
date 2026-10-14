import csv
import random
from pathlib import Path


def generate_test_file(path: Path, count: int) -> None:
    clients = [
        "Ivanenko", "Petrenko", "Shevchenko", "Kovalenko",
        "Bondarenko", "Melnyk", "Tkachenko", "Kravchenko",
    ]
    operations = ["deposit", "withdraw"]

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["account_number", "client", "balance", "operation", "amount"])
        for i in range(count):
            acc = f"UA{random.randint(0, 9_999_999_999):010d}"
            client = random.choice(clients)
            balance = round(random.uniform(0, 50_000), 2)
            operation = random.choice(operations)
            amount = round(random.uniform(10, 5_000), 2)
            writer.writerow([acc, client, balance, operation, amount])


if __name__ == "__main__":
    for n in (10_000, 100_000, 500_000):
        p = Path(f"data/accounts_{n}.csv")
        generate_test_file(p, n)
        print(f"Generated {p} ({n} records)")
    generate_test_file(Path("data/accounts.csv"), 1000)
    print("Generated data/accounts.csv (1000 records)")

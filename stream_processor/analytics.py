from collections import Counter
from collections.abc import Iterable
from heapq import nlargest
from typing import Any, Optional

from .models import ProcessedOperation


def calculate_statistics(records: Iterable[ProcessedOperation]) -> dict[str, Any]:
    count = 0
    total_balance = 0.0
    min_balance: Optional[float] = None
    max_balance: Optional[float] = None
    deposits_total = 0.0
    withdrawals_total = 0.0
    rejected = 0
    clients: Counter[str] = Counter()

    for rec in records:
        count += 1
        total_balance += rec.new_balance
        if min_balance is None or rec.new_balance < min_balance:
            min_balance = rec.new_balance
        if max_balance is None or rec.new_balance > max_balance:
            max_balance = rec.new_balance
        if rec.operation == "deposit":
            deposits_total += rec.amount
        else:
            withdrawals_total += rec.amount
        if not rec.applied:
            rejected += 1
        clients[rec.client] += 1

    return {
        "count": count,
        "total_balance": total_balance,
        "average_balance": total_balance / count if count else 0.0,
        "minimum_balance": min_balance,
        "maximum_balance": max_balance,
        "deposits_total": deposits_total,
        "withdrawals_total": withdrawals_total,
        "rejected_withdrawals": rejected,
        "clients": dict(clients),
    }


def find_account(records, account_number) -> Optional[ProcessedOperation]:
    for rec in records:
        if rec.account_number == account_number:
            return rec
    return None


def top_n_by_balance(records, n: int) -> list[ProcessedOperation]:
    return nlargest(n, records, key=lambda r: r.new_balance)

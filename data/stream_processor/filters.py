import re
from collections.abc import Iterable, Iterator

from .models import BankOperation, ProcessedOperation

ACCOUNT_RE = re.compile(r"^UA\d{10}$")
VALID_OPERATIONS = {"deposit", "withdraw"}


def validate_operations(
    rows: Iterable[dict[str, str]],
) -> Iterator[BankOperation]:
    """Streaming validation: номер рахунку, баланс, операція, сума."""
    for row in rows:
        try:
            account_number = row["account_number"].strip()
            client = row["client"].strip()
            balance = float(row["balance"])
            operation = row["operation"].strip().lower()
            amount = float(row["amount"])
        except (ValueError, TypeError, KeyError):
            continue

        if not ACCOUNT_RE.match(account_number):
            continue
        if not client:
            continue
        if balance < 0:
            continue
        if operation not in VALID_OPERATIONS:
            continue
        if amount <= 0:
            continue

        yield BankOperation(
            account_number=account_number,
            client=client,
            balance=balance,
            operation=operation,
            amount=amount,
        )


def apply_operations(
    records: Iterable[BankOperation],
) -> Iterator[ProcessedOperation]:
    """Потокове застосування операцій із захистом від від'ємного балансу."""
    for rec in records:
        if rec.operation == "deposit":
            new_balance = rec.balance + rec.amount
            applied = True
        else:  # withdraw
            if rec.balance - rec.amount < 0:
                new_balance = rec.balance
                applied = False       # відхилено
            else:
                new_balance = rec.balance - rec.amount
                applied = True

        yield ProcessedOperation(
            account_number=rec.account_number,
            client=rec.client,
            old_balance=rec.balance,
            operation=rec.operation,
            amount=rec.amount,
            new_balance=new_balance,
            applied=applied,
        )


def filter_by_client(
    records: Iterable[ProcessedOperation],
    client: str,
) -> Iterator[ProcessedOperation]:
    for rec in records:
        if rec.client == client:
            yield rec


def filter_by_balance_threshold(
    records: Iterable[ProcessedOperation],
    minimum: float,
) -> Iterator[ProcessedOperation]:
    for rec in records:
        if rec.new_balance >= minimum:
            yield rec


def filter_applied(
    records: Iterable[ProcessedOperation],
) -> Iterator[ProcessedOperation]:
    for rec in records:
        if rec.applied:
            yield rec
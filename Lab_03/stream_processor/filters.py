import re
from collections.abc import Iterable, Iterator

from .models import BankOperation, ProcessedOperation

ACCOUNT_RE = re.compile(r"^UA\d{10}$")
VALID_OPERATIONS = {"deposit", "withdraw"}


def validate_operations(rows: Iterable[dict[str, str]]) -> Iterator[BankOperation]:
    for row in rows:
        if row is None:
            continue
        if None in row.values():
            continue
        try:
            account_number = (row.get("account_number") or "").strip()
            client = (row.get("client") or "").strip()
            balance = float(row.get("balance") or "")
            operation = (row.get("operation") or "").strip().lower()
            amount = float(row.get("amount") or "")
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


def apply_operations(records: Iterable[BankOperation]) -> Iterator[ProcessedOperation]:
    for rec in records:
        if rec.operation == "deposit":
            new_balance = rec.balance + rec.amount
            applied = True
        else:
            if rec.balance - rec.amount < 0:
                new_balance = rec.balance
                applied = False
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


def filter_by_client(records, client):
    for rec in records:
        if rec.client == client:
            yield rec


def filter_by_balance_threshold(records, minimum):
    for rec in records:
        if rec.new_balance >= minimum:
            yield rec


def filter_applied(records):
    for rec in records:
        if rec.applied:
            yield rec

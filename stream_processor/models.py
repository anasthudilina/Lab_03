from typing import NamedTuple


class BankOperation(NamedTuple):
    account_number: str
    client: str
    balance: float
    operation: str
    amount: float


class ProcessedOperation(NamedTuple):
    account_number: str
    client: str
    old_balance: float
    operation: str
    amount: float
    new_balance: float
    applied: bool

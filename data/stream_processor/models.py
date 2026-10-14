from typing import NamedTuple


class BankOperation(NamedTuple):
    """Валідована операція до застосування."""
    account_number: str
    client: str
    balance: float
    operation: str          # "deposit" або "withdraw"
    amount: float


class ProcessedOperation(NamedTuple):
    """Результат застосування операції до балансу."""
    account_number: str
    client: str
    old_balance: float
    operation: str
    amount: float
    new_balance: float
    applied: bool            # False — якщо зняття відхилено
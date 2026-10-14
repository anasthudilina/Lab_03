from collections.abc import Iterable, Iterator

from .models import ProcessedOperation


def normalize_clients(
    records: Iterable[ProcessedOperation],
) -> Iterator[ProcessedOperation]:
    """Нормалізує імена клієнтів (Title Case)."""
    for rec in records:
        yield rec._replace(client=rec.client.title())


def mask_account_numbers(
    records: Iterable[ProcessedOperation],
    visible: int = 4,
) -> Iterator[ProcessedOperation]:
    """Маскує номер рахунку, залишаючи останні visible символів."""
    for rec in records:
        acc = rec.account_number
        masked = "*" * (len(acc) - visible) + acc[-visible:]
        yield rec._replace(account_number=masked)
from pathlib import Path
from collections.abc import Iterator

from .readers import read_lines
from .parsers import parse_csv_rows
from .filters import (
    validate_operations,
    apply_operations,
    filter_by_balance_threshold,
)
from .transformations import normalize_clients
from .models import ProcessedOperation


def build_pipeline(path: Path, min_balance: float = 0.0) -> Iterator[ProcessedOperation]:
    lines = read_lines(path)
    rows = parse_csv_rows(lines)
    valid = validate_operations(rows)
    applied = apply_operations(valid)
    normalized = normalize_clients(applied)
    filtered = filter_by_balance_threshold(normalized, min_balance)
    return filtered

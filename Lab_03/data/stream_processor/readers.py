from pathlib import Path
from collections.abc import Iterator


def read_lines(path: Path) -> Iterator[str]:
    """Читає файл рядок за рядком, не завантажуючи його повністю в RAM."""
    with path.open("r", encoding="utf-8") as file:
        yield from file
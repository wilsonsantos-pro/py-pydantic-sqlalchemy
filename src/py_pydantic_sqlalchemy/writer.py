from pathlib import Path


def write(code: str, dest: Path) -> None:
    with open(dest, "w", encoding="utf8") as fdest:
        fdest.write(code)

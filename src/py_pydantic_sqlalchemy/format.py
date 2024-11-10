import black
import isort


def format_code(code: str) -> str:
    config = isort.Config(
        known_standard_library=["os", "sys"],
        known_third_party=["requests"],
        include_trailing_comma=True,
    )

    return isort.code(black.format_str(code, mode=black.Mode()), config=config)

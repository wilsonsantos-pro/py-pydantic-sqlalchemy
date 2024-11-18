from pathlib import Path

from py_pydantic_sqlalchemy.generator import pydantic_to_sqlalchemy_code


def test_pydantic_to_sqlalchemy_code():
    test_src = Path(__file__).parent / "test_data" / "pydantic_user.py"
    with open(
        Path(__file__).parent / "test_data" / "sqla_user.py", encoding="utf-8"
    ) as fexpected:
        expected = fexpected.read()

    assert pydantic_to_sqlalchemy_code(str(test_src), None) == expected

import pytest

from py_pydantic_sqlalchemy.utils import camel_to_snake, snake_to_camel


@pytest.mark.parametrize(
    "value,expected",
    [
        ("A", "a"),
        ("AA", "a_a"),
        ("AaB", "aa_b"),
        ("AaBb", "aa_bb"),
        ("AaBB", "aa_b_b"),
    ],
)
def test_camel_to_snake(value: str, expected: str):
    assert camel_to_snake(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("a", "A"),
        ("a_a", "AA"),
        ("aa_b", "AaB"),
        ("aa_bb", "AaBb"),
        ("aa_b_b", "AaBB"),
    ],
)
def test_snake_to_camel(value: str, expected: str):
    assert snake_to_camel(value) == expected

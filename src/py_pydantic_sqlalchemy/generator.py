from pydantic import BaseModel

from .format import format_code
from .parser import ParserConfig, parse_pydantic_model
from .reflection import get_classes_from_package_path
from .renderer import render_all


def pydantic_to_sqlalchemy_code(
    src: str, parser_config: ParserConfig | None = None
) -> str:
    parse_results = []
    for pydantic_model in get_classes_from_package_path(
        src, lambda obj: issubclass(obj, BaseModel) and not obj == BaseModel
    ):
        parse_results.append(parse_pydantic_model(pydantic_model, parser_config))

    return format_code(render_all(parse_results))

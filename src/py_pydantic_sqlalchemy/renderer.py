from functools import lru_cache
from pathlib import Path

from mako.lookup import TemplateLookup

from .parser import ParseResult


@lru_cache
def _template_loader() -> TemplateLookup:
    return TemplateLookup(directories=Path(__file__).parent / "templates/")


def render(parse_result: ParseResult) -> str:
    template_loader = _template_loader()

    model_template = template_loader.get_template("model_template.mako")
    models_code = model_template.render(
        models=parse_result.models,
        include_relationship=False,
    )
    return str(models_code)


def render_all(parse_results: list[ParseResult]) -> str:
    template_loader = _template_loader()

    imports = []
    global_defs = []
    models = []

    for parse_result in parse_results:
        imports += parse_result.imports
        global_defs += parse_result.global_defs
        models += parse_result.models

    model_template = template_loader.get_template("model_template.mako")
    all_models_code = model_template.render(
        models=models,
        include_relationship=False,
        imports=imports,
        global_defs=set(global_defs),
    )
    return str(all_models_code)

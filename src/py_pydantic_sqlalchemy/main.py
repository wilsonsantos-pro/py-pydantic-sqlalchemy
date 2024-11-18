import argparse
from pathlib import Path

import yaml
from dacite import from_dict

from py_pydantic_sqlalchemy.generator import pydantic_to_sqlalchemy_code
from py_pydantic_sqlalchemy.model import ModelBase
from py_pydantic_sqlalchemy.parser import ParserConfig
from py_pydantic_sqlalchemy.writer import write


def main(src: str, dest: Path, parser_settings: str):
    if parser_settings:
        with open(parser_settings, encoding="utf-8") as settings_f:
            data = yaml.load(settings_f, yaml.Loader)
            model_bases = [
                from_dict(ModelBase, model_base)
                for model_base in data.get("model_bases", [])
            ]

        parser_config = ParserConfig(model_bases=model_bases)
    else:
        parser_config = ParserConfig()

    code = pydantic_to_sqlalchemy_code(src, parser_config)
    write(code, dest)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "src", type=str, help="The source code file to read the models from from"
    )
    parser.add_argument("dest", type=str, help="Where to write the code to")
    parser.add_argument("-p", "--parser-config", type=str)
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")

    args = parser.parse_args()

    main(args.src, Path(args.dest), args.parser_config)

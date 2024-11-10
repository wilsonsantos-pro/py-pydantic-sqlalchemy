import argparse
from pathlib import Path

from py_pydantic_sqlalchemy.generator import pydantic_to_sqlalchemy_code
from py_pydantic_sqlalchemy.writer import write


def main(src: str, dest: Path):
    code = pydantic_to_sqlalchemy_code(src)
    write(code, dest)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "src", type=str, help="The source code file to read the models from from"
    )
    parser.add_argument("dest", type=str, help="Where to write the code to")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")

    args = parser.parse_args()

    main(args.src, Path(args.dest))

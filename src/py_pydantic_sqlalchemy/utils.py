import re


def camel_to_snake(string: str):
    return re.sub(r"([A-Z])", r"_\1", string).lower().strip("_")


def snake_to_camel(snake_str):
    return snake_str.title().replace("_", "")

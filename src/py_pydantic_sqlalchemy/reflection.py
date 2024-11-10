import importlib.util
import inspect
from pathlib import PurePath


def get_classes_from_package_path(package_path: str, class_filter=lambda _: True):
    classes_in_package = []
    path = PurePath(package_path)
    module_name = path.name

    spec = importlib.util.spec_from_file_location(module_name, str(path))
    if not spec:
        return classes_in_package
    if not spec.loader:
        return classes_in_package

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    for _name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and class_filter(obj):
            classes_in_package.append(obj)
    return classes_in_package

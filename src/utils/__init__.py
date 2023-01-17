import re
import sys
import inspect
from abc import ABC
from types import ModuleType
from typing import Union


def print_bool(value: bool) -> bool:
    """
    Convenience function that prints a boolean as Yes or No for presentation
    purposes and, then, returns the value afterwards.
    """
    print("Yes" if value else "No")
    return value


def get_classes(module_or_name: Union[str, ModuleType]) -> dict[str, type]:
    """
    Dynamically lists the classes for a module.
    :param module_or_name: Either the module itself, or the name for the
    module.
    :return: A dictionary mapping a class name to a class object.
    """

    classes = {}

    # Loop over each subobject of the given module.
    for submodule_name, submodule_obj in inspect.getmembers(
        sys.modules[module_or_name] if isinstance(module_or_name, str) else module_or_name
    ):
        # Check that the subobject is a submodule.
        if inspect.ismodule(submodule_obj):
            # Find all members of the submodule.
            for name, obj in inspect.getmembers(submodule_obj):
                # Find any object that is a class but not an immediate
                # descendent of ABC (the abstract base class).
                if inspect.isclass(obj) and not obj.mro()[1] == ABC:
                    classes[normalize_name(name)] = obj

    return classes


def normalize_name(name):
    name = name.replace("_", ".")
    return name[0] + re.sub('([^.])([A-Z0-9])', r'\1 \2', name[1:])


# Import base classes.
from .question import Question

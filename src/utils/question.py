from typing import Optional

from utils import normalize_name
from abc import ABC


class Question(ABC):

    def __init__(self, name: Optional[str] = None):
        self.name: str = name if name is not None else normalize_name(self.__class__.__name__)
        """The name of the current question."""

        self.current_step: int = 1
        """The current step number being executed."""

    def set_current_step(self, current_step: int):
        """Sets the current step number to the specified value."""
        self.current_step = current_step

    def reset_steps(self):
        self.set_current_step(1)

    def begin_step(self, description):
        """Prints a banner and increments the current step."""
        print()
        print("\u001b[31;1m>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\u001b[0m")
        print(f"\u001b[31;1m>>> {self.name}, Step #{self.current_step}\u001b[0m")
        print(f"\u001b[31;1m>>> {description}\u001b[0m")
        print()
        self.current_step += 1

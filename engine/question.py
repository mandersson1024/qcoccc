from abc import ABC, abstractmethod


class Question(ABC):
    @property
    @abstractmethod
    def key(self) -> str:
        """Key under which the answer is stored in the context dict."""

    @abstractmethod
    def ask(self, context: dict):
        """Present the question to the user and return the answer."""

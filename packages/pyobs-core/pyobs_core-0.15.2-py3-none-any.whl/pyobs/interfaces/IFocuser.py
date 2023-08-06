from abc import ABCMeta, abstractmethod
from typing import Any

from .IMotion import IMotion


class IFocuser(IMotion, metaclass=ABCMeta):
    """The module is a focusing device."""

    __module__ = "pyobs.interfaces"

    @abstractmethod
    async def set_focus(self, focus: float, **kwargs: Any) -> None:
        """Sets new focus.

        Args:
            focus: New focus value.

        Raises:
            InterruptedError: If focus was interrupted.
        """
        ...

    @abstractmethod
    async def set_focus_offset(self, offset: float, **kwargs: Any) -> None:
        """Sets focus offset.

        Args:
            offset: New focus offset.

        Raises:
            InterruptedError: If focus was interrupted.
        """
        ...

    @abstractmethod
    async def get_focus(self, **kwargs: Any) -> float:
        """Return current focus.

        Returns:
            Current focus.
        """
        ...

    @abstractmethod
    async def get_focus_offset(self, **kwargs: Any) -> float:
        """Return current focus offset.

        Returns:
            Current focus offset.
        """
        ...


__all__ = ["IFocuser"]

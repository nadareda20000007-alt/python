from abc import ABC, abstractmethod


class NavigationService(ABC):
    @abstractmethod
    def update_target(self, axes: list) -> None:
        pass
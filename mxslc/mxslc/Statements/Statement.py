from abc import ABC, abstractmethod


# TODO add expression statement so I can do this: standard_surface(base_color=color3(...));
class Statement(ABC):
    @abstractmethod
    def execute(self) -> None:
        ...

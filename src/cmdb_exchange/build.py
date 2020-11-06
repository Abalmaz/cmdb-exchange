from abc import abstractmethod, ABCMeta


class Builder(metaclass=ABCMeta):

    @abstractmethod
    def build_structure(self) -> None:
        pass

    @abstractmethod
    def build_item(self) -> None:
        pass


class CmdbItemBuilder(Builder):
    def build_structure(self) -> None:
        pass

    def build_item(self) -> None:
        pass

class Builder:

    def build_structure(self) -> None:
        raise NotImplementedError

    def build_item(self) -> None:
        raise NotImplementedError


class CmdbItemBuilder(Builder):
    def build_structure(self) -> None:
        pass

    def build_item(self) -> None:
        pass

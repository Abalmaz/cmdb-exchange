class Builder:

    def reset(self) -> None:
        raise NotImplementedError

    def prepare_data(self) -> None:
        raise NotImplementedError

    # def build_item(self) -> None:
    #     raise NotImplementedError


class CmdbItemBuilder(Builder):
    def prepare_data(self) -> None:
        pass

    def build_item(self) -> None:
        pass


class EnvironmentsUserFile(Builder):
    def reset(self):
        pass

    def prepare_data(self):
        pass

    def get_result(self):
        pass


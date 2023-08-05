from .AbsGenerator import AbstractGenerator


class V2Generator(AbstractGenerator):
    # TODO
    def __init__(self):
        AbstractGenerator.__init__(self)
        raise self.OpenApiVersionError("Generator for version 2 doesn't implemented yet")

    # ********************************** MAIN FUNCTION THAT HANDLE ALL OPERATION      ****************************** #

    def deploy_schema(self, path: str) -> dict:
        # TODO
        pass

    def build_mapped_schema(self, path: str) -> dict:
        # TODO
        pass


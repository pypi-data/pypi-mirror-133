import abc


class AbstractGenerator(object):
    class OpenApiVersionError(Exception):
        def __init__(self, *args):
            Exception.__init__(self, *args)

    _sections_keys = ['paths', 'webhooks']
    _methods = ['get', 'post', 'put', 'delete']

    @abc.abstractmethod
    def deploy_schema(self, path):
        pass

    @abc.abstractmethod
    def build_mapped_schema(self, path):
        pass

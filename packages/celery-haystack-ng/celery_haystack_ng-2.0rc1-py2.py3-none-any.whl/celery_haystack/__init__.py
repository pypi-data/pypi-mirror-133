__version__ = '2.0rc1'


def version_hook(config):
    config['metadata']['version'] = __version__

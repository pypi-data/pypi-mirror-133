VERSION = (0, 6, 3)
__version__ = '.'.join(str(v) for v in VERSION)


def setup(app):
    from . import theme
    theme.setup(app)

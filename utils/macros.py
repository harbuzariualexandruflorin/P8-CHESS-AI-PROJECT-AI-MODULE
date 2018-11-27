class MetaConst(type):
    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        raise TypeError


class Const(object, metaclass=MetaConst):
    __metaclass__ = MetaConst

    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        raise TypeError


class Macros(Const):
    SERVER_PORT: str = '5002'
    BOARD_WIN_VALUE: float = 1
    BOARD_STALEMATE_VALUE: float = 0.80

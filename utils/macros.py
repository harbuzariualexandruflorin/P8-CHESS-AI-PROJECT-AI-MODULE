import chess


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

    BOARD_CHECKMATE_VALUE: float          = 1.0
    BOARD_POSSIBLE_CHECKMATE_VALUE: float = 0.9
    BOARD_STALEMATE_VALUE: float          = -0.80
    BOARD_CHECK_VALUE: float              = 0.1
    BOARD_INTERVAL_FIX                    = 55

    PIECE_VALUES = {
        chess.PAWN:   1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK:   5,
        chess.QUEEN:  9,
        chess.KING:   0
    }

    UCI_TO_SQUARE = dict(zip(chess.SQUARE_NAMES, chess.SQUARES))

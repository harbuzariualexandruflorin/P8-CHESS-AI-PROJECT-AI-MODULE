
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

    BOARD_CHECKMATE_VALUE: float = 1
    BOARD_POSSIBLE_CHECKMATE_VALUE: float = 0.9
    BOARD_STALEMATE_VALUE: float = -0.80
    BOARD_CHECK_VALUE: float = 0.1

    BOARD_PIECE_TAKE_VALUE: float = 0.02
    BOARD_INTERVAL_FIX = 20
    PIECE_VALUES = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }

    PAWN_ADVANCE_VALUES = {
        2: 1,
        3: 1,
        4: 1,
        5: 1.5,
        6: 3,
        7: 5
    }

    UCI_TO_SQUARE = dict(zip(chess.SQUARE_NAMES, chess.SQUARES))
    BOARD_SIZE: int = 8


from Constants import WHITE, BLACK, WALL


def get_opponent(color):
    if color == WHITE:
        return BLACK
    elif color == BLACK:
        return WHITE
    else:
        return WALL
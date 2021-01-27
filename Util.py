from Constants import WHITE, BLACK, WALL


def get_opponent(color):
    if color == WHITE:
        return BLACK
    elif color == BLACK:
        return WHITE
    else:
        return WALL


def get_flatten(unflatten_point, l):
    a = unflatten_point[0] * l*l
    b = a + unflatten_point[1] * l
    ret = b + unflatten_point[2]
    return ret


def get_unflatten(flatten_point, l):
    z = flatten_point // (l*l)
    mod = flatten_point % (l*l)
    y = mod // l
    mod = mod % l
    x = mod
    return [z, y, x]
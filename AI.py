def ai_make_move():
    pass


def ai_unmake_move():
    pass


def prune_func():
    pass


def search(depth, alpha, beta):
    if depth == 0:
        return eval()

    moves = []  # get all possible moves

    if len(moves) == 0:
        return 0

    for move in moves:
        ai_make_move()
        search_val = -search(depth - 1, -beta, -alpha);
        ai_unmake_move()

        # prune alpha, beta

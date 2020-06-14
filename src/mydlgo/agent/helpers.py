from dlgo.gotypes import Point


def is_point_an_eye(board, point, color):
    if board.get(point) is not None:  # 空の点でなければ眼ではない
        return False

    for neighbor in point.neighbors():  # 隣接する全ての点が味方ではない場合、眼ではない
        if board.is_on_grid(neighbor):
            neighbor_color = board.get(neighbor)
            if neighbor_color != color:
                return False

    friendly_corners = 0
    off_board_corners = 0
    corners = [
        Point(point.row - 1, point.col - 1),  # 左上
        Point(point.row - 1, point.col + 1),  # 右上
        Point(point.row + 1, point.col - 1),  # 左下
        Point(point.row + 1, point.col + 1),  # 右下
    ]

    for corner in corners:
        if board.is_on_grid(corner):
            corner_color = board.get(corner)
            if corner_color == color:
                friendly_corners += 1
        else:
            off_board_corners += 1

    if off_board_corners > 0:
        return off_board_corners + friendly_corners == 4  # 点が辺または隅にある場合、4つの角を占めている必要がある
    return friendly_corners >= 3  # 点が中央にある場合、3つ以上の角を占めている必要がある

def isValid(board, pos, e):
    i, j = pos
    rowOk = all([e != board[i][x] for x in range(9)])
    if rowOk:
        columnOk = all([e != board[x][j] for x in range(9)])
        if columnOk:
            secTopX, secTopY = 3 * (i // 3), 3 * (j // 3)
            for x in range(secTopX, secTopX + 3):
                for y in range(secTopY, secTopY + 3):
                    if board[x][y] == e:
                        return False
            return True
    return False


def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)

    return None


def solve(board):
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find
    for i in range(1, 10):
        if isValid(board, (row, col), i):
            board[row][col] = i

            if solve(board):
                return True

            board[row][col] = 0
    return False
def printsudoku(board):
    for i in range(len(board)):
        line = ""
        if i == 3 or i == 6:
            print("---------------------")
        for j in range(len(board[i])):
            if j == 3 or j == 6:
                line += "| "
            line += str(board[i][j]) + " "
        print(line)

board = [
    [0, 9, 0, 0, 0, 0, 8, 0, 1], 
    [1, 8, 0, 0, 2, 0, 0, 0, 0], 
    [3, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 5, 3, 0, 0, 0, 4], 
    [0, 7, 0, 0, 0, 0, 0, 0, 0], 
    [5, 6, 8, 4, 0, 9, 0, 0, 0], 
    [0, 0, 0, 6, 0, 0, 9, 0, 5], 
    [8, 0, 6, 9, 0, 0, 4, 0, 0], 
    [0, 1, 0, 0, 5, 0, 0, 0, 0]
]
solve(board)

printsudoku(board)

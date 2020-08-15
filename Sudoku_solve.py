try:
    import sys
    from PyQt5.QtTest import QTest
    from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QMessageBox
    from random import randint
    import requests
except ImportError:
    print("Import error, pls run `pip install -r requirements.txt` to install module.")
from theme import Ui_Form


def valid(board, pos, num):
    # Check row
    for i in range(0, len(board)):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # Check Col
    for i in range(0, len(board)):
        if board[i][pos[1]] == num and pos[1] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False

    return True


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


def get_new_problem(lever=0):
    """
    - Get problem from api of sudoku.com
    :param lever:
    :return: board and result
    """
    if lever == 0:
        lever = "easy"
    elif lever == 1:
        lever = "medium"
    elif lever == 2:
        lever = "hard"
    elif lever == 3:
        lever = "expert"
    else:
        return None

    def bind(text):
        bo = []
        while text:
            line = list(text[:9])
            bo.append(list(map(int, line)))
            text = text[9:]
        return bo

    api = f"https://sudoku.com/api/getLevel/{lever}"
    session = requests.Session()

    response = session.get(url=api, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.170 Safari/537.36',
    })
    data = response.json()
    if not data:
        return None
    info = data.get('desc')
    if info:
        result = info[0]
        ans = info[1]
        return bind(result), bind(ans)


def gen_problem():
    board = [[0] * 9 for _ in range(9)]

    for _ in range(30):
        i = randint(0, 8)
        j = randint(0, 8)
        while board[i][j] != 0:
            i = randint(0, 8)
            j = randint(0, 8)
        num = randint(1, 9)
        while valid(board, (i, j), num) == False:
            num = randint(1, 9)
        board[i][j] = num
    return board


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


class GUI(QMainWindow, Ui_Form):
    def __init__(self):
        super(GUI, self).__init__()
        self.setupUi(self)
        self.init_ui()
        self.btn_solve.clicked.connect(self.solve)
        self.btn_random_problem.clicked.connect(self.ramdom_problem)
        self.show()

    def init_ui(self):
        self.board = [
            [0, 6, 0, 5, 0, 1, 8, 0, 0],
            [4, 7, 3, 0, 0, 2, 0, 0, 5],
            [5, 0, 1, 0, 0, 0, 0, 2, 4],
            [8, 1, 0, 6, 0, 0, 0, 0, 0],
            [0, 9, 0, 0, 0, 0, 0, 3, 0],
            [3, 5, 7, 0, 2, 0, 6, 0, 1],
            [0, 0, 5, 2, 0, 7, 4, 8, 0],
            [9, 4, 6, 1, 0, 0, 7, 5, 0],
            [0, 0, 8, 9, 0, 0, 0, 1, 0],
        ]
        self.init_display()

    def ramdom_problem(self):
        problem = get_new_problem(lever=0)
        if problem:
            self.board, self.ans = problem
        self.init_display()

    def init_display(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                child = self.findChild(QTextEdit, f"txt_{i}_{j}")
                if self.board[i][j] != 0:
                    child.setText(str(f"  {self.board[i][j]}"))
                    child.setEnabled(False)
                else:
                    child.setText(str(""))
                    child.setReadOnly(True)
                    child.setEnabled(True)
                child.setStyleSheet(r'''QTextEdit {border: 1px solid #76797C; color: dark;}''')

    def solve(self):
        self.btn_solve.setEnabled(False)
        self.btn_random_problem.setEnabled(False)
        print("\nProblem: ")
        printsudoku(self.board)
        status = self.run_solve()
        if not status:
            QMessageBox.information(self, "Status", "This problem can't solve !", QMessageBox.Yes)
        else:
            print("\nSolved: ")
            printsudoku(self.board)
        self.btn_solve.setEnabled(True)
        self.btn_random_problem.setEnabled(True)

    def closeEvent(self, event):
        # reply = QMessageBox.question(self, "Window Close", "Are you sure want to close ?",
        #                              QMessageBox.Yes | QMessageBox.No)
        # if reply == QMessageBox.Yes:
        #     event.accept()
        #     sys.exit()
        # else:
        #     event.ignore()
        sys.exit()

    def run_solve(self):
        find = find_empty(self.board)
        if not find:
            return True
        else:
            row, col = find
        for i in range(1, 10):
            if valid(self.board, (row, col), i):
                self.board[row][col] = i
                child = self.findChild(QTextEdit, f"txt_{row}_{col}")
                child.setText(str(f"  {i}"))
                child.setStyleSheet(r'''QTextEdit { border: 2px solid #008000  }''')
                QTest.qWait(100)

                if self.run_solve():
                    return True

                self.board[row][col] = 0
                child = self.findChild(QTextEdit, f"txt_{row}_{col}")
                child.setText(str(f"  {0}"))
                child.setStyleSheet(r'''QTextEdit { border: 2px solid #FF0000  }''')
                QTest.qWait(100)
        return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    _ = GUI()
    sys.exit(app.exec_())

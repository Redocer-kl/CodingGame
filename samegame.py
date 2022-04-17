import heapq
import sys
import time
from typing import Optional

class State:
    def __init__(self, columns: 'list[list[int]]', score: int = 0):
        self.columns = columns
        self.score = score

    def moves(self) -> 'list[list[tuple[int, int]]]':
        visited = set()
        move = []
        for i in range(15):
            for j in range(15):
                if (i, j) not in visited:
                    if self.columns[i][j] != -1:
                        ans = self.dfs(i, j, [])
                        if len(ans) >= 2:
                            move.append(ans)
                        for pair in ans:
                            visited.add(pair)
        return move

    def sosed(self, x: int, y: int):
        color = self.columns[x][y]
        ans = [[x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]]
        final = []
        for i in ans:
            if (0 <= i[0] < 15) and (0 <= i[1] < 15):
                if color == self.columns[i[0]][i[1]]:
                    final.append(i)
        return final

    def dfs(self, x: int, y: int, move: 'list[tuple[int, int]]'):
        if (x,y) in move:
            return move
        move.append((x, y))
        for i in self.sosed(x, y):
            x1, y1 = i[0], i[1]
            if (x1, y1) not in move:
                move = self.dfs(x1, y1, move)
        return move

    def apply_move(self, move: 'list[tuple[int, int]]') -> 'State':
        ans = [[-1 for i in range(15)] for i in range(15)]
        exx = 0
        for x in range(15):
            exy = 0
            stolb = [-1] * 15
            for y in range(15):
                if (x, y) not in move:
                    stolb[y - exy] = self.columns[x][y]
                else:
                    exy += 1
            if stolb.count(-1) == 15:
                exx += 1
            else:
                for i in range(15):
                    ans[x - exx][i] = stolb[i]
        res = State(ans, self.score + (len(move) - 2) ** 2)
        return res

def greedy_ai(state: State, estimate_state) -> 'Optional[list[tuple[int, int]]]':
    moves = state.moves()
    if len(moves) == 0:
        return None
    best_move = []
    best_score = -10
    for i in moves:
        new_state = state.apply_move(i)
        score = estimate(new_state)
        if score >= best_score:
            best_score = score
            best_move = i
    return best_move

def estimate(state: State) -> float:
    moves = state.moves()
    if len(moves) == 0:
        return state.score
    best_num = -10
    for i in moves:
        new_state = state.apply_move(i)
        num = get_score(new_state)
        if num > best_num:
            best_num = num
    return best_num


def get_score(state:State):
    s = state.score
    move = state.moves()
    for i in move:
        s += (len(i) - 2)**2
    return s

class Node:
    def __init__(self, score: float, state: State, parent_node: Optional['Node'],
                 move: Optional['list[tuple[int, int]]']):
        self.score = score
        self.state = state
        self.parent_node = parent_node
        self.move = move

    def __lt__(self, other):
        return self.score > other.score

def get_next_nodes(node: Node, estimate_state):
    pass

def chokudai_search(state: State, estimate_state) -> Node:
    pass

def chokudai_solve(state: State) -> 'list[list[tuple[int, int]]]':
    pass

def solve(state: State) -> 'list[list[tuple[int, int]]]':
    solution = []
    t1 = time.time()
    while time.time() - t1 < 19.8:
        move = greedy_ai(state, estimate)
        if move is None:
            break
        solution.append(move)
        state = state.apply_move(move)
    return solution

def read_state_from(lines: 'list[str]') -> State:
    rows = []
    for line in lines:
        row = []
        for color in line.split():
            row.append(-1 if color == '.' else int(color))
        rows.append(row)

    cols = [[row[x] for row in reversed(rows) if row[x] != -1] for x in range(len(rows[0]))]
    return State(cols)

def read_state() -> State:
    lines = [input() for _ in range(15)]
    return read_state_from(lines)

def main():
    state = read_state()
    moves = solve(state)
    # moves = chokudai_solve(state)
    for move in moves:
        x, y = move[0]
        print(x, y)
        read_state()

if __name__ == '__main__':
    main()

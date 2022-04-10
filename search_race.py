import random
import sys
import math
import time


def norm_angle(a):
    a = a % 360  # 0..360
    if a > 180:
        a -= 360  # -180..180
    return a


class Move:
    def __init__(self, x, y, thrust, message=""):
        self.x, self.y, self.thrust, self.message = x, y, thrust, message

    def __str__(self):
        return f'{self.x} {self.y} {self.thrust} {self.message}'


class State:
    def __init__(self, checkpoints, checkpoint_index, x, y, vx, vy, angle):
        self.checkpoints = checkpoints
        self.checkpoint_index = checkpoint_index
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.angle = angle


    def __str__(self):
        return f'State(checkpoints, {self.checkpoint_index}, {self.x}, {self.y}, {self.vx}, {self.vy}, {self.angle})'


    def copy(self):
        return State(self.checkpoints, self.checkpoint_index, self.x, self.y, self.vx, self.vy, self.angle)


    def next_checkpoint(self):
        return self.checkpoints[self.checkpoint_index % len(self.checkpoints)]


    def simulate(self, move: Move):
        desired_angle = 180 * math.atan2(move.y - self.y, move.x - self.x) / math.pi
        da = norm_angle(desired_angle - self.angle)
        da = max(-18, min(18, da))
        self.angle = self.angle + da
        self.vx += move.thrust * math.cos(self.angle * math.pi / 180)
        self.vy += move.thrust * math.sin(self.angle * math.pi / 180)
        self.x = int(self.x + self.vx)
        self.y = int(self.y + self.vy)
        self.vx = int(0.85 * self.vx)
        self.vy = int(0.85 * self.vy)
        self.angle = round(self.angle) % 360
        xc, yc = self.next_checkpoint()
        dx, dy = self.x - xc, self.y - yc
        if dx * dx + dy * dy <= 600 * 600:
            self.checkpoint_index += 1


def estimate(state):
    nx, ny = state.next_checkpoint()
    x, y = state.x, state.y
    dx = abs(nx - x)
    dy = abs(ny - y)
    return state.checkpoint_index * 20000 - (dx ** 2 + dy ** 2) ** 0.5


def create_random_moves(depth):
    ans = []
    for i in range(depth):
        ans.append(Move(random.randint(0, 16000), random.randint(0, 9000), random.randint(0, 200)))
    return ans

def random_search(state, depth):
    best_moves = []
    best_score = -math.inf
    simulations_count = 0
    t1 = time.time() * 1000
    moves_score = []
    while (time.time() * 1000) - t1 < 40:
        ans = create_random_moves(depth)
        score = 0
        mid_state = state.copy()
        for i in ans:
            mid_state.simulate(i)
        score = estimate(mid_state)
        if best_score < score:
            best_score = score
            best_moves = ans
    return(best_moves)

def read_checkpoints():
    n = int(input())
    checkpoints = []
    for i in range(n):
        x, y = [int(j) for j in input().split()]
        checkpoints.append((x, y))
    return checkpoints


def main():
    checkpoints = read_checkpoints()
    print(f'checkpoints={checkpoints}', file=sys.stderr)
    predicted_state = None
    best_moves = None
    while True:
        state = State(checkpoints, *list(map(int, input().split())))
        if predicted_state:
            print(predicted_state, file=sys.stderr)
            # Проверка, что наша симуляция работает точно так же как и официальная.
            # Если раскомментировать строку ниже, то решение начнет падать с ошибкой каждый раз, 
            # когда наша симуляция ошиблась, предсказывая к чему приведет наш предыдущий ход
            # assert str(predicted_state) == str(state)

        best_moves = random_search(state, depth=5)  # подходящую глубину нужно подобрать!
        best_move = best_moves[0]
        print(str(best_move))
        state.simulate(best_move)
        predicted_state = state


if __name__ == '__main__':
    main()

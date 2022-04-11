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

    def next(self):
        return self.checkpoints[(self.checkpoint_index + 1) % len(self.checkpoints)]


    def ai(self):
        dy = self.next_checkpoint()[1] - self.y
        dx = self.next_checkpoint()[0] - self.x
        dy1 = self.next()[1] - self.y
        dx1 = self.next()[0] - self.x
        beta = ((math.atan2(dy, dx) * 180 / math.pi) - self.angle) % 360
        beta1 = ((math.atan2(dy1, dx1) * 180 / math.pi) - self.angle) % 360
        if beta > 180:
            beta -= 360
        if beta1 > 180:
            beta1 -= 360
        if math.sqrt(self.vx * self.vx + self.vy * self.vy) > math.sqrt(dx*dx + dy*dy) * 0.1667:
            if abs(beta1 - beta) < 10:
                return Move(self.next()[0], self.next()[1], 200, "Gas")
            return Move(self.next()[0], self.next()[1], 0, "Turn")
        if abs(beta) > 4:
            return Move(self.next_checkpoint()[0], self.next_checkpoint()[1], 0, "Turn")
        return Move(self.next_checkpoint()[0], self.next_checkpoint()[1], 200, "Gas")


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
        ans.append(Move(random.randint(0, 16000), random.randint(0, 9000), max(0, min(200, random.randint(-50, 250)))))
    return ans



def random_search(state, pr_moves, depth):
    best_moves = []
    if pr_moves != None:
        pr_moves.pop(0)
        pr_moves += create_random_moves(1)
        mid_state = state.copy()
        for i in pr_moves:
            mid_state.simulate(i)
        best_score = estimate(mid_state)
        best_moves = pr_moves
    else:
        best_score = -math.inf
    t1 = time.time() * 1000
    while (time.time() * 1000) - t1 < 40:
        ans = create_random_moves(depth)
        mid_state = state.copy()
        for i in ans:
            mid_state.simulate(i)
        score = estimate(mid_state)
        if best_score < score:
            best_score = score
            best_moves = ans
    mid_state = state.copy()
    for i in range(depth):
        mid_state.simulate(mid_state.ai())
    score = estimate(mid_state)
    if best_score < score:
        best_score = score
        best_moves = [state.ai()]
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
    best_moves = None
    while True:
        state = State(checkpoints, *list(map(int, input().split())))
        best_moves = random_search(state, best_moves, depth=5) 
        best_move = best_moves[0]
        print(str(best_move))
        state.simulate(best_move)


if __name__ == '__main__':
    main()

import copy

FIRST_TYPE = 1
SECOND_TYPE = 2

class State:
    def __init__(self, _snake, _seed, _profit):
        self.snake = _snake
        self.seed = _seed
        self.profit = _profit
        self.path = ''
        self.F = 0

    def __lt__(self, other):
        return self.F < other.F

    def __eq__(self, other):
        if other != None:
            return self.F == other.F
        return False

    def move(self, dest, profit):
        head = self.snake[0]
        if dest not in self.snake:
            if str([dest[0], dest[1], FIRST_TYPE]) in self.seed and len(self.seed) == 1:
                self.seed.remove(str([dest[0], dest[1], FIRST_TYPE]))
                self.profit += 1
                return True
            if str([head[0], head[1], FIRST_TYPE]) in self.seed:
                self.seed.remove(str([head[0], head[1], FIRST_TYPE]))
                self.profit += 1
                self.snake.insert(0, dest)
            elif str([head[0], head[1], SECOND_TYPE]) in self.seed:
                self.seed.remove(str([head[0], head[1], SECOND_TYPE]))
                self.seed.add(str([head[0], head[1], FIRST_TYPE]))
                self.profit += 1
                self.snake.insert(0, dest)
            else:
                self.snake.insert(0, dest)
                self.snake.pop()
            return True
        if len(self.snake) > 2 and dest == self.snake[len(self.snake) - 1]:
            self.snake.insert(0, dest)
            self.snake.pop()
            return True     
        return False

    def up(self):
        rv = State(copy.deepcopy(self.snake), copy.deepcopy(self.seed), self.profit)
        head = rv.snake[0]
        dest = (0 if head[0] + 1 == H else head[0] + 1, head[1])
        if rv.move(dest, self.profit) == False:
            return None
        rv.path = self.path + 'U'
        return rv
        
    def down(self):
        rv = State(copy.deepcopy(self.snake), copy.deepcopy(self.seed), self.profit)
        head = rv.snake[0]
        dest = (H - 1 if head[0] == 0 else head[0] - 1, head[1])
        if rv.move(dest, self.profit) == False:
            return None
        rv.path = self.path + 'D'
        return rv
    
    def left(self):
        rv = State(copy.deepcopy(self.snake), copy.deepcopy(self.seed), self.profit)
        head = rv.snake[0]
        dest = (head[0], head[1] - 1 if head[1] > 0 else W - 1)
        if rv.move(dest, self.profit) == False:
            return None
        rv.path = self.path + 'L'
        return rv
    
    def right(self):
        rv = State(copy.deepcopy(self.snake), copy.deepcopy(self.seed), self.profit)
        head = rv.snake[0]
        dest = (head[0], head[1] + 1 if head[1] + 1 < W else 0)
        if rv.move(dest, self.profit) == False:
            return None
        rv.path = self.path + 'R'
        return rv

def get_input(path):
    global H, W
    file = open(path)
    H, W = map(int, file.readline().split(','))
    seed = set()
    xs, ys = map(int, file.readline().split(','))
    number_of_seeds = int(file.readline())
    i = 0
    goal = 0
    while i < number_of_seeds:
        y, x, typ = map(int, file.readline().split(','))
        if typ == 1:
            seed.add(str([y, x, FIRST_TYPE]))
            goal += 1
        else:
            seed.add(str([y, x, SECOND_TYPE]))
            goal += 2
        i = i + 1
    file.close()
    return State([(ys, xs)], seed, 0), goal
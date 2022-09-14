import copy
import time
import sys
import MyUtility as mu

sys.setrecursionlimit(1000000000)

explored = set()

number_of_states = 0
number_of_not_repeated_states = 0

def DFS(root, goal, depth):
    global number_of_states
    global number_of_not_repeated_states
    number_of_states += 1
    if (str(root.snake), root.profit, len(root.path)) not in explored:
        number_of_not_repeated_states += 1
        explored.add((str(root.snake), root.profit, len(root.path)))
        if root.profit == goal: return root
        if depth <= 0: return None
        moves = []
        u = root.up()
        if u != None: moves.append(u)
        d = root.down()
        if d != None: moves.append(d)
        r = root.right()
        if r != None: moves.append(r)
        l = root.left()
        if l != None: moves.append(l)

        for i in moves:
            res = DFS(i, goal, depth - 1)
            if res != None:
                return res
    return None  

def IDS(initial_state, goal):
    depth = 1
    while True:
        explored.clear()
        rv = DFS(initial_state, goal, depth)
        if rv != None: return rv
        depth = depth + 1

if __name__ == "__main__":
    s, goal = mu.get_input(sys.argv[1])

    tic = time.time()
    goal_state = IDS(s, goal)
    toc = time.time()

    # print 'goal_state.snake' for snake position.
    print("Length:", len(goal_state.path))
    print("Path:", goal_state.path)
    print("Number of states:", number_of_states)
    print("Number of not reapeted states:", number_of_not_repeated_states)
    print("Time: %f ms" % ((toc - tic) * 1000))
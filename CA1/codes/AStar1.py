import copy
import time
import sys
import bisect
import MyUtility as mu

sys.setrecursionlimit(1000000000)

explored = set()

number_of_states = 0
number_of_not_repeated_states = 0

def AStar(root, goal):
    global number_of_not_repeated_states, number_of_states
    frontier = []
    frontier.append(root)
    while frontier != []:
        number_of_states += 1
        n = frontier.pop(0)
        if (str(n.snake), n.profit) not in explored:
            number_of_not_repeated_states += 1
            explored.add((str(n.snake), n.profit))
            if n.profit == goal: return n
            moves = []
            u = n.up()
            if u != None: moves.append(u)
            d = n.down()
            if d != None: moves.append(d)
            r = n.right()
            if r != None: moves.append(r)
            l = n.left()
            if l != None: moves.append(l)
            
            for i in moves:
                i.F = (goal - i.profit) + len(i.path)
                bisect.insort(frontier, i)
    return None

if __name__ == "__main__":
    s, goal = mu.get_input(sys.argv[1])

    tic = time.time()
    goal_state = AStar(s, goal)
    toc = time.time()

    # print 'goal_state.snake' for snake position.
    print("Path Length:", len(goal_state.path))
    print("Path:", goal_state.path)
    print("Number of states:", number_of_states)
    print("Number of not reapeted states:", number_of_not_repeated_states)
    print("Time: %f ms" % ((toc - tic) * 1000))
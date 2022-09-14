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
                head = i.snake[0]
                for j in i.seed:
                    j = list(map(int, j[1:len(j) - 1].split(',')))
                    dr = abs(head[0] - j[0]) + abs(head[1] - j[1])

                    dx = j[1] + (W - head[1])
                    if head[1] < j[1]: dx = (W - j[1]) + head[1]

                    dy = j[0] + (H - head[0]) 
                    if head[0] < j[0]: dy = (H - j[0]) + head[0]

                    if dr > dx + dy:
                        dr = dx + dy
                    
                    if i.F < dr:
                        i.F = dr
                
                i.F += len(i.path)
                bisect.insort(frontier, i)
    return None

if __name__ == "__main__":
    s, goal = mu.get_input(sys.argv[1])

    global H, W
    file = open(sys.argv[1])
    H, W = map(int, file.readline().split(','))
    file.close()

    tic = time.time()
    goal_state = AStar(s, goal)
    toc = time.time()

    # print 'goal_state.snake' for snake position.
    print("Path Length:", len(goal_state.path))
    print("Path:", goal_state.path)
    print("Number of states:", number_of_states)
    print("Number of not reapeted states:", number_of_not_repeated_states)
    print("Time: %f ms" % ((toc - tic) * 1000))
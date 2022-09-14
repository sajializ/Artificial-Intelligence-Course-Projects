import copy
import time
import sys
import MyUtility as mu

number_of_states = 0
number_of_not_repeated_states = 0

def BFS(initial_state, goal):
    global number_of_states
    global number_of_not_repeated_states
    frontier = []
    explored = set()
    frontier.append(initial_state)
    while frontier != []:
        number_of_states += 1
        current = frontier.pop(0)
        if (str(current.snake), current.profit) not in explored:
            number_of_not_repeated_states += 1
            u = current.up()
            if u != None:
                frontier.append(u)
                if u.profit == goal: return u

            d = current.down()
            if d != None:
                frontier.append(d)
                if d.profit == goal: return d

            l = current.left()
            if l != None:
                frontier.append(l)
                if l.profit == goal: return l

            r = current.right()
            if r != None:
                frontier.append(r)
                if r.profit == goal: return r

            explored.add((str(current.snake), current.profit))

    # If search failed:
    return None

if __name__ == "__main__":
    s, goal = mu.get_input(sys.argv[1])

    tic = time.time()
    goal_state = BFS(s, goal)
    toc = time.time()

    # print 'goal_state.snake' for snake position.
    print("Length:", len(goal_state.path))
    print("Path:", goal_state.path)
    print("Number of states:", number_of_states)
    print("Number of not reapeted states:", number_of_not_repeated_states)
    print("Time: %f ms" % ((toc - tic) * 1000))
from collections import deque

def is_valid(state):
    missionaries, cannibals, boat = state
    if missionaries < 0 or cannibals < 0 or missionaries > 3 or cannibals > 3:
        return False
    if missionaries > 0 and missionaries < 3 and missionaries < cannibals:
        return False
    return True

def get_successors(state):
    successors = []
    missionaries, cannibals, boat = state
    if boat == 1:
        moves = [(2, 0), (0, 2), (1, 1), (1, 0), (0, 1)]
        for move in moves:
            new_state = (missionaries - move[0], cannibals - move[1], 0)
            if is_valid(new_state):
                successors.append(new_state)
    else:
        moves = [(2, 0), (0, 2), (1, 1), (1, 0), (0, 1)]
        for move in moves:
            new_state = (missionaries + move[0], cannibals + move[1], 1)
            if is_valid(new_state):
                successors.append(new_state)
    return successors

def dfs(start_state, goal_state):
    stack = deque()
    stack.append((start_state, []))
    visited = set()
    count = 0  
    while stack:
        (state, path) = stack.pop()
        if state in visited:
            continue
        visited.add(state)
        path = path + [state]
        count += 1  
        if state == goal_state:
            return path, count
        for successor in get_successors(state):
            stack.append((successor, path))
    return None, count

start_state = (3, 3, 1)
goal_state = (0, 0, 0)

solution, node_count = dfs(start_state, goal_state)
if solution:
    print("Solution found:")
    for step in solution:
        print(step)
    print(f"\nNumber of nodes in the path: {len(solution)}")
    print(f"Total number of nodes visited: {node_count}")
else:
    print("No solution found.")
    print(f"Total number of nodes visited: {node_count}")
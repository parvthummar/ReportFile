from collections import deque

# Define the initial and goal states.
# Rabbits are represented by their direction: 'E' for east-bound, 'W' for west-bound.
# Empty space is represented by '_'.
start_state = ('E', 'E', 'E', 'O', 'W', 'W', 'W')
goal_state = ('W', 'W', 'W', 'O', 'E', 'E', 'E')

# Function to check if a move is valid.
def is_valid(new_index, state):
    # Ensure no out-of-bounds issues
    return 0 <= new_index < len(state)

# Function to generate possible successors from the current state.
def get_successors(state):
    successors = []
    empty_index = state.index('O')

    # Possible moves: 1-step or 2-step
    move_options = [-1, 1, -2, 2]
    
    for move in move_options:
        new_index = empty_index + move
        if is_valid(new_index, state):
            new_state = list(state)
            new_state[empty_index], new_state[new_index] = new_state[new_index], new_state[empty_index]
            successors.append(tuple(new_state))
    
    return successors

def bfs(start_state, goal_state):
    queue = deque([(start_state, [])])
    visited = set()
    
    while queue:
        (state, path) = queue.popleft()
        if state in visited:
            continue
        visited.add(state)
        path = path + [state]
        
        if state == goal_state:
            return path
        
        for successor in get_successors(state):
            queue.append((successor, path))
    
    return None

# Find the solution from start to goal state.
solution = bfs(start_state, goal_state)
print("Total Number of operations:", len(solution) - 1 if solution else 0)
print()

if solution:
    print("Solution found:")
    for step in solution:
        print(step)
else:
    print("No solution found.")
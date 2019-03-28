import random

maze = []
w = 20
cols = rows = 20
direction = [[-1, 0], [0, 1], [1, 0], [0, -1]]
current = None
stack = []
cell_queue = []

class Cell():
    def __init__(self, i, j):
        self.i = i
        self.j = j
        # Top - Right - Bot - Left
        self.wall = [True, True, True, True]
        self.visited = False
        # BFS traversal
        self.BFS = False
        self.distance = 0
        
        
    def show(self):
        x = self.i*w + 10
        y = self.j*w + 10
        noStroke()
        if not self.visited:
            fill(51)
            rect(x, y, w, w)
        elif self.visited:
            fill(255)
            rect(x, y, w, w)
        if self.BFS:
            fill(255 - self.distance, 255 - self.distance, 240)
            rect(x, y, w, w)
        
        # Cells can carve through (x, y) - (x+w, y) - (x+w, y+w) - (x, y+w)
        stroke(0)
        if self.wall[0]:
            line(x, y, x+w, y)
        if self.wall[1]:
            line(x+w, y, x+w, y+w)
        if self.wall[2]:
            line(x+w, y+w, x, y+w)
        if self.wall[3]:
            line(x, y+w, x, y)
            
    def carve_wall(self):
        adjacent = []
        for d in range(4):
            u = self.i + direction[d][0]
            v = self.j + direction[d][1]
            if check_cell(u, v) and maze[u][v].visited == False:
                adjacent.append(maze[u][v])
        if len(adjacent) > 0:
                # Next cell
            return random.choice(adjacent)
        else:
            return None

def setup():
    size(420,420)
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(Cell(i, j))
        maze.append(row)
    global current    
    current = maze[0][0]
    
def draw():
    background(255)
    for i in range(rows):
        for j in range(cols):
            maze[i][j].show()
    # Start from (0,0)
    global current
    current.visited = True
    next = current.carve_wall()
    if next:
        next.visited = True
        stack.append(next)
        # Remove wall
        remove(current, next)
        current = next
    elif len(stack) > 0:
        current = stack.pop()
        
    # BFS traversal
    if len(stack) == 0:
        BFS(rows/2, cols/2)

        
def remove(cellA, cellB):
    if cellA.i - cellB.i == 1:
        # Carve top wall
        cellA.wall[3] = False
        cellB.wall[1] = False
    elif cellA.i - cellB.i == -1:
        # Carve bot wall
        cellA.wall[1] = False
        cellB.wall[3] = False
    elif cellA.j - cellB.j == -1:
        # Carve right wall
        cellA.wall[2] = False
        cellB.wall[0] = False
    else:
        # Carve left wall
        cellA.wall[0] = False
        cellB.wall[2] = False

def check_cell(u, v):
    if 0 <= u < rows and 0 <= v < cols:
        return True
    return False

def check_route(cellA, cellB):
    if cellA.i - cellB.i == 1 and cellA.wall[3] == False:
        return True
    elif cellA.i - cellB.i == -1 and cellA.wall[1] == False :
        return True
    elif cellA.j - cellB.j == -1 and cellA.wall[2] == False:
        return True
    elif cellA.j - cellB.j == 1 and cellA.wall[0] == False:
        return True
    return False

def BFS(u, v):
    global cell_queue
    cell_queue.append((u, v))
    maze[u][v].BFS = True
    
    while len(cell_queue) > 0:
        x, y = cell_queue[0]
        cell_queue = cell_queue[1:]
        for d in range(4):
            i = x + direction[d][0]
            j = y + direction[d][1]
            if check_cell(i, j) and not maze[i][j].BFS and check_route(maze[x][y], maze[i][j]):
                cell_queue.append((i, j))
                maze[i][j].BFS = True
                maze[i][j].distance = maze[x][y].distance + 1

import turtle

from node import Node

PART_OF_PATH = 'O'
TRIED = '.'
OBSTACLE = '+'
DEAD_END = '-'
VISITED = 'x'
CLEAR = ' '

COLOR_WALLS = "#99c2ff"
COLOR_VISITED = "#FFCCCC"
COLOR_FOUND = "#CCFFCC"

RUN_SPEED = 10;

ListQ = [] # Lista de coordenadas visitadas
ListT = [] # Lista de nodos
Route = [] # Lista de coordenadas de la mejor ruta (salida a inicio)
algorithmCost = [0]
maxDepth = [0]

ADDED_DEPTH = 50

Turtle = turtle.Turtle ();
depth_reached = False

class Maze:
    def __init__(self, maze_file_name):
        rows_in_maze = 0
        columns_in_maze = 0
        self.maze_list = []
        maze_file = open(maze_file_name,'r')
        #rows_in_maze = 0
        for line in maze_file:
            row_list = []
            col = 0
            for ch in line[: -1]:
                row_list.append(ch)
                if ch == 'S':
                    self.start_row = rows_in_maze
                    self.start_col = col
                col = col + 1
            rows_in_maze = rows_in_maze + 1
            self.maze_list.append(row_list)
            columns_in_maze = len(row_list)

        self.rows_in_maze = rows_in_maze
        self.columns_in_maze = columns_in_maze
        self.x_translate = - columns_in_maze / 2
        self.y_translate = rows_in_maze / 2
        self.t = Turtle
        self.t.shape('turtle')
        self.wn = turtle.Screen()
        self.wn.setworldcoordinates(- (columns_in_maze - 1) / 2 - .5,
                - (rows_in_maze - 1) / 2 - .5,
                (columns_in_maze - 1) / 2 + .5,
                (rows_in_maze - 1) / 2 + .5)


    def draw_maze(self):
        self.t.speed(0)
        for y in range(self.rows_in_maze):
            initial = -1
            for x in range(self.columns_in_maze):
                if self.maze_list[y][x] == OBSTACLE and initial == -1:
                    initial = x + self.x_translate
                if self.maze_list[y][x] != OBSTACLE and initial != -1:
                    self.draw_centered_box(initial, x + self.x_translate, - y + self.y_translate, COLOR_WALLS)
                    initial = -1;
            if initial != -1:
                self.draw_centered_box(initial, self.columns_in_maze + self.x_translate, - y + self.y_translate, COLOR_WALLS)

        self.t.color('black')
        self.t.fillcolor('green')
        self.t.speed(RUN_SPEED)


    def draw_centered_box(self, xi, xf, y, color):
        self.t.up()
        self.t.goto(xi - .5, y - .5)
        self.t.color(color)
        self.t.fillcolor(color)
        self.t.setheading(90)
        self.t.down()
        self.t.begin_fill()

        self.t.forward(1)
        self.t.right(90)

        self.t.forward(xf - xi)
        self.t.right(90)

        self.t.forward(1)
        self.t.right(90)

        self.t.forward(xf - xi)
        self.t.right(90)

        self.t.end_fill()

    def move_turtle(self, x, y):
        self.t.up()
        self.t.setheading(self.t.towards(x + self.x_translate, y + self.y_translate))
        self.t.goto(x + self.x_translate, - y + self.y_translate)


    def drop_bread_crumb(self, color):
        self.t.dot(10, color)


    def update_position(self, row, col, val=None):
        if val:
            self.maze_list[row][col] = val
        self.move_turtle(col, row)

        if val == PART_OF_PATH:
            color = '#ffad99'
        elif val == OBSTACLE:
            color = 'red'
        elif val == TRIED:
            color = 'black'
        elif val == DEAD_END:
            color = 'red'
        elif val == VISITED:
            color = 'gray'
        elif val == "exit":
            color = 'yellow'
        else:
            color = None

        if color:
            self.drop_bread_crumb(color)


    def is_exit(self, row, col):
        return (row == 0 or
            row == self.rows_in_maze - 1 or
            col == 0 or
            col == self.columns_in_maze - 1)


    def __getitem__(self, idx):
        return self.maze_list[idx]


## Recorre la mejor ruta desde inicio a fin

def BE_FREE(maze):
    print("Free at Last!")
    while Route:
        row = Route.pop()
        col = Route.pop()
        maze.update_position(row, col, PART_OF_PATH)

    print('algorithmCost: ' + str(algorithmCost[0]))
    while True:
        maze.t.right(90)

## Cuando encuentra la salida, retrocede al inicio guardando las coordenadas
## por las que va pasando

def best_route(maze, start_row, start_column, tree):
    #maze.update_position(start_row, start_column, PART_OF_PATH)
    print(tree.name)
    if tree.name == "start":
        Route.append(start_column)
        Route.append(start_row)
        BE_FREE(maze)
        return True
    Route.append(start_column)
    Route.append(start_row)
    tree = tree.prev()
    best_route(maze, tree.row, tree.col, tree)

def isClear(position, maze):
    if maze[position[0]][position[1]] == CLEAR:
        return True
    else:
        return False

def moveLeft(maze, position):
    newPos = (position[0], position[1] - 1);
    return newPos

def moveRight(maze, position):
    newPos = (position[0], position[1] + 1);
    return newPos

def moveUp(maze, position):
    newPos = (position[0] - 1, position[1]);
    return newPos

def moveDown(maze, position):
    newPos = (position[0] + 1, position[1]);
    return newPos

def newNode (node, name, row, col):
    new_node = node.add()
    new_node.name = name
    new_node.row = row
    new_node.col = col
    ListT.append(new_node)
    return new_node

##################################################################################################################################################
def search_depthFirst (startPos, currentDepth, maxDepth, maze, exitFound, node):
    global depth_reached
    algorithmCost[0] += 1

    maze.update_position(startPos[0], startPos[1], VISITED)

    if maze.is_exit(startPos[0], startPos[1]):
        best_route(maze, startPos[0], startPos[1], node);
        return True
    elif currentDepth >= maxDepth:
        print ("Going back...");
        depth_reached = True;
        return False

    #Check each child in the node, using depth-first
    maze.t.setheading(maze.t.towards(-1000, 0))
    if not exitFound:
        #LEFT
        algorithmCost[0] += 1
        if(isClear(moveLeft(maze, startPos), maze)):
            node = newNode(node, "Left", startPos[0], startPos[1] - 1)
            exitFound = search_depthFirst(moveLeft(maze, startPos), currentDepth + 1, maxDepth, maze, exitFound, node)
            node = node.prev()

    maze.update_position(startPos[0], startPos[1], VISITED)
    maze.t.setheading(maze.t.towards(1000, 0))
    if not exitFound:
        #RIGHT
        algorithmCost[0] += 1
        if(isClear(moveRight(maze, startPos), maze)):
            node =  newNode(node, "Right", startPos[0], startPos[1] + 1)
            exitFound = search_depthFirst(moveRight(maze, startPos), currentDepth + 1, maxDepth, maze, exitFound, node)
            node = node.prev()

    maze.update_position(startPos[0], startPos[1], VISITED)
    maze.t.setheading(maze.t.towards(0, 1000))
    if not exitFound:
        #UP
        algorithmCost[0] += 1
        if(isClear(moveUp(maze, startPos), maze)):
            node =  newNode(node, "Up", startPos[0] - 1, startPos[1])
            exitFound = search_depthFirst(moveUp(maze,startPos), currentDepth + 1, maxDepth, maze, exitFound, node)
            node = node.prev()

    maze.update_position(startPos[0], startPos[1], VISITED)
    maze.t.setheading(maze.t.towards(0, -1000))
    if not exitFound:
        #DOWN
        algorithmCost[0] += 1
        if(isClear(moveDown(maze, startPos), maze)):
            node = newNode(node, "Down", startPos[0] + 1, startPos[1])
            exitFound = search_depthFirst(moveDown(maze, startPos), currentDepth + 1, maxDepth, maze, exitFound, node)
            node = node.prev()

    maze.update_position(startPos[0], startPos[1], VISITED)
    if exitFound:
        return True


    return False # If program reaches this point, this depth limit does not lead to the exit

def initialSetup(shouldDraw):
    print('shouldDraw: ' + str(shouldDraw))

    # Maze Creation
    my_maze = Maze('maze2.txt')

    if shouldDraw:
        my_maze.draw_maze()

    my_maze.update_position(my_maze.start_row, my_maze.start_col)

    # Tree Creation
    tree=Node()  #create a node
    tree.name="start" #name it root
    tree.row = my_maze.start_row
    tree.col = my_maze.start_col
    print(tree.name)

    return tree, my_maze

def solve_breathFirst():
    tree, my_maze = initialSetup(True)

    ListQ.append(tree.row)
    ListQ.append(tree.col)
    ListT.append(tree)
    my_maze.update_position(tree.row, tree.col, PART_OF_PATH)

    search_from_breathFirst(my_maze, ListQ[0], ListQ[1], tree)

def solve_depthFirst(shouldIncrementMaxDepth, shouldDraw):
    tree, my_maze = initialSetup(shouldDraw)

    startPos = (tree.row, tree.col); # Tuple for representing the coordinate

    my_maze.update_position(tree.row, tree.col, PART_OF_PATH)

    maxDepthValue = maxDepth[0]

    if shouldIncrementMaxDepth:
        maxDepthValue += ADDED_DEPTH
        maxDepth[0] = maxDepthValue

    exitFound = search_depthFirst (startPos, 0, maxDepthValue, my_maze, False, tree)

    if exitFound:
        BE_FREE(my_maze)
    else:
        print('Couldn\'t find the exit!')

    print('algorithmCost: ' + str(algorithmCost[0]))

    return exitFound

def main():
    global depth_reached
    # solve_breathFirst()
    result = solve_depthFirst(False, True)

    while not result:
        depth_reached = False
        result = solve_depthFirst(True, False)


if __name__ == '__main__':
    main()

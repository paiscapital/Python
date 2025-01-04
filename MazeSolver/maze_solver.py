# Coded By Meguminz : @paiscapital

class GridPosition:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	def __hash__(self):
		return hash((self.x, self.y))

class Node:
	def __init__(self, Pos: GridPosition, Step, HeuristicCost=0, Parent=None):
		self.Pos = Pos
		self.Step = Step
		self.HeuristicCost = HeuristicCost
		self.Total = Step + HeuristicCost

	def __it__(self, other):
		return self.Total < other.Total

class Deque:
	def __init__(self):
		self.data = list()

	def is_empty(self):
		return len(self.data) == 0

	def append(self, value):
		self.data.append(value)

	def popleft(self):
		if not self.is_empty():
			return self.data.pop(0)
		else:
			raise IndexError("popleft from empty deque")
	def pop(self):
		if not self.is_empty():
			return self.data.pop()
		else:
			raise IndexError("pop from empty deque")

	def priority(self, value):
		self.data.append(value)
		self.data.sort(key=lambda x: x.Total)

	# While loop safety (Truthy, Falsy)
	def __len__(self):
		return len(self.data)

	def __bool__(self):
		return len(self.data) > 0

def MazeBeautifier(maze):
	return "[\n" + "\n".join(["    [ " + " ".join(row) + " ]" for row in maze]) + "\n]"


def BFSAlgoSolver(Grid, Dest: GridPosition, Start: GridPosition):

	HorizontalMoveX = [-1, 0, 0, 1]
	VerticalMoveY = [0, -1, 1, 0]
	X, Y = (len(Grid), len(Grid))
	VisitedBlocks = [[0 for i in range(len(Grid[0]))] for j in range(len(Grid))]
	ParentBlocks = [[None for _ in range(Y)] for _ in range(X)]
	VisitedBlocks[Start.x][Start.y] = 1
	Queue = Deque()
	Sol = Node(Start,0)
	Queue.append(Sol)
	Steps = 0

	while Queue:
		CurrentBlock = Queue.popleft()
		CurrentPosition = CurrentBlock.Pos

		if CurrentPosition.x == Dest.x and CurrentPosition.y == Dest.y:
			print(f"BFSAlgo Visited Nodes: {Steps}\n\nFound the best posible pattern:")
			path = []
			node = CurrentBlock

			while node is not None:
				path.append(node.Pos)
				node = ParentBlocks[node.Pos.x][node.Pos.y]
			PathColorGrid = [[str(cell) for cell in row] for row in Grid]

			for position in path:
				PathColorGrid[position.x][position.y] = f"\033[91m{PathColorGrid[position.x][position.y]}\033[0m"

			print(MazeBeautifier(PathColorGrid))
			return CurrentBlock.Step

		if CurrentBlock not in VisitedBlocks:
			VisitedBlocks[CurrentPosition.x][CurrentPosition.y] = 1
			Steps += 1

		XPos = CurrentPosition.x
		YPos = CurrentPosition.y

		for i in range(4):
			if XPos == len(Grid)-1 and HorizontalMoveX[i] == 1:
				XPos = CurrentPosition.x
				YPos = CurrentPosition.y + VerticalMoveY[i]
			if YPos == 0 and VerticalMoveY[i] == -1:
				XPos = CurrentPosition.x + HorizontalMoveX[i]
				YPos = CurrentPosition.y
			else:
				XPos = CurrentPosition.x + HorizontalMoveX[i]
				YPos = CurrentPosition.y + VerticalMoveY[i]
			if XPos < 12 and YPos < 12 and XPos >= 0 and YPos >= 0:
				if Grid[XPos][YPos] == 1:
					if not VisitedBlocks[XPos][YPos]:
						NextStep = Node(GridPosition(XPos,YPos),CurrentBlock.Step + 1)
						ParentBlocks[XPos][YPos] = CurrentBlock
						VisitedBlocks[XPos][YPos] = 1
						Queue.append(NextStep)
	return -1

def DFSAlgoSolver(Grid, Dest: GridPosition, Start: GridPosition):
    HorizontalMoveX = [-1, 0, 0, 1]
    VerticalMoveY = [0, -1, 1, 0]
    X, Y = len(Grid), len(Grid[0])
    VisitedBlocks = [[0 for _ in range(Y)] for _ in range(X)]
    VisitedBlocks[Start.x][Start.y] = 1
    Stack = Deque()
    Sol = Node(Start, 0)
    Stack.append(Sol)
    Steps = 0

    while Stack:
        CurrentBlock = Stack.pop()
        CurrentPosition = CurrentBlock.Pos

        if CurrentPosition.x == Dest.x and CurrentPosition.y == Dest.y:
            print(f"DFSAlgo Visited Nodes: {Steps}")
            return CurrentBlock.Step

        for i in range(4):
            NewX = CurrentPosition.x + HorizontalMoveX[i]
            NewY = CurrentPosition.y + VerticalMoveY[i]

            if 0 <= NewX < X and 0 <= NewY < Y:
                if Grid[NewX][NewY] == 1 and not VisitedBlocks[NewX][NewY]:
                    Steps += 1
                    VisitedBlocks[NewX][NewY] = 1
                    Stack.append(Node(GridPosition(NewX, NewY), CurrentBlock.Step + 1))
    return -1

def Heuristic(a: GridPosition, b: GridPosition):
	return abs(a.x - b.x) + abs(a.y - b.y)

def AStarAlgoSolver(Grid, Dest: GridPosition, Start: GridPosition):
	X, Y = len(Grid), len(Grid[0])
	HorizontalMoveX = [-1, 0, 0, 1]
	VerticalMoveY = [0, -1, 1, 0]
	VisitedBlocks = [[0 for _ in range(Y)] for _ in range(X)]
	VisitedBlocks[Start.x][Start.y] = 1
	Queue = Deque()
	Closed = set()
	Sol = Node(Start, 0)
	Queue.priority(Sol)
	Steps = 0

	while Queue:
		CurrentBlock = Queue.pop()
		CurrentPosition = CurrentBlock.Pos

		if CurrentPosition.x == Dest.x and CurrentPosition.y == Dest.y:
			print(f"\nA* Algo Visited Nodes: {Steps}")
			return CurrentBlock.Step

		for i in range(4):
			NewX = CurrentPosition.x + HorizontalMoveX[i]
			NewY = CurrentPosition.y + VerticalMoveY[i]

			if 0 <= NewX < X and 0 <= NewY < Y:
				if Grid[NewX][NewY] == 1 and not VisitedBlocks[NewX][NewY]:
					Steps += 1
					VisitedBlocks[NewX][NewY] = 1
					Cost = CurrentBlock.Step + 1
					HeuristicCost = abs(NewX - Dest.x) + abs(NewY - Dest.y)
					Queue.append(Node(GridPosition(NewX, NewY), Cost + HeuristicCost))

	return -1

def main():
	Maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
		[0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
		[0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
		[0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0],
		[0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
		[0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
		[0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
		[1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1],
		[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
		[0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

	Destination = GridPosition(8,11)
	Starting = GridPosition(8,0)

	ResAStar = AStarAlgoSolver(Maze, Destination, Starting)
	ResDFS = DFSAlgoSolver(Maze, Destination, Starting)
	ResBFS = BFSAlgoSolver(Maze, Destination, Starting)
main()

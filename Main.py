import API
import sys
from typing import Type
import heapq
from statistics import median

def log(s):
	sys.stderr.write('{}\n'.format(s))
	sys.stderr.flush()

def tmanhattan_distance(a, b):
	return abs(a[0]-b[0]) + abs(a[1] - b[1])
	
def aStar(maze_array, current_x: int, current_y: int, goal_x: int, goal_y: int):
	log(maze_array[current_x][current_y])
	neighbors = [(0,1), (0,-1), (1, 0), (-1,0)]
	start = (current_x,current_y)
	goal = (goal_x, goal_y)
	close_set = set()
	came_from = {}
	gscore = {start:0}
	fscore = {start:tmanhattan_distance(start,goal)}
	oheap = []
	heapq.heappush(oheap, (fscore[start], start))
	while oheap:
		current = heapq.heappop(oheap)[1]
		if current == goal:
			data = []
			while current in came_from:
				data.append(current)
				current = came_from[current]
			data.reverse()
			return data
		
		close_set.add(current)
		for i,j in neighbors:
			neighbor = current[0] + i, current[1] + j
			tentative_g_score = gscore[current] + tmanhattan_distance(current, neighbor)
			if 0 <= neighbor[0] < len(maze_array):
				if 0 <= neighbor[1] < len(maze_array[1]):
					if i == 0 and j == 1 and bool(4 & maze_array[neighbor[0]][neighbor[1]]):
						continue
					if i == 0 and j == -1 and bool(1 & maze_array[neighbor[0]][neighbor[1]]):
						continue
					if i == 1 and j == 0 and bool(8 & maze_array[neighbor[0]][neighbor[1]]):
						continue
					if i == -1 and j == 0 and bool(2 & maze_array[neighbor[0]][neighbor[1]]):
						continue
				else:
					continue
			else:
				continue
			
			if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
				continue
			
			if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
				came_from[neighbor] = current
				gscore[neighbor] = tentative_g_score
				fscore[neighbor] = tentative_g_score + tmanhattan_distance(neighbor, goal)
				heapq.heappush(oheap, (fscore[neighbor], neighbor))
	return False

"""
def concat_int(a,b):
	if a == 5:
		inp = [str(b)]
	if b == 5:
		inp = [str(a)]
	inp = [str(a), str(b)]
	l = [list(w) for w in inp]
	sl = []
	[sl.extend(s) for s in l]
	return int(''.join(sorted(list(set(sl)))))
"""
	
def concat_bin(a,b):
	if a == 16:
		return b
	elif b == 16:
		return a
	else:
		return a|b

def map(maze_array, x, y, degmode):
	F = API.wallFront()
	R = API.wallRight()
	L = API.wallLeft()
	if F:
		if (degmode==0):
			if y != 15:
				maze_array[x][y+1] = concat_bin(maze_array[x][y+1], 4)
			API.setWall(x,y,'n')
			maze_array[x][y] = concat_bin(maze_array[x][y], 1)
		elif (degmode==1):
			if x != 15:
				maze_array[x+1][y] = concat_bin(maze_array[x+1][y], 8) 
			API.setWall(x,y,'e')
			maze_array[x][y] = concat_bin(maze_array[x][y], 2)
		elif (degmode==2):
			if y != 0:
				maze_array[x][y-1] = concat_bin(maze_array[x][y-1], 1) 
			API.setWall(x,y,'s')
			maze_array[x][y] = concat_bin(maze_array[x][y], 4)
		elif (degmode==3): 
			if x != 0:
				maze_array[x-1][y] = concat_bin(maze_array[x-1][y], 2)
			API.setWall(x,y,'w')
			maze_array[x][y] = concat_bin(maze_array[x][y], 8)
	if R:
		if (degmode==0):
			if x != 15:
				maze_array[x+1][y] = concat_bin(maze_array[x+1][y], 8) 
			API.setWall(x,y,'e')
			maze_array[x][y] = concat_bin(maze_array[x][y], 2)
		elif (degmode==1): 
			if y != 0:
				maze_array[x][y-1] = concat_bin(maze_array[x][y-1], 1) 
				API.setWall(x,y,'s')
				maze_array[x][y] = concat_bin(maze_array[x][y], 4)
		elif (degmode==2): 
			if x != 0:
				maze_array[x-1][y] = concat_bin(maze_array[x-1][y], 2)
				API.setWall(x,y,'w')
				maze_array[x][y] = concat_bin(maze_array[x][y], 8)
		elif (degmode==3): 
			if y != 15:
				maze_array[x][y+1] = concat_bin(maze_array[x][y+1], 4)
				API.setWall(x,y,'n')
				maze_array[x][y] = concat_bin(maze_array[x][y], 1)
	if L:
		if (degmode==0): 
			if x != 0:
				maze_array[x-1][y] = concat_bin(maze_array[x-1][y], 2)
			API.setWall(x,y,'w')
			maze_array[x][y] = concat_bin(maze_array[x][y], 8)
		elif (degmode==1): 
			if y != 15:
				maze_array[x][y+1] = concat_bin(maze_array[x][y+1], 4)
			API.setWall(x,y,'n')
			maze_array[x][y] = concat_bin(maze_array[x][y], 1)
		elif (degmode==2):
			if x != 15:
				maze_array[x+1][y] = concat_bin(maze_array[x+1][y], 8) 
			API.setWall(x,y,'e') 
			maze_array[x][y] = concat_bin(maze_array[x][y], 2)
		elif (degmode==3): 
			if y != 0:
				maze_array[x][y-1] = concat_bin(maze_array[x][y-1], 1) 
			API.setWall(x,y,'s')
			maze_array[x][y] = concat_bin(maze_array[x][y], 4)
		
	elif not F and not R and not L and maze_array[x][y]==0:
		maze_array[x][y] = 16
	
	for i in range(0,16):
		for j in range(0,16):
			API.setText(i,j,str(maze_array[i][j]))
				
	return maze_array

def set_degmode(desired, cur):
	if desired == cur:
		return cur
	if desired == (cur+1)%4:
		API.turnRight()
		return desired
	elif desired == (cur-1)%4:
		API.turnLeft()
		return desired
	else:
		API.turnRight()
		API.turnRight()
		return desired

def flood_fill(maze_array, x, y):
	pass
	

def main():
	log('Running')
	MAZE_WIDTH = API.mazeWidth()
	MAZE_HEIGHT = API.mazeHeight()
	maze_array = [[0 for j in range(MAZE_HEIGHT)] for i in range(MAZE_WIDTH)]
	FINISH_X = 8
	FINISH_Y = 8
	START_X = 0
	START_Y = 0
	current_x = START_X
	current_y = START_Y
	oldpath = []
	old_path = []
	degmode = 0
	completed = False
	while True:
		if not completed:
			log('Mapping')
			maze_array = map(maze_array, current_x, current_y, degmode)
			log('Finished mapping; pathing')
			path = aStar(maze_array, current_x, current_y, FINISH_X, FINISH_Y)
			log('Finished pathing')
			if path:
				for p in old_path:
					API.setColor(p[0], p[1], 'k')
				log(path)
				move_to_x = path[0][0]
				move_to_y = path[0][1]
				for p in path:
					API.setColor(p[0], p[1], 'B')
				old_path = path
			else:
				log('Found end')
				completed = True
		else:
			path = aStar(maze_array, current_x, current_y, START_X, START_Y)
			log('Finished pathing')
			if path:
				for p in old_path:
					API.setColor(p[0], p[1], 'k')
				log(path)
				move_to_x = path[0][0]
				move_to_y = path[0][1]
				for p in path:
					API.setColor(p[0], p[1], 'B')
				old_path = path
			else:
				break
		args = ["moveForward"]
		response = ''
		if move_to_x == current_x and move_to_y == current_y + 1:
			degmode = set_degmode(0, degmode)
			if not API.wallFront():
				try:
					API.moveForward()
				except MouseCrashedError as e:
					log(e)
					break
				current_y += 1
		if move_to_x == current_x + 1 and move_to_y == current_y:
			degmode = set_degmode(1, degmode)
			if not API.wallFront():
				try:
					API.moveForward()
				except MouseCrashedError as e:
					log(e)
					break
				current_x += 1
		if move_to_x == current_x and move_to_y == current_y - 1:
			degmode = set_degmode(2, degmode)
			if not API.wallFront():
				try:
					API.moveForward()
				except MouseCrashedError as e:
					log(e)
					break
				current_y -= 1
		if move_to_x == current_x - 1 and move_to_y == current_y:
			degmode = set_degmode(3, degmode)
			if not API.wallFront():
				try:
					API.moveForward()
				except MouseCrashedError as e:
					log(e)
					break
				current_x -= 1
		"""
		printArr = maze_array
		for p in path:
			printArr[p[0]][p[1]] = 2
		for i in range(32):
			for j in range(32):
				if printArr[i][j] == 0: 
					sys.stderr.write('[]')
				elif printArr[i][j] == 1:
					sys.stderr.write('  ')
				else:
					sys.stderr.write('..')
			sys.stderr.write('\n')

		sys.stderr.flush()
		"""
if __name__ == '__main__':
	main()
				


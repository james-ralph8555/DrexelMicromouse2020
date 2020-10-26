import API
import sys
from typing import Type
import heapq

def log(s):
	sys.stderr.write('{}\n'.format(s))
	sys.stderr.flush()

def tmanhattan_distance(a, b):
	return abs(a[0]-b[0]) + abs(a[1] - b[1])
	
def aStar(maze_array, current_x: int, current_y: int):
	neighbors = [(0,2), (0,-2), (2, 0), (-2,0)]
	start = (current_x,current_y)
	goal = (17, 17)
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
					if i == 0 and j == 2 and maze_array[neighbor[0]][neighbor[1] - 1] == 1:
						continue
					if i == 0 and j == -2 and maze_array[neighbor[0]][neighbor[1] + 1] == 1:
						continue
					if i == 2 and j == 0 and maze_array[neighbor[0] - 1][neighbor[1]] == 1:
						continue
					if i == -2 and j == 0 and maze_array[neighbor[0] + 1][neighbor[1]] == 1:
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
	
def map(maze_array, current_x, current_y, degmode):
	empty = 0
	wall = 1
	apix = (current_x-1)//2
	apiy = (current_y-1)//2
	if degmode == 0:
		if API.wallFront():
			maze_array[current_x][current_y+1] = wall
			API.setWall(apix, apiy, 'n')
		if API.wallRight():
			maze_array[current_x+1][current_y] = wall
			API.setWall(apix, apiy, 'e')
		if API.wallLeft():
			maze_array[current_x-1][current_y] = wall
			API.setWall(apix, apiy, 'w')
	if degmode == 1:
		if API.wallFront():
			maze_array[current_x+1][current_y] = wall
			API.setWall(apix, apiy, 'e')
		if API.wallRight():
			maze_array[current_x][current_y-1] = wall
			API.setWall(apix, apiy, 's')
		if API.wallLeft():
			maze_array[current_x][current_y+1] = wall
			API.setWall(apix, apiy, 'n')
	if degmode == 2:
		if API.wallFront():
			maze_array[current_x][current_y-1] = wall
			API.setWall(apix, apiy, 's')
		if API.wallRight():
			maze_array[current_x-1][current_y] = wall
			API.setWall(apix, apiy, 'w')
		if API.wallLeft():
			maze_array[current_x+1][current_y] = wall
			API.setWall(apix, apiy, 'e')
	if degmode == 3:
		if API.wallFront():
			maze_array[current_x-1][current_y] = wall
			API.setWall(apix, apiy, 'w')
		if API.wallRight():
			maze_array[current_x][current_y+1] = wall
			API.setWall(apix, apiy, 'n')
		if API.wallLeft():
			maze_array[current_x][current_y-1] = wall
			API.setWall(apix, apiy, 's')
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

def main():
	log('Running')
	MAZE_WIDTH = API.mazeWidth() * 2 + 2
	MAZE_HEIGHT = API.mazeHeight() * 2 + 2
	maze_array = [[0 for j in range(MAZE_HEIGHT)] for i in range(MAZE_WIDTH)]
	FINISH_X = 17
	FINISH_Y = 17
	START_X = 1
	START_Y = 1
	current_x = START_X
	current_y = START_Y
	oldpath = []
	old_path = []
	degmode = 0
	while True:
		log('Mapping')
		maze_array = map(maze_array, current_x, current_y, degmode)
		log('Finished mapping; pathing')
		path = aStar(maze_array, current_x, current_y)
		if path:
			for p in old_path:
				API.setColor((p[0]-1)//2, (p[1]-1)//2, 'k')
			log(path)
			move_to_x = path[0][0]
			move_to_y = path[0][1]
			for p in path:
				API.setColor((p[0]-1)//2, (p[1]-1)//2, 'B')
			old_path = path
		else:
			break
		args = ["moveForward"]
		response = ''
		if move_to_x == current_x and move_to_y == current_y + 2:
			degmode = set_degmode(0, degmode)
			if not API.wallFront():
				try:
					API.moveForward()
				except MouseCrashedError as e:
					log(e)
					break
				current_y += 2
		if move_to_x == current_x + 2 and move_to_y == current_y:
			degmode = set_degmode(1, degmode)
			if not API.wallFront():
				try:
					API.moveForward()
				except MouseCrashedError as e:
					log(e)
					break
				current_x += 2
		if move_to_x == current_x and move_to_y == current_y - 2:
			degmode = set_degmode(2, degmode)
			if not API.wallFront():
				try:
					API.moveForward()
				except MouseCrashedError as e:
					log(e)
					break
				current_y -= 2
		if move_to_x == current_x - 2 and move_to_y == current_y:
			degmode = set_degmode(3, degmode)
			if not API.wallFront():
				try:
					API.moveForward()
				except MouseCrashedError as e:
					log(e)
					break
				current_x -= 2
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
if __name__ == '__main__':
	main()
				


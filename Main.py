import API
import sys
from typing import Type
import heapq
from collections import deque
from math import sqrt

def log(s):
	sys.stderr.write('{}\n'.format(s))
	sys.stderr.flush()

def manhattan_distance(a, b, maze_array):
	return abs(a[0]-b[0]) + abs(a[1] - b[1])
	
def manhattan_distance_explore(a, b, maze_array):
	if maze_array[b[0]][b[1]] != 0:
		return (abs(a[0]-b[0]) + abs(a[1] - b[1]))**2
	else:
		return abs(a[0]-b[0]) + abs(a[1] - b[1])
		
def manhattan_distance_gotoint(a, b, maze_array):
	if maze_array[b[0]][b[1]] == 0:
		return sys.maxsize
	else:
		return (abs(a[0]-b[0]) + abs(a[1] - b[1]))
		
def manhattan_distance_goto_start(a, b, maze_array):
	if maze_array[b[0]][b[1]] == 0:
		return (abs(a[0]-b[0]) + abs(a[1] - b[1]))/2
	else:
		return abs(a[0]-b[0]) + abs(a[1] - b[1])
		
def aStar(maze_array, current_x: int, current_y: int, goal_x: int, goal_y: int, h_func, state):
	for i in range(16):
		for j in range(16):
			API.clearText(i, j)
	neighbors = [(0,1), (0,-1), (1, 0), (-1,0)]
	start = (current_x,current_y)
	goal = (goal_x, goal_y)
	close_set = set()
	came_from = {}
	gscore = {start:0}
	fscore = {start:h_func(start,goal, maze_array)}
	oheap = []
	heapq.heappush(oheap, (fscore[start], start))
	while oheap:
		current = heapq.heappop(oheap)[1]
		if current == goal:
			if current_x == 4 and current_y == 14:
				log(came_from)
			data = []
			while current in came_from:
				data.append(current)
				current = came_from[current]
			data.reverse()
			return data
		
		close_set.add(current)
		for i,j in neighbors:
			neighbor = current[0] + i, current[1] + j
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
			
			tentative_g_score = gscore[current] + h_func(current, neighbor, maze_array)
			
			if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
				continue
			
			t_path = []
			t = current[:]
			c = False
			while t in came_from:
				if came_from[t] in t_path:
					c = True
					break
				t_path.append(t)
				t = came_from[t]
			
			if c:
				continue	
			
			if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
				came_from[neighbor] = current
				gscore[neighbor] = tentative_g_score
				fscore[neighbor] = tentative_g_score + h_func(neighbor, goal, maze_array)
				if state == 3 and fscore[neighbor] > sys.maxsize:
					return False
				API.setText(neighbor[0],neighbor[1],str(fscore[neighbor]))
				
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

def mapping(maze_array, x, y, degmode, intersections):
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

	if maze_array[x][y] == 1 or maze_array[x][y] == 2 or maze_array[x][y] == 4 or maze_array[x][y] == 8 or maze_array[x][y] == 16:
		intersections.append((x,y))
		
	return maze_array, intersections

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

def DFS(maze_array, start_x, start_y, visited):
	v = visited.copy()
	goal = (8,8)
	stack = deque([([], (start_x,start_y))])
	neighbors = [(0,1), (0,-1), (1, 0), (-1,0)]
	MAZE_WIDTH = API.mazeWidth()
	MAZE_HEIGHT = API.mazeHeight()
	v.remove((start_x, start_y))
	paths = []
	while stack:
		path, current = stack.pop()
		if current ==  goal:
			paths.append(path)
			continue
		if (current[0],current[1]) in v:
			continue
		v.add((current[0],current[1]))
		for i, j in neighbors:
			neighbor = [current[0] + i, current[1] + j]
			if 0 <= neighbor[0] < len(maze_array) and 0 <= neighbor[1] < len(maze_array[1]):
					if neighbor in path:
						continue
					if i == 0 and j == 1 and not bool(4 & maze_array[neighbor[0]][neighbor[1]]):
						stack.append((path + [neighbor], (neighbor[0], neighbor[1])))
						continue
					if i == 0 and j == -1 and not bool(1 & maze_array[neighbor[0]][neighbor[1]]):
						stack.append((path + [neighbor], (neighbor[0], neighbor[1])))
						continue
					if i == 1 and j == 0 and not bool(8 & maze_array[neighbor[0]][neighbor[1]]):
						stack.append((path + [neighbor], (neighbor[0], neighbor[1])))
						continue
					if i == -1 and j == 0 and not bool(2 & maze_array[neighbor[0]][neighbor[1]]):
						stack.append((path + [neighbor], (neighbor[0], neighbor[1])))
						continue
			else:
				continue
	log(len(paths))
	leastdist = sys.maxsize
	leasti = -1
	for i, p in enumerate(paths):
		if len(p) < leastdist:
			leastdist = len(p)
			leasti = i
	if leasti == -1:
		return False
	elif len(paths[leasti]) == 1:
		if path[leasti][0] == goal[0] and path[leasti][1] == goal[1]:
			return path[leasti]
		else:
			return False
	else:
		log(leasti)
		log(paths[leasti] == paths[0])
		log(paths[leasti])
		return paths[leasti]

def move_to(current_x, current_y, move_to_x, move_to_y, degmode):
	args = ["moveForward"]
	response = ''
	if move_to_x == current_x and move_to_y == current_y + 1:
		degmode = set_degmode(0, degmode)
		if not API.wallFront():
			try:
				API.moveForward()
			except MouseCrashedError as e:
				log(e)
				return current_x, current_y, degmode
			current_y += 1
	if move_to_x == current_x + 1 and move_to_y == current_y:
		degmode = set_degmode(1, degmode)
		if not API.wallFront():
			try:
				API.moveForward()
			except MouseCrashedError as e:
				log(e)
				return current_x, current_y, degmode
			current_x += 1
	if move_to_x == current_x and move_to_y == current_y - 1:
		degmode = set_degmode(2, degmode)
		if not API.wallFront():
			try:
				API.moveForward()
			except MouseCrashedError as e:
				log(e)
				return current_x, current_y, degmode
			current_y -= 1
	if move_to_x == current_x - 1 and move_to_y == current_y:
		degmode = set_degmode(3, degmode)
		if not API.wallFront():
			try:
				API.moveForward()
			except MouseCrashedError as e:
				log(e)
				return current_x, current_y, degmode
			current_x -= 1
	return current_x, current_y, degmode
	
def move_right(x,y):
	return x+1, y
def move_down(x,y):
	return x,y-1
def move_left(x,y):
	return x-1,y
def move_up(x,y):
	return x,y+1
def gen_points(end):
	from itertools import cycle
	_moves = cycle([move_right, move_down, move_left, move_up])
	n=0
	pos = 8,8
	times_to_move = 1
	
	yield n, pos
	
	while True:
		for _ in range(2):
			move = next(_moves)
			for _ in range(times_to_move):
				if n>=end:
					return
				pos = move(*pos)
				n+=1
				yield n,pos
		times_to_move+=1

def closest_unexplored_to_goal(maze_array, visited, current_x, current_y, spiral, reached_goal): 
	if reached_goal:
		goal_x = 0
		goal_y = 0
	else:
		goal_x = 8
		goal_y = 8
	MAZE_WIDTH = API.mazeWidth()
	MAZE_HEIGHT = API.mazeHeight()
	closest = (-1, -1)
	closestdist = sys.maxsize
	shortestpath = sys.maxsize
	for i, coords in spiral:
		n, m = coords
		if 0 <= n < 16 and 0 <= m <= 16:
			if (n,m) not in visited:
				d = manhattan_distance((current_x,current_y), (n,m), 0) + manhattan_distance((n,m), (goal_x,goal_x), 0)
				if d <= closestdist:
					closestdist = d
					pl = len(aStar(maze_array, current_x, current_y, n, m, manhattan_distance_explore, 0))+len(aStar(maze_array, n, m, goal_x, goal_y, manhattan_distance_explore, 0))
					if pl < shortestpath:
						shortestpath = pl
						closest = (n,m)
	return closest[0], closest[1]
	
def path_score(path):
	cur_x = path[0][0]
	last_x = path[0][0]
	last_x2 = -1
	last_x3 = -1
	cur_y = path[0][1]
	last_y = path[0][1]
	last_y2 = -1
	last_y3 = -1

	score = -1
	for n in path[1:len(path)]:
		cur_x = n[0]
		cur_y = n[1]
		if not(cur_x == last_x == last_x2) and not(cur_y == last_y == last_y2):
			score += 2
		elif cur_x == last_x == last_x2 == last_x3 or cur_y == last_y == last_y2 == last_y3:
			score += 0.5
		else:
			score += 1
		last_x3 = last_x2
		last_y3 = last_y2
		last_x2 = last_x
		last_y2 = last_y
		last_x = cur_x
		last_y = cur_y
	return score

def current_score(path, total_effective_distance, total_turns):
	pscore = path_score(path)
	return pscore + 0.1*(pscore + total_effective_distance, total_turns)
	
def main():
	log('Running')
	spiral = list(gen_points(256))
	MAZE_WIDTH = API.mazeWidth()
	MAZE_HEIGHT = API.mazeHeight()
	maze_array = [[0 for j in range(MAZE_HEIGHT)] for i in range(MAZE_WIDTH)]
	intersections = deque([])
	visited = {(0,0)}
	FINISH_X = 8
	FINISH_Y = 8
	START_X = 0
	START_Y = 0
	current_x = START_X
	current_y = START_Y
	oldpath = []
	old_path = []
	degmode = 0
	reached_goal = False
	state = 0 #0 - mapping, 1 - return to start, 2 - goto goal
	while True:
		log(state)
		if state == 0:
			if current_x == FINISH_X and current_y == FINISH_Y:
				reached_goal = True
			log('Mapping')
			maze_array, intersections = mapping(maze_array, current_x, current_y, degmode, intersections)
			#path = DFS(maze_array, current_x, current_y, visited)
			goto_x, goto_y = closest_unexplored_to_goal(maze_array, visited, current_x, current_y, spiral, reached_goal)
			log('going to ' + str(goto_x) + ' ' + str(goto_y))
			while current_x != goto_x or current_y != goto_y:
				maze_array, intersections = mapping(maze_array, current_x, current_y, degmode, intersections)
				path = aStar(maze_array, current_x, current_y, goto_x, goto_y, manhattan_distance, state)
				if path:
					if len(path) > len(old_path):
						for p in old_path:
							API.setColor(p[0], p[1], 'k')
						old_path = path
						break
					for p in old_path:
							API.setColor(p[0], p[1], 'k')
					for p in path:
						API.setColor(p[0], p[1], 'B')
					current_x, current_y, degmode = move_to(current_x, current_y, path[0][0], path[0][1], degmode)
					visited.add((current_x,current_y))	
					old_path = path
				else:
					log('err')
			"""
			if path == False:
				state = 3
			else:
				if path:
					for p in old_path:
						API.setColor(p[0], p[1], 'k')
					for p in path:
						API.setColor(p[0], p[1], 'B')
					current_x, current_y, degmode = move_to(current_x, current_y, path[0][0], path[0][1], degmode)
					visited.add((current_x,current_y))
					old_path = path
			if not any(0 in row for row in maze_array):
				state = 1
			"""
				
			
		if state == 1:
			log('Returning to start')
			maze_array, intersections = mapping(maze_array, current_x, current_y, degmode, intersections)
			log(maze_array[current_x][current_y])
			path = aStar(maze_array, current_x, current_y, START_X, START_Y, manhattan_distance_goto_start, state)
			log(path)
			if path:
				for p in old_path:
					API.setColor(p[0], p[1], 'k')
				for p in path:
					API.setColor(p[0], p[1], 'B')
				current_x, current_y, degmode = move_to(current_x, current_y, path[0][0], path[0][1], degmode)
				old_path = path
			elif current_x == START_X and current_y == START_Y:
				log('Returned to start')
				state = 2
			else:
				printArr = list(map(list, maze_array))
				for n in path:
					printArr[n[0]][n[1]] = str(printArr[n[0]][n[1]])+'+'
				printArr[current_x][current_y] = str(printArr[current_x][current_y]) + '-'
				for i in range(16):
					for j in range(16):
						sys.stderr.write(str(printArr[i][j]) + ' ')
					sys.stderr.write('\n')
				
		if state == 2:
			log('Going to goal')
			path = aStar(maze_array, current_x, current_y, FINISH_X, FINISH_Y, manhattan_distance, state)
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
				state = 1
		"""
		if state == 3:
			log('Returning to last intersection')
			goto = intersections.pop()
			path = aStar(maze_array, current_x, current_y, goto[0], goto[1], manhattan_distance_gotoint, state)
			if path == False:
				state = 1
			else:
				for p in old_path:
					API.setColor(p[0], p[1], 'k')
				for p in path:
					API.setColor(p[0], p[1], 'B')
				for p in path:
					current_x, current_y, degmode = move_to(current_x, current_y, p[0], p[1], degmode)
					visited.add((current_x,current_y))
					printArr = list(map(list, maze_array))
					for n in path:
						printArr[n[0]][n[1]] = str(printArr[n[0]][n[1]])+'+'
					printArr[current_x][current_y] = str(printArr[current_x][current_y]) + '-'
					for i in range(16):
						for j in range(16):
							sys.stderr.write(str(printArr[i][j]) + ' ')
						sys.stderr.write('\n')
					sys.stderr.write('\n')
					sys.stderr.flush()
				old_path = path
				state = 0
		"""	
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
				


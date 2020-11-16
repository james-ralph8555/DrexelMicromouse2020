import API
import sys
import heapq
from collections import deque
from math import sqrt

def log(s):
	sys.stderr.write('{}\n'.format(s))
	sys.stderr.flush()

def manhattan_distance(a, b, visited):
	return abs(a[0]-b[0]) + abs(a[1] - b[1])
	
def manhattan_distance_explore(a, b, visited):
	if visited[b[0]][b[1]]:
		return (abs(a[0]-b[0]) + abs(a[1] - b[1]))**2
	else:
		return abs(a[0]-b[0]) + abs(a[1] - b[1])

def manhattan_distance_visited(a, b, visited):
	if visited[b[0]][b[1]]:
		return abs(a[0]-b[0]) + abs(a[1] - b[1])
	else:
		return sys.maxsize
	
def aStar(maze_array, current_x, current_y, goal_x, goal_y, h_func, state, visited): #modified from code by Christian Careaga (MIT license)
	for i in range(16):
		for j in range(16):
			API.clearText(i, j)
	neighbors = [(0,1), (0,-1), (1, 0), (-1,0)]
	start = (current_x,current_y)
	goal = (goal_x, goal_y)
	close_set = set()
	came_from = {}
	gscore = {start:0}
	fscore = {start:h_func(start,goal, visited)}
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
			
			tentative_g_score = gscore[current] + h_func(current, neighbor, visited)
			
			if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
				continue

			if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
				came_from[neighbor] = current
				gscore[neighbor] = tentative_g_score
				fscore[neighbor] = tentative_g_score + h_func(neighbor, goal, visited)
				if state == 3 and fscore[neighbor] >= sys.maxsize:
					return False
				API.setText(neighbor[0],neighbor[1],str(fscore[neighbor]))
				
				heapq.heappush(oheap, (fscore[neighbor], neighbor))
	return False
	
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

def set_degmode(desired, cur, score):
	if desired == cur:
		return cur, score
	if desired == (cur+1)%4:
		API.turnRight()
		return desired, (score + 1)
	elif desired == (cur-1)%4:
		API.turnLeft()
		return desired, (score + 1)
	else:
		API.turnRight()
		API.turnRight()
		return desired, (score + 2)

def BFS(maze_array, start, goal, visited, allow_unvisited):
	paths = []
	neighbors = [(0,1), (0,-1), (1, 0), (-1,0)]
	q = deque()
	path = [start]
	q.append(path)
	while q:
		path = q[0]
		q.popleft()
		last = path[-1]
		if last ==  goal:
			paths.append(path)
		for i, j in neighbors:
			neighbor = (last[0] + i, last[1] + j)
			if 0 <= neighbor[0] < len(maze_array) and 0 <= neighbor[1] < len(maze_array[1]) and last not in path[1:-1]:
					if i == 0 and j == 1 and not bool(4 & maze_array[neighbor[0]][neighbor[1]]):
						if (allow_unvisited) or visited[neighbor[0]][neighbor[1]]:
							q.append(path + [neighbor])
					if i == 0 and j == -1 and not bool(1 & maze_array[neighbor[0]][neighbor[1]]):
						if (allow_unvisited) or visited[neighbor[0]][neighbor[1]]:
							q.append(path + [neighbor])
					if i == 1 and j == 0 and not bool(8 & maze_array[neighbor[0]][neighbor[1]]):
						if (allow_unvisited) or visited[neighbor[0]][neighbor[1]]:
							q.append(path + [neighbor])
					if i == -1 and j == 0 and not bool(2 & maze_array[neighbor[0]][neighbor[1]]):
						if (allow_unvisited) or visited[neighbor[0]][neighbor[1]]:
							q.append(path + [neighbor])
	best_path = []
	best_score = sys.maxsize
	best_score_path = []
	for p in paths:
		cur_score, score_path = path_score(p)
		last_path = p
		if cur_score < best_score:
			best_path = p
			best_score = cur_score
			best_score_path = score_path
	return best_path, best_score_path, best_score

def move_to(current_x, current_y, degmode, path, maze_array, visited, score):
	dist = 1
	if path[0][0] == current_x and path[0][1] == current_y + 1:
		degmode, score = set_degmode(0, degmode, score)
		for i, n in enumerate(path[1:len(path)]):
			if n[0] == current_x and n[1] == current_y + 2 + i and visited[n[0]][n[1]] and not bool(4 & maze_array[n[0]][n[1]]):
				dist += 1
			else:
				break
		if not API.wallFront():
			try:
				if dist <= 2:
					score += dist
				else:
					score += 2 + (dist-2)/2
				API.moveForward(dist)
			except API.MouseCrashedError as e:
				log(e)
			return current_x, current_y + dist, degmode, score
	if path[0][0] == current_x + 1 and path[0][1] == current_y:
		degmode, score = set_degmode(1, degmode, score)
		for i, n in enumerate(path[1:len(path)]):
			if n[0] == current_x + 2 + i and n[1] == current_y and visited[n[0]][n[1]] and not bool(8 & maze_array[n[0]][n[1]]):
				dist += 1
			else:
				break
		if not API.wallFront():
			try:
				if dist <= 2:
					score += dist
				else:
					score += 2 + (dist-2)/2
				API.moveForward(dist)
			except API.MouseCrashedError as e:
				log(e)
			return current_x + dist, current_y, degmode, score
	if path[0][0] == current_x and path[0][1] == current_y - 1:
		degmode, score = set_degmode(2, degmode, score)
		for i, n in enumerate(path[1:len(path)]):
			if n[0] == current_x and n[1] == current_y - 2 - i and visited[n[0]][n[1]] and not bool(1 & maze_array[n[0]][n[1]]):
				dist += 1
			else:
				break
		if not API.wallFront():
			try:
				if dist <= 2:
					score += dist
				else:
					score += 2 + (dist-2)/2
				API.moveForward(dist)
			except API.MouseCrashedError as e:
				log(e)
			return current_x, current_y - dist, degmode, score
	if path[0][0] == current_x - 1 and path[0][1] == current_y:
		degmode, score = set_degmode(3, degmode, score)
		for i, n in enumerate(path[1:len(path)]):
			if n[0] == current_x - 2 - i and n[1] == current_y and visited[n[0]][n[1]] and not bool(2 & maze_array[n[0]][n[1]]):
				dist += 1
			else:
				break
		if not API.wallFront():
			try:
				if dist <= 2:
					score += dist
				else:
					score += 2 + (dist-2)/2
				API.moveForward(dist)
			except API.MouseCrashedError as e:
				log(e)
			return current_x - dist, current_y, degmode, score

	
def path_score(path):
	score_path = []
	
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
		score_path.append(score)
	return score, score_path

def detect_shortcut_start_to_goal(maze_array, start_x, start_y, goal_x, goal_y, current_x, current_y, visited, checked_pairs, intersections):
	m = (current_x, current_y)
	current_path = [(start_x, start_y)] + aStar(maze_array, start_x, start_y, m[0], m[1], manhattan_distance_visited, 0, visited)
	for i, n in enumerate(current_path[len(current_path):0:-1]):
		if n in intersections and not(m in [(n[0] + k, n[1] + l) for k,l in [(0,1), (0,-1), (1, 0), (-1,0)]]) and (n, m) not in checked_pairs and n!=m:
			shortcut_path = [n] + aStar(maze_array, n[0], n[1], m[0], m[1], manhattan_distance, 0, visited)
			ps_shortcut = path_score(shortcut_path)
			ps_current = path_score(current_path[current_path.index(n):current_path.index(n)+current_path.index(m)])
			checked_pairs.append((n,m))
			if ps_shortcut[0] < ps_current[0] and len(shortcut_path) <= len(current_path):
				log('shortcut detected between ' + str((n,m)))
				log('shortcut path: ' + str(shortcut_path))
				log('shortcut path score: ' + str(ps_shortcut[0]))
				log('current path: ' + str(current_path[current_path.index(n):current_path.index(n)+current_path.index(m)]))
				log('current path score: ' + str(ps_current[0]))
				return shortcut_path, checked_pairs
	return [], checked_pairs

def detect_shortcut_goal_to_start(maze_array, start_x, start_y, goal_x, goal_y, current_x, current_y, visited, checked_pairs, intersections):
	m = (current_x, current_y)
	current_path = [(start_x, start_y)] + aStar(maze_array, start_x, start_y, goal_x, goal_y, manhattan_distance_visited, 0, visited)
	shortcut_path = [(start_x, start_y)] + aStar(maze_array, start_x, start_y, goal_x, goal_y, manhattan_distance, 0, visited)
	ps_shortcut = path_score(shortcut_path)
	ps_current = path_score(current_path)
	if len(aStar(maze_array, current_x, current_y, shortcut_path[0][0], shortcut_path[0][1], manhattan_distance, 0, visited)) > len(aStar(maze_array, current_x, current_y, shortcut_path[-1][0], shortcut_path[-1][1], manhattan_distance, 0, visited)):
		far_end = 0
	else:
		far_end = -1
	if ps_shortcut[0] < ps_current[0] and is_shortcut_economic(maze_array, visited, current_x, current_y, ps_shortcut, ps_current, shortcut_path, 1, far_end):
		log('shortcut detected between start and goal')
		log('shortcut path: ' + str(shortcut_path))
		log('shortcut path score: ' + str(ps_shortcut[0]))
		log('current path: ' + str(current_path))
		log('current path score: ' + str(ps_current[0]))
		return shortcut_path, checked_pairs
	return [], checked_pairs

def is_shortcut(maze_array, n, m, visited, current_x, current_y):
	current_path = [n] + aStar(maze_array, n[0], n[1], m[0], m[1], manhattan_distance_visited, 0, visited)
	shortcut_path = [n] + aStar(maze_array, n[0], n[1], m[0], m[1], manhattan_distance, 0, visited)
	ps_shortcut = path_score(shortcut_path)
	ps_current = path_score(current_path)
	if len(aStar(maze_array, current_x, current_y, shortcut_path[0][0], shortcut_path[0][1], manhattan_distance, 0, visited)) > len(aStar(maze_array, current_x, current_y, shortcut_path[-1][0], shortcut_path[-1][1], manhattan_distance, 0, visited)):
		far_end = 0
	else:
		far_end = -1
	if ps_shortcut[0] < ps_current[0] and is_shortcut_economic(maze_array, visited, current_x, current_y, ps_shortcut, ps_current, shortcut_path, 1.5, far_end):
		return True
	else:
		return False
		
def is_shortcut_economic(maze_array, visited, current_x, current_y, ps_shortcut, ps_current, shortcut_path, allowance, far_end):
	shortcut_path_unvisited = []
	for n in shortcut_path:
		if not visited[n[0]][n[1]]:
			shortcut_path_unvisited.append(n)
	estpath = [(current_x, current_y)] + aStar(maze_array, current_x, current_y, shortcut_path_unvisited[far_end][0], shortcut_path_unvisited[far_end][1], manhattan_distance, 0, visited)
	estcost = path_score(estpath)
	log('estimated shortcut path savings ' + str(ps_current[0] - ps_shortcut[0]))
	log('estimated cost to explore shortcut ' + str(estcost[0]))
	if estcost[0] < (ps_current[0] - ps_shortcut[0])*allowance:
		return True
	else:
		return False
def update_viable(visited, maze_array):
	viable = [row[:] for row in visited]
	for i in range(len(viable)):
		for j in range(len(viable)):
				
			l = False
			r = False
			u = False
			d = False
			if i == 0:
				l = True
				if visited[i+1][j]:
					r = True
			elif i == 15:
				r = True
				if visited[i-1][j]:
					l = True
			else:
				if visited[i+1][j] and visited[i-1][j]:
					l = True
					r = True
			if j == 0:
				d = True
				if visited[i][j+1]:
					u = True
			elif j == 15:
				u = True
				if visited[i][j-1]:
					d = True
			else:
				if visited[i][j+1] and visited[i][j-1]:
					u = True
					d = True
			if l and r and u and d:
				viable[i][j] = True
	return viable
def main():
	log('Running')
	MAZE_WIDTH = API.mazeWidth()
	MAZE_HEIGHT = API.mazeHeight()
	maze_array = [[0 for j in range(MAZE_HEIGHT)] for i in range(MAZE_WIDTH)]
	visited = [[False for j in range(MAZE_HEIGHT)] for i in range(MAZE_WIDTH)]
	viable = [row[:] for row in visited]
	intersections = []
	FINISH_X = 8
	FINISH_Y = 8
	START_X = 0
	START_Y = 0
	current_x = START_X
	current_y = START_Y
	oldpath = []
	old_path = []
	degmode = 0
	state = 0 #0 - mapping, 1 - return to start, 2 - goto goal
	visited[START_X][START_Y] = True
	got_best_score = False
	total_score = 0
	best_run_score = 0
	final_score = 0
	checked_pairs = []
	shortcut_queue = []
	shortcut_order = 0
	while True:
		log('State: ' + str(state))
		if 7 <= current_x <= 8 and 7 <= current_y <= 8: 
			if state == 0:
				state = 1
				log('Changing state to 1: goal to start')
				FINISH_X = current_x
				FINISH_Y = current_y
			if state == 2:
				final_score = total_score * 0.1 + best_run_score
				log('Best Run Turns + Effective Distance : ' + str(best_run_score))
				log('Total Turns + Effective Distance: ' + str(total_score))
				log('Final Weighted Score: ' + str(final_score))
				exit()
		elif any(visited[7:9][7:9]) and state == 0:
			state = 1
			log('Changing state to 1: goal to start')
		if state == 1 and current_x == START_X and current_y == START_Y:
			state = 2
			log('Changing state to 2: final run')
		maze_array, intersections = mapping(maze_array, current_x, current_y, degmode, intersections)
		if state == 0 or state == 2:
			goto_x = FINISH_X
			goto_y = FINISH_Y
		elif state == 1:
			goto_x = START_X
			goto_y = START_Y
		while (current_x != goto_x or current_y != goto_y) and (state != 3):
			if state == 0 or state == 1:
				shortcut_path = []
				maze_array, intersections = mapping(maze_array, current_x, current_y, degmode, intersections)
				''' uncomment to enable shortcut finding - not reccomended
				if (current_x, current_y) in intersections:	
					if state == 0 and goto_x == FINISH_X and goto_y == FINISH_Y:
						shortcut_path, checked_pairs = detect_shortcut_start_to_goal(maze_array, START_X, START_Y, FINISH_X, FINISH_Y, current_x, current_y, visited, checked_pairs, intersections)
					if state == 1 and goto_x == START_X and goto_y == START_Y: 
						shortcut_path, checked_pairs = detect_shortcut_goal_to_start(maze_array, START_X, START_Y, FINISH_X, FINISH_Y, current_x, current_y, visited, checked_pairs, intersections)
					if shortcut_path:
						prev_loc = (current_x, current_y)
						prevstate = state
						not_sc = False
						state = 3
						sc_start = shortcut_path[0]
						sc_end = shortcut_path[-1]
						shortcut_path.reverse()
						log('Changing state to 3: Explore Shortcuts')
						break
				'''
						
				if state != 3:
					path = aStar(maze_array, current_x, current_y, goto_x, goto_y, manhattan_distance_explore, state, visited)
			elif state == 2:				
				path, best_score_path, best_score = BFS(maze_array, (current_x, current_y), (FINISH_X, FINISH_Y), viable, False)
				for i,n in enumerate(path[1:len(path)]):
					API.setText(n[0], n[1], best_score_path[i])
					API.setColor(n[0],n[1],'B')
				if not got_best_score:
					num_visited = 0
					for c in [row.count(True) for row in visited]:
						num_visited += c
					log('Exploration efficiency: ' + str(len(path)) + ' needed, ' + str(num_visited) + ' visited.  Efficiency: ' + str(100*len(path)/num_visited) + '%')
					got_best_score = True
					best_run_score = best_score
			if path:
				if (current_x, current_y) in path:
					path.remove((current_x, current_y))
				for p in old_path:
					API.setColor(p[0], p[1], 'k')
					if state == 2:
						API.clearText(p[0], p[1])
				for i, p in enumerate(path):
					API.setColor(p[0], p[1], 'B')
					if state == 2:
						API.setText(p[0], p[1], best_score_path[i])
				current_x, current_y, degmode, total_score = move_to(current_x, current_y, degmode, path, maze_array, viable, total_score)
				visited[current_x][current_y] = True
				viable = update_viable(visited, maze_array)	
				for i in range(len(visited)):
					for j in range(len(visited)):
						if visited[i][j]:
							API.setColor(i,j,'R')
						elif viable[i][j]:
							API.setColor(i,j,'G')
				old_path = path
				if 7 <= current_x <= 8 and 7 <= current_y <= 8: 
					break
			else:
				log('err')
		if state == 3:
			if shortcut_path and not not_sc:
				log('SC : ' + str(shortcut_path))
				for n in shortcut_path:
					if visited[n[0]][n[1]]:
						shortcut_path.remove(n)
					else:
						API.setColor(n[0], n[1], 'G')
				for n in shortcut_path:
					if not_sc:
						break
					maze_array, intersections = mapping(maze_array, current_x, current_y, degmode, intersections)
					if is_shortcut(maze_array, sc_start, sc_end, visited, current_x, current_y):
						if 0 <= n[0] < len(maze_array) and 0 <= n[1] < len(maze_array[1]) and not visited[n[0]][n[1]] and not not_sc:
							while current_x != n[0] or current_y != n[1]:
								log('sc: visiting ' + str(n) + ' to explore shortcut between ' + str((sc_start, sc_end)))
								maze_array, intersections = mapping(maze_array, current_x, current_y, degmode, intersections)
								if not is_shortcut(maze_array, sc_start, sc_end, visited, current_x, current_y):
									log('Not a shortcut')
									for n in shortcut_path:
										API.setColor(n[0], n[1], 'k')
									not_sc = True
									break
								path = aStar(maze_array, current_x, current_y, n[0], n[1], manhattan_distance, 0, visited)
								for p in old_path:
									API.setColor(p[0], p[1], 'k')
								for i, p in enumerate(path):
									API.setColor(p[0], p[1], 'B')
								current_x, current_y, degmode, total_score = move_to(current_x, current_y, degmode, path, maze_array, visited, total_score)
								old_path = path
								visited[current_x][current_y] = True
								if 7 <= current_x <= 8 and 7 <= current_y <= 8: 
									if prevstate == 0:
										prevstate = 1
										log('Changing prevstate to 1: goal to start')
										FINISH_X = current_x
										FINISH_Y = current_y
								elif any(visited[7:9][7:9]) and prevstate == 0:
									prevstate = 1
									log('Changing prevstate to 1: goal to start')
					else:
						log('Not a shortcut')
						for n in shortcut_path:
							API.setColor(n[0], n[1], 'k')
						not_sc = True
						break

			elif (current_x == sc_end[0] and current_y == sc_end[1] and not not_sc) or not_sc or not(shortcut_path):
				state = prevstate
				log('Changing state to ' + str(prevstate))

		""" uncomment to print array in log
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
				


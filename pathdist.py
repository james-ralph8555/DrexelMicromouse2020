# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 15:21:21 2020


path = [(0,0), (0,1), (0,2), (0,3), (1,3), (1,4), (1,5), (1,6), (1,7), (2,7), (2,6), (2,5), (2,4), (2,3), (2,2), (3,2)]
#path = [(0,0),(0,1),(1,1),(1,2),(1,3),(1,4),(2,4),(2,3),(2,2),(2,1),(2,0)]
curx = path[0][0]
lastx = path[0][0]
lastx2 = -1
lastx3 = -1
cury = path[0][1]
lasty = path[0][1]
lasty2 = -1
lasty3 = -1

run_score = -1

for node in path[1:len(path)]:
    curx = node[0]
    cury = node[1]
    if not(curx == lastx == lastx2) and not(cury == lasty == lasty2):
        run_score += 2
    elif curx == lastx == lastx2 == lastx3 or cury == lasty == lasty2 == lasty3:
        run_score += 0.5
    else:
        run_score += 1
    lastx3 = lastx2
    lasty3 = lasty2
    lastx2 = lastx
    lasty2 = lasty
    lastx = curx
    lasty = cury
    print(node,dist)

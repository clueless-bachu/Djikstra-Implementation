import heapq as hq
import numpy as np
import cv2

actions_cost = {'up':[-1,0,1], 'down':[1,0,1], 'left':[-1,0,1], 'right':[0,1,1],\
 'up-left':[-1,-1,2**0.5],'up-right':[-1,1,2**0.5],'down-left':[1,-1,2**0.5],'down-right':[1,1,2**0.5]}
def get_children(state, mat, size=(200,300)):
	new_states = {}
	for i in actions_cost.values():
		dx, dy, cost = i
		if 0<=state[0]+dx<size[0] and 0<=state[1]+dy<size[1] and mat[state[0]+dx][state[1]+dy]!=1 :
			new_states[(state[0]+dx,state[1]+dy)]= cost
	return new_states


def dijkstra(mat, start, goal):

	cost = np.full(mat.shape, np.inf)
	backtrack = {}
	visited = np.zeros(mat.shape, dtype=bool)
	nodes = [(0,start)]
	cost[start]=0
	while len(nodes):
		min_cost, cord = hq.heappop(nodes)
		if cord == goal:
			break
		elif visited[cord]:
			continue

		visited[cord] = True
		children = get_children(cord, mat, size= mat.shape)
		for child_cords, child_cost in children.items():
			if not visited[child_cords]:
				if cost[child_cords]>= child_cost+min_cost:
					cost[child_cords] = child_cost+min_cost
					backtrack[child_cords] = cord
				hq.heappush(nodes,(cost[child_cords],child_cords))

	return cost, backtrack

def create_map(scale = 1):
    img = np.ones((200,300))
    concave = \
    np.array([[20,200-120],[50,200-150],[75,200-120],[100,200-150],[75,200-185],[25,200-185]],dtype=int)
    img = cv2.fillPoly(img, [concave], 0)
    diamond = np.array([[300-75,200-10],[300-75+25,200-10-15],[300-75,200-10-30],[300-75-25,200-10-15]])
    img = cv2.fillPoly(img, [diamond], 0)
    
    img = cv2.circle(img, (300-75,50), 25, 0, -1)
    img = cv2.ellipse(img, (150,100), (40,20), 
           0, 0, 360, 0, -1)
    x,y = 95,30
    p,q = 75,10
    a = 30*3.14/180
    rect = np.array([[x,200-y],[x+q*np.sin(a),200-(y+q*np.cos(a))],\
                     [x-p*np.cos(a)+q*np.sin(a),200-(y+p*np.sin(a)+q*np.cos(a))],\
                     [x-p*np.cos(a),200-(y+p*np.sin(a))]],dtype=int)
    img = cv2.fillPoly(img, [rect], 0)
#     cv2.imshow('mat',img)

    return 1*(img==0), img

if __name__=='__main__':
	mat, img = create_map()
	start = (0,0)
	goal = (199,210)
	cost, backtrack = dijkstra(mat, start, goal)
	cord = goal

	while 1:
	    try:
	        cord = backtrack[cord]
	        img[cord]= 0
	#         print(cord)
	    except Exception as e:
	        break
	cv2.imshow('img',img)
	while 1:
	    if cv2.waitKey(33) == ord('a'):
	        break
	cv2.destroyAllWindows()
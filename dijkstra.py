# Importing required libraries
import heapq as hq
import numpy as np
import cv2

actions_cost = {'up':[-1,0,1], 'down':[1,0,1], 'left':[-1,0,1], 'right':[0,1,1],\
 'up-left':[-1,-1,2**0.5],'up-right':[-1,1,2**0.5],'down-left':[1,-1,2**0.5],'down-right':[1,1,2**0.5]}

def img_to_cart(i,j):
	'''
	Converts an image cordinates to cartesian cordinates

	input:
		i: row of image
		j: column of image

	returns:
		x: x-cordinate in cartesian system
		y: y-cordinate in cartesian system
	'''
	return j, 199-i

def cart_to_img(x,y):
    return 199-y,x

def incircle(x,y,r=0,c=0):
    # equation of circle: (x-225)^2 + (y-150)= 25^2
    return (x-225)**2 + (y-150)**2 <= (25+r+c)**2

def inellipse(x,y,r=0,c=0):
    # equation of ellipse: (x-150)^{2}/40^{2}+\(y-100)^{2}/20^{2}=1
    return (x-150)**2/(40+r+c)**2+(y-100)**2/(20+r+c)**2 <= 1

def get_straight(x1,y1,x2,y2,r,c,side=False, verbose=False):
    m = (y2-y1)/(x2-x1)
    c_ = y1- x1*(y2-y1)/(x2-x1)
    if side:
        c1 = (r+c)*(1+m*m)**0.5+c_
    else:
        c1 = -(r+c)*(1+m*m)**0.5+c_
    if verbose:
        print(m,c_,c1)
    return m,c1

def indiamond(x,y,r=0,c=0):
    #cords = (225,10), (250,25), (225,40), (200,25)
    m1,c1=get_straight(225,10,250,25,r,c)
    m2,c2=get_straight(250,25,225,40,r,c, True)
    m3,c3=get_straight(225,40,200,25,r,c, True)
    m4,c4=get_straight(200,25,225,10,r,c)
    
    return m1*x+c1<=y and m2*x+c2>=y and m3*x+c3>=y and m4*x+c4<=y

def inconcave1(x,y,r=0,c=0):
    #cords: (25,185),(75,185),(50,150),(20,120)
    m1,c1=get_straight(25,185,75,185,r,c,True)
    m2,c2=get_straight(75,185,50,150,0,0)
    m3,c3=get_straight(50,150,20,120,r,c)
    m4,c4=get_straight(20,120,25,185,r,c,True)
    
    return m1*x+c1>=y and m2*x+c2<=y and m3*x+c3<=y and m4*x+c4>=y

def inconcave2(x,y,r=0,c=0):
    #cords: (75,185),(100,150),(75,120),(50,150)
    m1,c1=get_straight(75,185,100,150,r,c,True)
    m2,c2=get_straight(100,150,75,120,r,c)
    m3,c3=get_straight(75,120,50,150,r,c)
    m4,c4=get_straight(50,150,75,185,0,0,True)
    
    return m1*x+c1>=y and m2*x+c2<=y and m3*x+c3<=y and m4*x+c4>=y

def inrectangle(x,y,r=0,c=0):
    #cords: (95,30),(100,38.66),(35.05,76.16),(30.05,67.5)
    m1,c1=get_straight(95,30,100,38.66,r,c)
    m2,c2=get_straight(100,38.66,35.05,76.16,r,c,True)
    m3,c3=get_straight(35.05,76.16,30.05,67.5,r,c,True)
    m4,c4=get_straight(30.05,67.5,95,30,r,c)
    
    return m1*x+c1<=y and m2*x+c2>=y and m3*x+c3>=y and m4*x+c4<=y


def get_children(state, mat, size=(200,300)):
	new_states = {}
	for i in actions_cost.values():
		dx, dy, cost = i
		if 0<=state[0]+dx<size[0] and 0<=state[1]+dy<size[1] and mat[state[0]+dx][state[1]+dy]!=1 :
			new_states[(state[0]+dx,state[1]+dy)]= cost
	return new_states


def dijkstra(mat, start, goal):
    cost = np.full(mat.shape, np.inf)
    memory = []
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
        memory.append(cord)
        children = get_children(cord, mat, size= mat.shape)
#         print('cord:',cord,'\nchildren: ',children)
        for child_cords, child_cost in children.items():
            if not visited[child_cords]:
                if cost[child_cords]>= child_cost+min_cost:
                    cost[child_cords] = child_cost+min_cost
                    backtrack[child_cords] = cord
                hq.heappush(nodes,(cost[child_cords],child_cords))

    return cost, backtrack,memory

def create_map(r=0,c=0):
    img=np.zeros((200,300))
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            x,y = img_to_cart(i,j)
            if incircle(x,y,r,c) or inellipse(x,y,r,c) \
            or indiamond(x,y,r,c) or inconcave1(x,y,r,c) or inconcave2(x,y,r,c) or inrectangle(x,y,r,c):
                img[i,j]= 1
    return img

def main(start, goal, rad=0, clearance=0,speed=100):

    mat = create_map(rad,clearance)
    
    start = cart_to_img(*start)
    goal = cart_to_img(*goal)
    cost, backtrack, memory = dijkstra(mat, start, goal)
    cord = goal
    cords=[]
    mat = (255*(mat==0)).astype(np.uint8)
    for i in range(0, len(memory)-1,speed):
        for j in range(speed):
            try:
                mat[(memory[i+j])]= 255//2
            except:
                break
        cv2.imshow('img',mat)
        if cv2.waitKey(33) == ord('a'):
            break
    while 1:
        try:
            cord = backtrack[cord]
        except Exception as e:
            if cord == goal:
                print('path not found')
            break
        cords.append(cord)
        
    for i in cords:
        mat[i]=254
        cv2.imshow('img',mat)
        if cv2.waitKey(33) == ord('a'):
            break
    cv2.destroyAllWindows()
    return mat, memory, backtrack

if __name__=='__main__':
	r = int(input("Enter Radius. If point robot, enter 0. Eg: 7\nRadius: "))
	c = int(input("Enter Clearance. If point robot, enter 0. Eg: 3\nClearance: "))
	start = input("Enter x,y cordinates of start point wrt cartesian cordinate system. Eg: \"5 5\" without the quotes\nStart: ")
	goal = input("Enter x,y cordinates of goal point wrt cartesian cordinate system. Eg: \"295 195\" without the quotes\nGoal: ")
	print("Thank You! Enjoy the pretty visualisation :)")
	start = tuple([int(i) for i in start.split()])
	goal = tuple([int(i) for i in goal.split()])
	mat, memory, backtrack=main(start, goal, r,c)
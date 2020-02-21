#importing Libraries
import numpy as np
from itertools import permutations
from collections import deque


def bfs(end, visit, start=(0,1,2,3,4,5,6,7,8), filepath = "./data/Nodes.txt"):
	'''
	Applies breadth first search to a well formed graph. In this case bfs starts from the goal node( named as start )
	and reaches the initial node( named as end). It keeps track of all visited nodes so it doesnt visit the same node twice 

	argument:
	end: the node characterised by the initial configuration of the 8 puzzle
	visit: a dictionary that maps a configuration to true or false (visited or not)
	start: the desired end configuration; default (0,1,2,3,4,5,6,7,8)
	filepath: the text file where all the explored nodes are written

	return:
	track: a dictionary that maps a configuration to its previous configuration and the action needed to reach given configuration

	'''
	track={}
	visit[start]=True
	q = deque()
	q.append(start)
	front = start
	# bfs will end if it reached the end node or there are no more nodes left to explore
	with open(filepath,'w') as f:
		while front != end and len(q):
			front = q[0]
			pos_ = (np.array(front).reshape(3,3).T).flatten()
			pos_ = "".join(str(i)+' ' for i in pos_)
			f.write(pos_+'\n')
			q.popleft()
			for child,action in child_nodes(front):
				if not visit[child]:
					visit[child]=True
					q.append(child)
					track[child]=[tuple(-1*i for i in action),front]
	return track
    
def child_nodes(parent):
	'''
	finds out the possible actions and correcponding resulting child configurations for a given configuration

	arguments:
	parent: the parent node whose children needs to be found

	returns:
	children: a list of tuples with the child node configuration and the corresponding action
	'''
	pos = parent.index(0)
	row = pos//3
	col = pos%3
	parent = np.array(parent).reshape(3,3)
    # possible actions are up, down, left and right
	possible_actions = [(1,0),(-1,0),(0,1),(0,-1)]
	children = []
	for i in possible_actions:
		if -1<col+i[1]<3 and -1<row+i[0]<3:
 			# Swaps 2 tiles and to reveal the child node and adds them to "children"
			parent[row+i[0]][col+i[1]],parent[row][col]=parent[row][col],parent[row+i[0]][col+i[1]]
			children.append((tuple(parent.flatten()),i))
            #swaps in reverse order to get back parent
			parent[row+i[0]][col+i[1]],parent[row][col]=parent[row][col],parent[row+i[0]][col+i[1]]
	return children

def get_starting_node(filepath):
	'''
	reads a text file to return the initil node

	argument:
	filepath: the relative or absolute path of the text file

	returns:
	node: a tuple of values representing the node config 
	'''
	with open(filepath,'r')	as f:
		node = f.readline()
		node = node.split()
		node = tuple(int(i) for i in node)
	return node



if __name__=="__main__":

	a = [0,1,2,3,4,5,6,7,8]
	a = (list(i for i in permutations(a)))
	# creating an adjacency list to store the graphs as a dictionary or hash map
	adj_list = {}
	for i in a:
	    adj_list[i]=[]
	# populating the adjacency list to obtain a graph
	for i in a:
		adj_list[i]=child_nodes(i)
    
    #initialising goal node named "start" and visit data structure
	start = (0,1,2,3,4,5,6,7,8)
	visit={}
	for i in adj_list.keys():
	    visit[i]=False
	visit[start]=True
	
	# getting end node
	pos = get_starting_node('./data/initNode.txt')
	print("starting bfs....")
	# running bfs
	track = bfs(pos,visit)
	print('bfs ended....')

	actions = []
	# since there are unreachable node, it will not be a key in the track dictionary, 
	# so only unreachable nodes will will have key error which is handled by exception statement
	try:
		with open('./data/nodePath.txt','w') as f:
			with open('./data/NodesInfo.txt','w') as g:
			# backtracking from the initial node to goal node using the track variable that has already stored the nodes with corresponding actions
			    while pos != start:

			    	parentnodeindex = str(list(pos).index(0))
			    	step = track[pos]

			    	actions.append(step[0])
			    	pos = step[1]
			    	childnodeindex = str(list(pos).index(0))
			    	pos_ = (np.array(pos).reshape(3,3).T).flatten()
			    	pos_ = "".join(str(i)+' ' for i in pos_)
			    	# the new node is written into the text file
			    	g.write(childnodeindex+' '+parentnodeindex+'\n')
			    	f.write(pos_+'\n')
		print("Path Exists")
	except Exception as e:
		print("Path Doesn't Exist",e)
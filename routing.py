class EdgesClass:
    startNode = 0
    endNode = 0
    def __init__(self,st,en):
        self.startNode = st
        self.endNode = en

class denseNode():
    id = 0
    x = 0.0
    y = 0.0
    childnodes = []
    def __init__(self,id,x_in,y_in):
        self.id = id
        self.x = x_in
        self.y = y_in
        self.childnodes = []
    
    def appChild(self,node):
        self.childnodes.append(node)


import matplotlib.pyplot as plt
arr = []
with open('streets.txt') as f:
    for line in f:
        arr.append(line)

nodes = int(arr[0])
edges = int(arr[1]) 
nodeArray = []
#Load Nodes
for i in range(2,nodes+2):
    a = arr[i].split()
    a1 = a[0] #id
    a2 = float(a[1]) #Xcor
    a3 = float(a[2]) #Ycor
    nodeArray.append(denseNode(a1,a2,a3))

    #Plot the nodes
    plt.plot(a2,a3,'ko')
    plt.annotate(a1,xy=(a2+1,a3+1))    

print("Nodes loaded")

edgeArray = []
#Load edges
for i in range(2+nodes,nodes+2+edges):
    a = arr[i].split()
    st = int(a[0])
    en = int(a[1])
    edgeArray.append(EdgesClass(st,en))
    nodeArray[st-1].appChild(en)

    #plot the edges
    xarr = [nodeArray[st-1].x,nodeArray[en-1].x]
    yarr = [nodeArray[st-1].y,nodeArray[en-1].y]
    plt.plot(xarr,yarr,'b')
print("Edges loaded")
#plt.show()

# for i in range(len(nodeArray)):
#     print(nodeArray[i].childnodes)


#initiate routes list
routes = []
start = 1
lastNode = 4

for i in range(len(nodeArray[start-1].childnodes)):
        routes.append([start,nodeArray[start-1].childnodes[i]])


def route(rr):
    tmp = []
    for i in range(len(rr)):
        last = rr[i][-1]
        if last == lastNode:
            tmp.append(rr[i])
        else:
            for j in range(len(nodeArray[last-1].childnodes)):
                if nodeArray[last-1].childnodes[j] not in rr[i]:
                    tmp2 = rr[i].copy()
                    tmp2.append(nodeArray[last-1].childnodes[j])
                    tmp.append(tmp2)
                    tmp2 = None
    return tmp

while True:
    newRoutes = route(routes)
    if newRoutes == routes or newRoutes == []:
        break
    routes = newRoutes.copy()

#Print Routes
# for i in range(len(routes)):
#     print(routes[i])

print(len(routes))

import numpy as np

def testingProgram(route):
    corr = True
    for i in range(len(route)):
        cnt = np.zeros(nodes)
        for j in range(len(route[i])):
            cnt[routes[i][j]-1] = 1
        if max(cnt) > 1:
            print("Incorrect route found")
            corr = False

    if corr:
        print("Routes are correct")

testingProgram(routes)
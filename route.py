class PathElement():
    def __init__(self,node,aT,dT,trId,rId):
        self.node = node
        self.arrTime = aT
        self.depTime = dT
        self.tripId = trId
        self.routeId = rId

class Graph():
    def __init__(self):
        self.nStops = 45265
        self.foundPaths = 0
        self.blockTime = []
        self.searchDate = ""
        self.dates = {}
        self.calculatedPaths = []
        self.maxTransfers = 0
        self.maxnPaths = 0
        self.keepSearch = True

        with open("serviceId.txt") as f:
            lines = f.readlines()
            for i in range(len(lines)):
                a = lines[i][:-2].split(",")
                self.dates[a[0]] = a[1:]

        self.numIdToIdx = {}
        self.idxToText = []
        with open("stopsData.txt") as f:
            lines = f.readlines()
            for i in range(len(lines)):
                a = lines[i].split(",")
                self.numIdToIdx[a[1]] = {'idx':int(a[0])}
                self.idxToText.append(a[2])         

    def checkServId(self,date,servId):
        if len(servId)>0:
            li = self.dates[servId]
            i = 0
            while i<len(li):
                if date in li[i]:
                    return True
                i = i+1
        return False
    def checkIfInList(self,li,el):
        
        i = 0
        while i<len(li):
            if el == li[i]:
                return True
            i = i+1
        return False


    from datetime import datetime
    def compTime(self,t1,t2):
        time1 = self.datetime.strptime(t1,"%H:%M:%S")
        time2 = self.datetime.strptime(t2,"%H:%M:%S")
        if int(time1.hour)<int(time2.hour):
            return True
        elif int(time1.hour)==int(time2.hour) and int(time1.minute)<int(time2.minute):
            return True
        return False

    def getOkChilds(self,parent,goTime,parentRoute,parentTripId,date):
        tmp = []
        childNodes = [];routeId = []; servId = [];arrTimes = []; depTimes = []
        with open("stops/"+str(parent)+".txt") as f:
            lines = f.readlines()
            childNodes = lines[5][:-2].split(",")
            servId = lines[6][:-2].split(",")
            routeId = lines[7][:-2].split(",")
            tripId = lines[8][:-2].split(",")
            depTimes = lines[9][:-2].split(",")
            arrTimes = lines[10][:-2].split(",")
    
        for i in range(len(servId)):
            if self.checkServId(date,servId[i]) == True and self.compTime(arrTimes[i],self.blockTime[self.numIdToIdx[childNodes[i]]['idx']]) == True:
                if self.compTime(goTime,depTimes[i]) == True:
                    if self.checkIfInList(parentRoute,routeId[i]) == True and parentTripId == tripId[i]:
                        tmp.append([childNodes[i],routeId[i],tripId[i],depTimes[i],arrTimes[i]])
                    elif self.checkIfInList(parentRoute,routeId[i])==False:
                        tmp.append([childNodes[i],routeId[i],tripId[i],depTimes[i],arrTimes[i]])
        return tmp

    from collections import Counter

    def allPathsUtil(self,atNode,destination,goTime,routeId,tripId,path,visited,date,routes):
        path.append(PathElement(atNode,goTime,'-',tripId,routeId))
        visited[atNode] = True
        routes.append(routeId)
        if atNode == destination:
            if self.foundPaths == 200:
                self.keepSearch = False
            # print("---")
            # for j in range(len(path)):
            #     print(self.idxToText[int(path[j].node)],path[j].arrTime,path[j].depTime)#,path[j].routeId,tripId)
            # print("---")
            self.foundPaths = self.foundPaths + 1
            self.calculatedPaths.append(path.copy())
        
        elif len(self.Counter(routes).keys())<maxTransfers and self.keepSearch == True:
            tmp = self.getOkChilds(atNode,goTime,routes,tripId,date)
            for i in range(len(tmp)):
                if visited[self.numIdToIdx[tmp[i][0]]['idx']] == False:
                    path[len(path)-1].depTime = tmp[i][3]
                    nBef = self.foundPaths
                    self.allPathsUtil(self.numIdToIdx[tmp[i][0]]['idx'],destination,tmp[i][4],tmp[i][1],tmp[i][2],path,visited,date,routes)
                    naf = self.foundPaths
                    deltaPaths = naf - nBef
                    if deltaPaths == 0:# and self.compTime(tmp[i][4],self.blockTime[self.numIdToIdx[tmp[i][0]]['idx']]) == True:
                        self.blockTime[self.numIdToIdx[tmp[i][0]]['idx']] = tmp[i][4]
        path.pop()
        routes.pop()
        visited[atNode] = False


    def allPaths(self,start,destination,date,goTime,lastTime,maxT,nPaths):
        self.maxnPaths = nPaths
        self.maxTransfers = maxT
        path = []
        visited = [False]*self.nStops
        for i in range(self.nStops):
            self.blockTime.append(lastTime)
        import time
        tic = time.perf_counter()
        routes = []
        self.allPathsUtil(start,destination,goTime,"","",path,visited,date,routes)
        toc = time.perf_counter() 
        # for j in range(len(self.calculatedPaths)):
        #     print("---")
        #     for i in range(len(self.calculatedPaths[j])):
        #         print(self.idxToText[int(self.calculatedPaths[j][i].node)],self.calculatedPaths[j][i].arrTime,self.calculatedPaths[j][i].depTime)
        #     print("---") 
        print(self.foundPaths," paths found")
        print(f"Calculated in {toc - tic:0.4f} seconds")

g = Graph()
#start = 134 #'740000144' #Luleå
#stop = 140 #'740000150' #Boden
#start = 7 #'740000007' #Norrköping
#stop = 9 #'740000009' #Linköping
start = 1 #Stockholm
stop = 5 #Uppsala
goDate = '20200816'
startTime = '00:00:00'
endTime =  '23:59:00'
maxTransfers = 20
maxnPaths = 200
g.allPaths(start,stop,goDate,startTime,endTime,maxTransfers,maxnPaths)



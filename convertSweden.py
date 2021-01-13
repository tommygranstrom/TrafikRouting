#Load trips to get service id and routeId for each trip
from collections import defaultdict 
trips = {}
with open('sweden/trips.txt') as f:
    lines = f.readlines()
    for i in range(1,len(lines)):
        a = lines[i].split(',')
        trips[a[2]] = {'service_id':a[1],'route_id':a[0]}
print(len(trips)," trips loaded")

#Service id gives calendar date for a trip
calendar_dates = {}
ser = []
cnt = 0

def seeIf(l,e):
    i = 0
    while i<len(l):
        if e == l[i]:
            return False
        i = i+1
    return True


with open('sweden/calendar_dates.txt') as f:
    lines = f.readlines()
    print(len(lines)," lines")
    for i in range(1,len(lines)):
        a = lines[i].split(",")
        if seeIf(ser,a[0]):
            ser.append(a[0])
        calendar_dates[str(a[0])] = {'serviceId':a[0],'dates':[]}
    for i in range(1,len(lines)):
        a = lines[i].split(',')
        if len(a[1]) == 8: #Valid date
            if seeIf(calendar_dates[a[0]]['dates'],a[1]):
                calendar_dates[a[0]]['dates'].append(a[1])
                cnt = cnt +1
with open("serviceId.txt", 'w') as file:
    for i in range(len(ser)):
        file.write(calendar_dates[ser[i]]['serviceId']+","+",".join(calendar_dates[ser[i]]['dates'])+";"+"\n")
print(len(ser)," service id saved")
print(len(calendar_dates)," calendar_dates")

stops = {}
hpls = []
hplsToFile = []
with open('sweden/stops.txt') as f:
    lines = f.readlines()
    for i in range(1,len(lines)):
        hplsToFile.append(str(i-1)+","+lines[i])
        a = lines[i].split(',')
        hpls.append(a[0])
        stops[a[0]] = {'numId':a[0],'txtId':a[1],'lat':a[2],'lon':a[3],'childs':[],'childSid':[],'childRouteId':[],'childTripId':[],'depTime':[],'arrTime':[]}
print(len(stops)," stops loaded")

with open("stops.txt", 'w') as file:
    for i in range(len(hplsToFile)):
        file.write(hplsToFile[i])
print(len(hplsToFile)," stops saved to file")
from datetime import datetime

# # Create edges, with trip id, get date
# inCorrs = 0
# eds = 0
# tcnt = 1
# with open("sweden/stop_times.txt") as f:
#     f,next(f)
#     lines = f.readlines()
#     for i in range(1,len(lines)):
#         if(i==tcnt*100000):
#             print(i)
#             tcnt = tcnt +1
#         a = lines[i-1].split(",")
#         b = lines[i].split(",")
#         if a[0] == b[0]: #Same tripid -> it is a edge
#             depTime = a[2]
#             arrTime = b[1]
#             st = a[3]
#             en = b[3]
#             tripid = a[0]
#             rId = trips[tripid]['route_id']
#             sId = trips[tripid]['service_id']
#             try:
#                 dep = datetime.strptime(depTime, "%H:%M:%S")
#                 arr = datetime.strptime(arrTime, "%H:%M:%S")
#             except ValueError:
#                 inCorrs = inCorrs +1
#             else:
#                 if depTime!=arrTime:
#                     stops[st]['childs'].append(en)
#                     stops[st]['childSid'].append(sId)
#                     stops[st]['childRouteId'].append(rId)
#                     stops[st]['childTripId'].append(tripid)
#                     stops[st]['depTime'].append(depTime)
#                     stops[st]['arrTime'].append(arrTime)
#                     eds = eds + 1    
# print(eds," edges loaded")
# import json

# print("Starting fileCreation")
# tcnt = 1
# for i in range(len(hpls)):
#     if tcnt*1000 == i:
#         print(i)
#         tcnt = tcnt + 1
#     path = "stops/"+str(i)+".txt"
#     with open(path, 'w') as file:
#         file.write("numId,txtId,lat,lon,childs,childRouteId,childTripId,depTime,arrTime,\n")
#         file.write(hpls[i]+";\n")
#         file.write(stops[hpls[i]]['txtId']+";\n")
#         file.write(stops[hpls[i]]['lat']+";\n")
#         file.write(stops[hpls[i]]['lon']+";\n")
#         file.write(",".join(stops[hpls[i]]['childs'])+";\n")
#         file.write(",".join(stops[hpls[i]]['childSid'])+";\n")
#         file.write(",".join(stops[hpls[i]]['childRouteId'])+";\n")
#         file.write(",".join(stops[hpls[i]]['childTripId'])+";\n")
#         file.write(",".join(stops[hpls[i]]['depTime'])+";\n")
#         file.write(",".join(stops[hpls[i]]['arrTime'])+";\n")
# print("allDone")







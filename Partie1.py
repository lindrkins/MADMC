
# coding: utf-8

# In[12]:

import math
def getId(data):
    res=[]
    resObj=[]
    for i in range(len(data[0])):
        temp=data[0][i]
        temp2=0
        for j in range(1,len(data)):
            if data[j][i]<temp:
                temp=data[j][i]
                temp2=j
        res.append(temp)
        resObj.append(temp2)
    return res,resObj

def getNad(data):
    t,info=getId(data)
    res=[]
    for i in range(len(data[0])):
        temp=data[info[0]][i]
        for j in range (1,len(info)):
            if temp<data[info[j]][i]:
                temp=data[info[j]][i]
        res.append(temp)
    return res,t

def tcheb(data,eps):
    Nad,Id=getNad(data)
    w=[]
    for i in range(len(Id)):
        w.append(abs(Nad[i]-Id[i]))
    tempRes=100000
    num=0
    for i in range(len(data)):
        temp=w[0]*abs(data[i][0]-Id[0])
        som=temp
        for j in range(1,len(data[0])):
            som=som+w[j]*abs(data[i][j]-Id[j])
            if temp<w[j]*abs(data[i][j]-Id[j]):
                temp=w[j]*abs(data[i][j]-Id[j])
        if tempRes>(temp+eps*som):
            tempRes=(temp+eps*som)
            num=i
    return num,data[num]

def sat(data,num,decideur):
    if decideur==0:
        return True,0
    else:
        #TODO
        return 

def methode(data,decideur,eps):
    if decideur!=0:
        
    dataT=data
    num=tcheb(data,eps)
    test,info=sat(data,num,decideur)
    while(not test):
        dataB=[]
        for i in range(len(dataT)):
            if dataT[i][info]<dataT[num][info]:
                dataB.append(dataT[i])
        dataT=dataB
        num=tcheb(dataT,eps)
        test,info=sat(dataT,num,decideur)
    return dataT[num]

def tchebToP(data,eps,vect):
    Nad,Id=getNad(data)
    Id=vect
    w=[]
    for i in range(len(Id)):
        w.append(abs(Nad[i]-Id[i]))
    tempRes=100000
    num=0
    for i in range(len(data)):
        temp=w[0]*abs(data[i][0]-Id[0])
        som=temp
        for j in range(1,len(data[0])):
            som=som+w[j]*abs(data[i][j]-Id[j])
            if temp<w[j]*abs(data[i][j]-Id[j]):
                temp=w[j]*abs(data[i][j]-Id[j])
        if tempRes>(temp+eps*som):
            tempRes=(temp+eps*som)
            num=i
    return num,data[num]
#>192 ch  >320 Nm  >1269 Kg  >0-100 km/h : 6"7  >PRIX : 26.390 € >CO2 : 139 g/km 
#data=[[1,2,3,4],[4,1,2,3],[3,4,1,2]]
#     max, max                 max, max
#     ch, Nm, Kg, t0-100, CO2, pres, chas
"""data=[[170,250,1145,7.5,124,4,3],#alfa
     [231,370,1315,5.8,166,5,5],#audi
     [180,250,1035,6.7,139,4,3],#abarth5
     [190,250,997,5.9,145,5,5],#abarth6
     [140,210,1128,9,104,3,4],#ford1
     [185,240,1163,6.9,138,3,4],#fordST
     [192,280,1160,6.8,133,4,4],#mini
     [231,320,1205,6.3,155,U,U],#miniJCW
     [150,220,1103,8.5,139,U,U],#OpelS
     [207,280,1218,6.8,174,3,5],#OpelOPC
     [208,300,1160,6.5,125,4,3],#peugot
     [208,300,1160,6.5,125,4,5],#peugotSp
     [120,190,1090,9.4,120,3,3],#renGT
     [200,240,1204,6.7,133,3,4],#renRS
     [220,280,1204,6.6,135,3,4],#renRST
     [110,175,1027,9.1,119,U,U],#seatFR
     [192,320,1269,6.7,139,U,U],#seatCh
     [136,160,1040,8.7,147,3,5],#Suzuki
     [150,250,1212,7.9,110,4,3],#VWB
     [192,320,1269,6.7,139,4,3]#VWGTI
     ]"""
"""data=[[-170,-250,1145,7.5,124],#alfa
     [-231,-370,1315,5.8,166],#audi
     [-180,-250,1035,6.7,139],#abarth5
     [-190,-250,997,5.9,145],#abarth6
     [-140,-210,1128,9,104],#ford1
     [-185,-240,1163,6.9,138],#fordST
     [-192,-280,1160,6.8,133],#mini
     [-231,-320,1205,6.3,155],#miniJCW
     [-150,-220,1103,8.5,139],#OpelS
     [-207,-280,1218,6.8,174],#OpelOPC
     [-208,-300,1160,6.5,125],#peugot
     [-208,-300,1160,6.5,125],#peugotSp
     [-120,-190,1090,9.4,120],#renGT
     [-200,-240,1204,6.7,133],#renRS
     [-220,-280,1204,6.6,135],#renRST
     [-110,-175,1027,9.1,119],#seatFR
     [-192,-320,1269,6.7,139],#seatCh
     [-136,-160,1040,8.7,147],#Suzuki
     [-150,-250,1212,7.9,110],#VWB
     [-192,-320,1269,6.7,139]#VWGTI
     ]"""
data=[[-170,-250,1145,7.5,124,-4,-3],#alfa
     [-231,-370,1315,5.8,166,-5,-5],#audi
     [-180,-250,1035,6.7,139,-4,-3],#abarth5
     [-190,-250,997,5.9,145,-5,-5],#abarth6
     [-140,-210,1128,9,104,-3,-4],#ford1
     [-185,-240,1163,6.9,138,-3,-4],#fordST
     [-192,-280,1160,6.8,133,-4,-4],#mini
     [-207,-280,1218,6.8,174,-3,-5],#OpelOPC
     [-208,-300,1160,6.5,125,-4,-3],#peugot
     [-208,-300,1160,6.5,125,-4,-5],#peugotSp
     [-120,-190,1090,9.4,120,-3,-3],#renGT
     [-200,-240,1204,6.7,133,-3,-4],#renRS
     [-220,-280,1204,6.6,135,-3,-4],#renRST
     [-136,-160,1040,8.7,147,-3,-5],#Suzuki
     [-150,-250,1212,7.9,110,-4,-3],#VWB
     [-192,-320,1269,6.7,139,-4,-3]#VWGTI
     ]
print (tcheb(data,0.000001))


# In[1]:




# In[ ]:



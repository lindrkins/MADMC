# -*- coding: utf-8 -*-

#ON EST EN MINIMISATION!!!!!

from gurobipy import *
import random

#importation des données

#calcul Ideal et Nadir
from Partie1 import *

################### calcul de l'ensemble des Pareto-optimaux ##################

#retourne 1 si item1 > item2 (> = "est préféré")
#        -1 si item1 < item2
#         0 sinon
#nécessite len(item1) = len(item2)
def comparaison(item1, item2):
    nbcrit1 = 0
    nbcrit2 = 0
    for i in range(len(item1)):
        if item1[i] > item2[i]:
            nbcrit2 += 1
        elif item1[i] < item2[i]:
            nbcrit1 += 1
    if nbcrit2 == 0 and nbcrit1 != 0:
        return 1
    if nbcrit1 == 0 and nbcrit2 != 0:
        return -1
    return 0
    
#on considère en entrée un tableau[instance][critère]
def paretoSet(alternatives):
    res = []
    domines = []
    for i in range(len(alternatives)):
        if not (i in domines):
            domine = False
            for j in range(i + 1, len(alternatives)):
                if not (j in domines):
                    if comparaison(alternatives[i], alternatives[j]) == -1:
                        domine = True
                    elif comparaison(alternatives[i], alternatives[j]) == 1:
                        domines.append(j)
            if not domine:
                res.append(alternatives[i])
            else:
                domines.append(i)
    return res


############################ normalisation ####################################
def normalisation(objets):
    #point Nadir approximé
    nadir, ideal = getNad(objets)
    print  "nadir " + str(nadir)
    print "ideal " + str(ideal)
    res = []
    for o in objets:
        tmp = []
        for i in range(len(o)):
            tmp.append(o[i]/float(abs(ideal[i] - nadir[i])))
        res.append(tmp)
    return res

############################### Calcul question ("x > y?") #################################

def MPR(item1, item2, contraintes):
    m = Model("MaxPairwiseRegret")
    #variables
    var = []
    for i in range(len(item1)):
        var.append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="w%d" % (i+1)))
    m.update()
    #fonction objectif
    o = [(item2[i] - item1[i]) for i in range(len(item1))]
    objectif = LinExpr(o, var)
    m.setObjective(objectif, GRB.MAXIMIZE)
    #contraintes
    m.addConstr(LinExpr([1 for i in range(len(item1))], var) >= 0, "Somme à 1 (1)")
    m.addConstr(LinExpr([1 for i in range(len(item1))], var) <= 0, "Somme à 1 (2)")
    t = [0 for i in range(len(item1))]
    for i in range(len(item1)):
        t[i] = 1
        m.addConstr(LinExpr(t, var) >= 0, "Domaine %d" % (i+1))
        t[i] = 0
    for i in range(contraintes):
        m.addConstr(LinExpr(contraintes[i], var) <= 0, "Contrainte %d" (i+1))
    #résolution
    m.optimize
    return m.ObjVal

#retourne le regret max de l'item nbitem ainsi que le(s) item(s) provoquant ce regret
def MRCSet(objets, nbitem, contraintes):
    res = []
    regretmax = 0
    for i in range(len(objets)):
        if i != nbitem:
            regret = MPR(objets[nbitem], objets[i], contraintes)
            if regret > regretmax:
                regretmax = regret
                res = []
            if regret == regretmax:
                res.append(i)
    return regretmax, res

def choixQuestion(objets, contraintes):
    regretmin = 10000 #SALE
    firstItem = []
    regretsmax = []
    for i in range(len(objets)):
        regretmax, res = MRCSet(objets, i, contraintes)
        regretsmax.append(res)
        if regretmax < regretmin:
            regretmin = regretmax
            firstItem = []
        if regretmin == regretmax:
            firstItem.append(i)
    f = random.choice(firstItem)
    return f, random.choice(regretsmax[f])
        
    






################################ TESTS #####################################
t = [[3,6],[4,5],[5,3],[5,9],[7,6],[6,7],[10,5]]
print paretoSet(t) #OK
print normalisation(t) #OK




                
    

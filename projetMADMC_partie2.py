# -*- coding: utf-8 -*-

#ON EST EN MINIMISATION!!!!!

from gurobipy import *
import random

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
    
#entrée : un tableau[instance][critère]
#retourne le tableau des indices des objets Pareto-optimaux
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
    o = [(item1[i] - item2[i]) for i in range(len(item1))]
    objectif = LinExpr(o, var)
    m.setObjective(objectif, GRB.MAXIMIZE)
    #contraintes
    m.addConstr(LinExpr([1 for i in range(len(item1))], var) == 1, "Somme à 1")
    t = [0 for i in range(len(item1))]
    for i in range(len(item1)):
        t[i] = 1
        m.addConstr(LinExpr(t, var) >= 0, "Domaine %d" % (i+1))
        t[i] = 0
    for i in range(len(contraintes)):
        m.addConstr(LinExpr(contraintes[i], var) >= 0, "Contrainte %d" % (i+1))
    #résolution
    m.optimize()
    if m.getAttr(GRB.Attr.ObjVal) < 0.00000001: # pour résoudre le fait que les contraintes doivent être strictes
        return 0
    return m.getAttr(GRB.Attr.ObjVal)

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
        if regretmax <= 0:
            return i, i, regretmax
        if regretmax < regretmin:
            regretmin = regretmax
            firstItem = []
        if regretmin == regretmax:
            firstItem.append(i)
    f = random.choice(firstItem)
    return f, random.choice(regretsmax[f]), regretmin
        

########################### procédures d'élicitation ##########################


def elicitationComplete(objets, pareto):
    candidats = objets
    if pareto:
        candidats = paretoSet(objets)
    toprint = [candidats[i] for i in range(len(candidats))]
    candidats = normalisation(candidats)
    contraintes = []
    res = -1
    while True:
        question = choixQuestion(candidats, contraintes)
        if question[0] == question[1]:
            res = question[0]
            break
        reponse = raw_input("Preferez-vous l'option a : " + str(toprint[question[0]]) + ", ou l'option b : " + str(toprint[question[1]]) + " ? (reponse : a/b) : ")
        while reponse != 'a' and reponse != 'b':
            reponse = raw_input("Il faut repondre 'a' ou 'b'! ")
        if reponse == 'a':
            contraintes.append([candidats[question[1]][i] - candidats[question[0]][i] for i in range(len(candidats[question[0]]))])
        else:
            contraintes.append([candidats[question[0]][i] - candidats[question[1]][i] for i in range(len(candidats[question[0]]))])
    print "La meilleure solution selon vos preferences est : " + str(toprint[res])

def elicitationStop(objets, pareto):
    candidats = objets
    if pareto:
        candidats = paretoSet(objets)
    toprint = [candidats[i] for i in range(len(candidats))]
    candidats = normalisation(candidats)
    contraintes = []
    res = -1
    while True:
        question = choixQuestion(candidats, contraintes)    
        if question[0] == question[1]:
            res = question[0]
            break
        reponse = raw_input("Preferez-vous l'option a : " + str(toprint[question[0]]) + ", ou l'option b : " + str(toprint[question[1]]) + " ? (reponse : a/b, stop pour arreter) :")
        while reponse != 'a' and reponse != 'b' and reponse != 'stop':
            reponse = raw_input("Il faut repondre 'a', 'b' ou 'stop'! ")
        if reponse == 'a':
            contraintes.append([candidats[question[1]][i] - candidats[question[0]][i] for i in range(len(candidats[question[0]]))])
        elif reponse == 'b':
            contraintes.append([candidats[question[0]][i] - candidats[question[1]][i] for i in range(len(candidats[question[0]]))])
        else:
            res = question[0]
            break
    print "La meilleure solution selon vos preferences est : " + str(toprint[res])


############################################ TESTS #################################################

def testNbQuestions(objets, nbiter):
    nbq = 0
    regrets = [0 for i in range(len(objets))]
    for i in range(nbiter):
        nberror = 0
        nbqit = 0
        pref = [random.random() for j in range(len(objets[0]))]
        pref = [pref[j] / sum(pref) for j in range(len(pref))]
        print "pref :" + str(pref)
        candidats = normalisation(objets)
        scores = [sum([pref[k]*candidats[j][k] for k in range(len(pref))]) for j in range(len(candidats))]
        objpref = 0
        minscore = scores[0]
        for j in range(len(scores)):
            if scores[j] < minscore:
                minscore = scores[j]
                objpref = j
        #for j in range(len(objets)):
            #score = sum([pref[k]*objets[j][k] for k in range(len(pref))])
        contraintes = []
        found = False
        it = 0
        while not found:
            question = choixQuestion(candidats, contraintes)
            regrets[it] += question[2]
            if question[0] == question[1]:
                found = True
                if question[0] != objpref:
                    nberror += 1
                else:
                    nbq += nbqit
                nbqit = 0
            else:
                nbqit += 1
                if scores[question[0]] < scores[question[1]]:
                    contraintes.append([candidats[question[1]][i] - candidats[question[0]][i] for i in range(len(candidats[question[0]]))])
                else:
                    contraintes.append([candidats[question[0]][i] - candidats[question[1]][i] for i in range(len(candidats[question[0]]))])
            it += 1
    regrets = [regrets[i] / nbiter for i in range(len(regrets))]
    return nberror, nbq / float(nbiter - nberror), regrets


############################################## PROGRAMME ################################################
#données voitures
data=[[-170,-250,1145,7.5,124],#alfa
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
     ]
"""
comp = raw_input("Elicitation complete ? (o/n) : ")
par = raw_input("Limiter les calculs aux P-opt? (o/n) :")
if comp == 'o':
    if par == 'o':
        elicitationComplete(data, True)
    else:
        elicitationComplete(data, False)
else:
        if par == 'o':
        elicitationStop(data, True)
    else:
        elicitationStop(data, False)"""


##### tests #####
obj = [[16,4], [12,11], [3,16], [6,15], [9,7]]
#print testNbQuestions(obj, 2) # OK! ca semble marcher, et sans erreur en plus
print testNbQuestions(data, 10)
    

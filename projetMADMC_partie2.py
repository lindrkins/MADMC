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
        m.addConstr(LinExpr(contraintes[i], var) <= 0, "Contrainte %d" % (i+1))
    #résolution
    m.optimize()
    print 
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
        if regretmax <= 0: # ce serait plutot < ici mais pour simplifier on fait <=
            return i, i
        if regretmax < regretmin:
            regretmin = regretmax
            firstItem = []
        if regretmin == regretmax:
            firstItem.append(i)
    f = random.choice(firstItem)
    return f, random.choice(regretsmax[f])
        

########################### procédure d'élicitation ##########################


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
        reponse = raw_input("Préférez-vous l'option a : " + str(toprint[question[0]]) + ", ou l'option b : " + str(toprint[question[1]]) + " ? (réponse : a/b) : ")
        while reponse != 'a' and reponse != 'b':
            reponse = raw_input("Il faut répondre 'a' ou 'b'! ")
        if reponse == 'a':
            contraintes.append([candidats[question[0]][i] - candidats[question[1]][i] for i in range(len(candidats[question[0]]))])
        else:
            contraintes.append([candidats[question[1]][i] - candidats[question[0]][i] for i in range(len(candidats[question[0]]))])
    print "La meilleure solution selon vos préférences est : " + str(toprint[res])

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
        reponse = raw_input("Préférez-vous l'option a : " + str(toprint[question[0]]) + ", ou l'option b : " + str(toprint[question[1]]) + " ? (réponse : a/b, stop pour arrêter) :")
        while reponse != 'a' and reponse != 'b' and reponse != stop:
            reponse = raw_input("Il faut répondre 'a', 'b' ou 'stop'! ")
        if reponse == 'a':
            contraintes.append([candidats[question[0]][i] - candidats[question[1]][i] for i in range(len(candidats[question[0]]))])
        elif reponse == 'b':
            contraintes.append([candidats[question[1]][i] - candidats[question[0]][i] for i in range(len(candidats[question[0]]))])
        else:
            res = question[0]
            break
    print "La meilleure solution selon vos préférences est : " + str(toprint[res])






################################ TESTS #####################################
t = [[3,6],[4,5],[5,3],[5,9],[7,6],[6,7],[10,5]]
print paretoSet(t) #OK
#print normalisation(t) #OK

#test avec instance cours MADI
obj = [[16,4], [12,11], [3, 16], [6,15], [9,7]]
#obj = [[9,7], [8,5], [1,3]]
#print paretoSet(obj)
#print MPR(obj[4], obj[5], [])
#print MPR(obj[5], obj[4], [])
#print choixQuestion(obj, [])
elicitationComplete(obj, False) #TROMPE DE SIGNE < au lieu de >



                
    

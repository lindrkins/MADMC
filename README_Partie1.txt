methode(data,decideur,eps):
Cette méthode lance Tchebichev sur data, puis sur un sous ensemble de data si le décideur n’est pas satisfait.
data est une liste de liste de valeurs de critères. les critères à maximiser doivent être remplacé par leur opposé.
décideur est 0 si on ne veut seulement le résultat de Tchebichev et est à 1 si on utilise notre « décideur » (somme pondéré)
eps est l’epsilon.


tchebToP(data,eps,vect):
Cette méthode lance tchebichev sur data et rend un résultat proche de vect ou meilleur que vect.
vect est liste de valeurs de critères.s
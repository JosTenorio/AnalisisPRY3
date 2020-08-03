import numpy as np

# Markov chain code
# [1,2,3 - Terreno] [1,2,3 - Motor] [1,2,3 - Batería] [1 arriba, 2 abajo, 3 izquierda, 4 derecha]

# globals
NODES = [1111, 1112, 1113, 1114, 1121, 1122, 1123, 1124, 1131, 1132, 1133, 1134, 1211, 1212, 1213, 1214, 1221, 1222,
         1223, 1224, 1231, 1232, 1233, 1234, 1311, 1312, 1313, 1314, 1321, 1322, 1323, 1324, 1331, 1332, 1333, 1334,
         2111, 2112, 2113, 2114, 2121, 2123, 2122, 2124, 2131, 2132, 2133, 2134, 2211, 2212, 2213, 2214, 2221, 2222,
         2223, 2224, 2231, 2232, 2233, 2234, 2311, 2312, 2313, 2314, 2321, 2322, 2323, 2324, 2331, 2332, 2333, 2334,
         3111, 3112, 3113, 3114, 3121, 3122, 3123, 3124, 3131, 3132, 3133, 3134, 3211, 3212, 3213, 3214, 3221, 3222,
         3223, 3224, 3231, 3232, 3233, 3234, 3311, 3312, 3313, 3314, 3321, 3322, 3323, 3324, 3331, 3332, 3333, 3334]
SIZE = len(NODES)

def createRandomMarkovChain():
    markovChain = {}
    for currentNode in NODES:
        markovChain[currentNode] = {}
        values = sumToX(SIZE, 1)
        counter = 0
        for nextNode in NODES:
            markovChain[currentNode][nextNode] = values[counter]
            counter += 1
    return markovChain

def sumToX(n, x):
    values = [0.0, x] + list(np.random.uniform(low = 0.0, high = x, size = n - 1))
    values.sort()
    return [values[i+1] - values[i] for i in range(n)]







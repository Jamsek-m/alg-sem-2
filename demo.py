import math


def agent_calc_grad(agent, w):
    return w[0] - agent[0], w[1] - agent[1]


def correct_grad(grads, n, f):
    # filter
    norms = []
    for gi in grads:
        norms.append(math.sqrt(math.pow(gi[0], 2) + math.pow(gi[1], 2)))
    norms.sort()
    for i in range(n - f, n):  # clips f largest gradients to the value of the (f + 1)-th largest norm
        norms[i] = norms[f + 1 - 1]
        grads[i] = grads[f + 1 - 1]


    # aggregate
    x, y = 0, 0
    for gi in grads:
        x += gi[0]
        y += gi[1]
    return x, y  # aggregated gradient


def check_if_close_enough(g, limit=0.05):
    return g[0] < limit and g[1] < limit


A = (1, 1)
B = (10, 0)
C = (17, 1)
D = (2, 7)
FF = (33, 138)

n = 5  # number of the agents
f = 1  # number of the Byzantine faulty agents
w = [7, 12]  # estimation
step = 0.05  # constant

for i in range(100):
    gA = agent_calc_grad(A, w)
    gB = agent_calc_grad(B, w)
    gC = agent_calc_grad(C, w)
    gD = agent_calc_grad(D, w)
    gFF = agent_calc_grad(FF, w)

    g = correct_grad([gA, gB, gC, gD, gFF], n, f)
    if check_if_close_enough(g):
        print(w[0], ' ', w[1])
        print(i)
        break
    else:
        w[0] = w[0] - step * g[0]
        w[1] = w[1] - step * g[1]

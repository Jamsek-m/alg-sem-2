import math


def agent_calc_grad(agent, w):
    # calculates the gradient (really simple in our case - no derivatives)
    return w[0] - agent[0], w[1] - agent[1]


def correct_grad(grads, n, f):
    # filters and aggregates the gradients

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
    # check if the estimation is good enough (aggregated gradient is small enough)
    return g[0] < limit and g[1] < limit


# Assume that the agents are taxi drivers in the city of San Francisco,
# which on our map lies between 0 and 20 on the x axis and 0 and 30 on the y axis

# arguments:
agents = [(1, 1), (10, 0), (17, 1), (33, 138), (31, 1381)]  # agents
f = 2  # number of the Byzantine faulty agents (f < n/2)
w = [10, 15]  # first estimation (random or something)
step = 0.05  # constant (speed of moving on the gradient)

n = len(agents)  # number of the agents
grads = [None] * n  # gradients

c = 0
while True:
    c += 1

    # simulation of receiving gradients from the agents
    for i in range(0, len(agents)):
        grads[i] = agent_calc_grad(agents[i], w)

    g = correct_grad(grads, n, f)
    if check_if_close_enough(g):
        print('meeting point (x, y): ', w[0], ' ', w[1])
        print('steps: ', c)
        break
    else:
        w[0] = w[0] - step * g[0]
        w[1] = w[1] - step * g[1]

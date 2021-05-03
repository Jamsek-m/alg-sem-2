def agent_calc_grad(agent, w):
    return w[0] - agent[0], w[1] - agent[1]


def correct_grad(grads, f: int):
    # TODO clipping
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
# FF = (33, 138)

f = 0  # number of the Byzantine faulty agents
w = [7, 12]  # estimation
step = 0.05  # constant

for i in range(100):
    gA = agent_calc_grad(A, w)
    gB = agent_calc_grad(B, w)
    gC = agent_calc_grad(C, w)
    gD = agent_calc_grad(D, w)

    g = correct_grad([gA, gB, gC, gD], f)
    if check_if_close_enough(g):
        print(w[0], ' ', w[1])
        print(i)
        break
    else:
        w[0] = w[0] - step * g[0]
        w[1] = w[1] - step * g[1]

import math
import matplotlib.pyplot as plt


def agent_calc_grad(agent, w):
    # calculates the gradient (really simple in our case - no derivatives)
    return w[0] - agent[0], w[1] - agent[1]


def clip_norm(current, largest_possible):
    # clips the norm of the current gradient to the size of the largest_possible gradient
    current_norm = math.sqrt(math.pow(current[0], 2) + math.pow(current[1], 2))
    largest_possible_norm = math.sqrt(math.pow(largest_possible[0], 2) + math.pow(largest_possible[1], 2))

    new_current = (largest_possible_norm / current_norm * current[0], largest_possible_norm / current_norm * current[1])
    return new_current


def correct_grad(grads, n, f):
    # filters and aggregates the gradients
    sorted_grads = sorted(grads, key=lambda g: math.sqrt(math.pow(g[0], 2) + math.pow(g[1], 2)))

    for i in range(n - f, n):  # clips f largest gradients so the norm equals to the size of the (f + 1)-th largest norm
        sorted_grads[i] = clip_norm(sorted_grads[i], sorted_grads[f])

    # aggregate
    x, y = 0.0, 0.0
    for gi in sorted_grads:
        x += gi[0]
        y += gi[1]
    return x, y  # aggregated gradient


def check_if_close_enough(g, limit=0.5):
    # check if the estimation is good enough (aggregated gradient is small enough)
    return math.fabs(g[0]) < limit and math.fabs(g[1]) < limit


def draw(agents, w):
    # plot the agents and the estimated meeting point
    x, y = zip(*agents)
    plt.scatter(x, y, color='blue')
    plt.scatter(w[0], w[1], color='red')
    plt.show()


# Assume that the agents are taxi drivers in the city of San Francisco,
# which on our map lies between 0 and 20 on the x axis and 0 and 30 on the y axis

# arguments:
agents = [(1, 1), (12, 11), (10, 0), (17, 1), (333, 191), (3, 13), (235, 132), (137, 173), (19, 15)]
# agents = [(0, 0), (20, 20), (0, 20), (20, 0), (333, 191), (0, 10), (235, 132), (137, 173), (10, 0), (10, 20), (20, 10)]

f = 3  # number of the Byzantine faulty agents (f < n/2) TODO: try to detect automatically
w = [10, 15]  # first estimation (random or something)
step = 0.1  # constant (speed of moving on the gradient)

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
        # move in gradient's direction for a small amount
        w[0] = w[0] - step * g[0]
        w[1] = w[1] - step * g[1]

draw(agents, w)

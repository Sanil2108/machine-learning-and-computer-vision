import numpy as np
import matplotlib.pyplot as plt

def draw(x1, x2):
    ln = plt.plot(x1, x2)
    plt.pause(0.0001)
    ln[0].remove()
    
def sigmoid(score):
    return 1/(1+np.exp(-score))

def calculate_error(line_parameters, points, y):
    p = sigmoid(points * line_parameters)
    error = -((np.log(p).T * y) + (np.log(1-p).T * (1-y)))/len(y)
    return error

def gradient_descent(line_parameters, points, y, alpha):
    m = len(y)
    for i in range(2000):
        p = sigmoid(points*line_parameters)
        gradient = (points.T * (p - y))*(alpha/m)
        line_parameters = line_parameters - gradient
        w1 = line_parameters.item(0)
        w2 = line_parameters.item(1)
        b = line_parameters.item(2)
        x1 = np.array([points[:, 0].min(), points[:, 0].max()])
        x2 = -b/w2 + x1 * (-w1/w2)
        draw(x1, x2)
        print(calculate_error(line_parameters, points, y))
    return line_parameters


n_pts = 100
np.random.seed(0)
b = np.ones(n_pts)
top_region = np.array([np.random.normal(10, 2, n_pts), 
                       np.random.normal(12, 2, n_pts), b]).transpose()
bottom_region = np.array([np.random.normal(5, 2, n_pts), 
                       np.random.normal(6, 2, n_pts), b]).transpose()
all_pts = np.vstack((top_region, bottom_region))
# w1 = -0.1
# w2 = -0.15
# b = 0
line_parameters = np.matrix([np.zeros(3)]).T
linear_combination  = all_pts*line_parameters
probablities = sigmoid(linear_combination)

_, ax = plt.subplots(figsize=(4, 4))
ax.scatter(top_region[:, 0], top_region[:, 1], color='r')
ax.scatter(bottom_region[:, 0], bottom_region[:, 1], color='b')
labels = np.array([np.zeros(n_pts), np.ones(n_pts)]).reshape(2*n_pts, 1)
calculate_error(line_parameters, all_pts, labels)
gradient_descent(line_parameters, all_pts, labels, 0.06)
# draw(x1, x2)
plt.show()



np.array([1, 2, 3])*3
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from pylab import *

class StatManager(object):
    def __init__(self, game):
        self.game = game
        self.fig, self.axes = plt.subplots(2, 1)
        
        self.all_scores = []

        thismanager = get_current_fig_manager()
        thismanager.window.wm_geometry("+0+0")

        plt.tight_layout()

    def draw_score(self, params):
        self.axes[0].clear()

        x_values = np.linspace(0, len(self.all_scores), len(self.all_scores))
        self.axes[0].plot(x_values, self.all_scores, 'o-', color = 'red')
        self.axes[0].set_title('Individual score')
        self.axes[0].set_xlabel('Games')
        self.axes[0].set_ylabel('Score')


    def draw_average_scores(self, params):
        self.axes[1].clear()

        x_values = np.linspace(0, len(self.all_scores)/10, len(self.all_scores)/10)

        averaged_scores = [0] * (len(self.all_scores) / 10)
        for i in range(len(averaged_scores)):
            averaged_scores[i] = float(sum(self.all_scores[10*i:10*(i + 1)]))/10

        self.axes[1].plot(x_values, averaged_scores, 'o-', color = 'red')
        self.axes[1].set_title('Average score')
        self.axes[1].set_xlabel('Games')
        self.axes[1].set_ylabel('Score')

    def update(self, params):
        self.all_scores.append(params['score'])
        self.draw_score(params)
        self.draw_average_scores(params)

        plt.draw()
        plt.pause(1e-10)
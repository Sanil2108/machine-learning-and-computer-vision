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

    def draw_score(self, params):
        self.axes[0].clear()

        self.all_scores.append(params['score'])
        x_values = np.linspace(0, len(self.all_scores), len(self.all_scores))
        self.axes[0].plot(x_values, self.all_scores, 'o-', color = 'red')
        self.axes[0].set_title('Individual score')
        self.axes[0].set_xlabel('Games')
        self.axes[0].set_ylabel('Score')


    def draw_average_scores(self, params):
        pass

    def update(self, params):
        self.draw_score(params)
        self.draw_average_scores(params)

        plt.draw()
        plt.pause(1e-10)
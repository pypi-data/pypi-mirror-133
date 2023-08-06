import os
from pathlib import Path
import matplotlib.pyplot as plt

class VisualizationCmd:
    def __init__(self, config, dataObj, rankers):
        self.viz_dir = 'visualizations'
        self.viz_path = self.make_viz_dir(config)

    def draw(self, metric, data, labels):
        self.line_plot(metric, data, labels)
        return

    def line_plot(self, metric, data, labels):
        for key, value in data.items():
            plt.plot(value['x'], value['y'], label=labels['legend'][key])
        plt.xlabel(labels['x'])
        plt.ylabel(labels['y'])
        if len(data.keys()) > 1:
            plt.legend()
        plt.savefig(self.viz_path / Path(metric + '.eps'), format='eps')
        plt.close()

    def make_viz_dir(self, config):
        if not os.path.exists(config._target / Path(self.viz_dir)):
            os.makedirs(config._target / Path(self.viz_dir))
        return config._target / Path(self.viz_dir)
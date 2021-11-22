from matplotlib import pyplot as plt


class Plotter:

    def __init__(self, name=None):
        self.name = name
        self.diagrams = list()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        l = len(self.diagrams)
        fig, axes = plt.subplots(nrows=l, figsize=(8, 4))

        if l == 1:
            axes = [axes]

        for ax, diagram in zip(axes, self.diagrams):
            plt.sca(ax)
            diagram.plot()
        plt.tight_layout()
        if self.name is not None:
            plt.savefig(self.name)
        else:
            plt.show()

    def add(self, dia):
        self.diagrams.append(dia)
        return dia

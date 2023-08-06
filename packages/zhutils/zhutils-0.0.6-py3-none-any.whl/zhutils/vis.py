from .lib import *


class AdaptiveAxes:
    def __init__(self,
                 n_figure: int,
                 n_col: int = 4,
                 fig_size: tuple = (7, 5)) -> None:
        self.n = n_figure
        self.n_col = min(n_figure, n_col)
        self.n_row = (n_figure + n_col - 1) // n_col
        self.fig_size = (fig_size[0] * self.n_col, fig_size[1] * self.n_row)
        self.fig, self.axes = plt.subplots(self.n_row,
                                           self.n_col,
                                           squeeze=False,
                                           figsize=self.fig_size)
    
    def __iter__(self):
        for i in range(self.n):
            j = i // self.n_col
            k = i % self.n_col
            yield self.axes[j][k]


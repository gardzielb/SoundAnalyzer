from math import ceil

import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from sound_analyzer.audio.plot import plot_sound


class FigureWidget(FigureCanvasQTAgg):
	def __init__(self, plot_width = 9, plot_height = 3, dpi = 100, n_plots = 1):
		n_cols = 2
		n_rows = int(ceil(n_plots / n_cols))

		self.figure = Figure(figsize = (n_cols * plot_width, n_rows * plot_height), dpi = dpi)

		self.axes = []
		for i in range(n_plots):
			self.axes.append(self.figure.add_subplot(n_rows, n_cols, i + 1))

		super().__init__(self.figure)

		self.n_plots = n_plots
		self.idx = 0

	def add_plot(self, data: np.ndarray, sample_rate: int, title: str, silence_ranges: list[tuple[int, int]]):
		if self.idx < self.n_plots:
			plot_sound(data, sample_rate, title, silence_ranges = silence_ranges, axes = self.figure.axes[self.idx])
			self.idx += 1

	def reset(self):
		self.idx = 0
		for ax in self.axes:
			ax.clear()

	def show_plots(self):
		self.figure.tight_layout()
		self.draw()

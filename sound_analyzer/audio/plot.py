from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix


def plot_sound(
		audio: np.ndarray, sample_rate: int, title: str, axes = None,
		silence_ranges: Optional[list[tuple[int, int]]] = None
):
	if axes is None:
		_, axes = plt.subplots()

	audio_len_sec = audio.shape[0] / sample_rate
	t = np.linspace(0, audio_len_sec, num = audio.shape[0])
	axes.plot(t, audio)
	axes.grid(color = 'black', alpha = 0.5, linestyle = '-', linewidth = 0.7)

	if silence_ranges is not None:
		for start, end in silence_ranges:
			axes.hlines(
				y = 0, xmin = start / sample_rate, xmax = end / sample_rate,
				color = 'r', linestyle = '-', linewidth = 3
			)

	axes.set_title(title)
	axes.set_xlabel('Time [s]')


def plot_filter_bank(filter_bank: np.ndarray, sample_rate: int):
	_, axes = plt.subplots()
	nfft = filter_bank.shape[1]
	f = (np.linspace(0, nfft - 1, num = nfft) * sample_rate) / (nfft + 1)
	axes.plot(f, filter_bank.T)
	axes.set_xlabel('f [Hz]')
	axes.set_title('Filter bank')
	plt.xlim(0, sample_rate / 2)


def plot_confusion_matrix(y_true, y_pred, labels, title):
	cm = confusion_matrix(y_true, y_pred, labels = labels)
	div = cm.sum(axis = 1, keepdims = True)
	div = np.where(div > 0, div, 1)
	cm_norm = cm / div
	fix, axes = plt.subplots()
	cm_disp = ConfusionMatrixDisplay(cm_norm, display_labels = labels)
	cm_disp.plot(ax = axes, colorbar = False)
	plt.xticks(rotation = 'vertical')
	plt.xlabel('Predicted person')
	plt.ylabel('True person')
	plt.title(title)
	fix.tight_layout()

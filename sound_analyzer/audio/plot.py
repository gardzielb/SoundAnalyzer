from typing import Optional

import numpy as np


def plot_sound(
		axes, audio: np.ndarray, sample_rate: int, title: str,
		silence_ranges: Optional[list[tuple[int, int]]] = None
):
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

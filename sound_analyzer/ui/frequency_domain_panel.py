import numpy as np
from PyQt5.QtWidgets import QWidget


class FrequencyDomainPanel(QWidget):
	def __init__(self):
		super().__init__()

	def set_audio(self, audio: np.ndarray, sample_rate: int):
		print(f'Freq domain audio set, shape = {audio.shape}, sample rate = {sample_rate}')

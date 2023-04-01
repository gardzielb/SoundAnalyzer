from pathlib import Path

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy


class AudioInfoPanel(QWidget):
	def __init__(self):
		super().__init__()

		self.audio_info_label = QLabel('No audio loaded')
		self.audio_info_label.setFont(QFont('Serif', 12))
		self.load_audio_button = QPushButton('Load audio')
		self.load_audio_button.setFont(QFont('Serif', 12))
		self.load_audio_button.setMinimumSize(200, 40)

		layout = QHBoxLayout()
		layout.addWidget(self.audio_info_label)
		layout.addItem(QSpacerItem(1000, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
		layout.addWidget(self.load_audio_button)
		self.setLayout(layout)

	def set_audio(self, path: str, sample_rate: int):
		audio_name = Path(path).stem
		self.audio_info_label.setText(f'Track: {audio_name}, sample rate: {sample_rate}')

from typing import Optional

import numpy as np
import soundfile as sf
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QFileDialog, QTabWidget

from sound_analyzer.ui.audio_info_panel import AudioInfoPanel
from sound_analyzer.ui.frequency_domain_panel import FrequencyDomainPanel
from sound_analyzer.ui.time_domain_panel import TimeDomainPanel


class AppWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.audio: Optional[np.ndarray] = None
		self.sample_rate: Optional[int] = None

		self.audio_info_panel = AudioInfoPanel()
		self.tab_widget = QTabWidget()
		self.time_domain_panel = TimeDomainPanel()
		self.freq_domain_panel = FrequencyDomainPanel()

		layout = QVBoxLayout()
		layout.addWidget(self.audio_info_panel)
		layout.addWidget(self.tab_widget)

		central_widget = QWidget()
		central_widget.setLayout(layout)
		self.setCentralWidget(central_widget)

		self.audio_info_panel.load_audio_button.clicked.connect(self.open_file_dialog)
		self.tab_widget.setFont(QFont('Serif', 12))
		self.tab_widget.addTab(self.time_domain_panel, 'Time domain')
		self.tab_widget.addTab(self.freq_domain_panel, 'Frequency domain')
		self.tab_widget.currentChanged.connect(self.__on_tab_changed__)

	def load_audio(self, path: str):
		self.audio, self.sample_rate = sf.read(path)
		self.audio_info_panel.set_audio(path, self.sample_rate)
		self.tab_widget.currentWidget().set_audio(self.audio, self.sample_rate)

	def open_file_dialog(self):
		audio_path, _ = QFileDialog.getOpenFileName(self, 'Load audio', '*.wav', 'WAV files')
		if audio_path:
			self.load_audio(audio_path)

	def __on_tab_changed__(self):
		if self.audio is not None and self.sample_rate is not None:
			self.tab_widget.currentWidget().set_audio(self.audio, self.sample_rate)

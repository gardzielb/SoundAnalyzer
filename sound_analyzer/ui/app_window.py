from typing import Optional

import numpy as np
import soundfile as sf
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QFileDialog

from sound_analyzer.ui.audio_control_panel import AudioControlPanel
from sound_analyzer.ui.audio_info_panel import AudioInfoPanel
from sound_analyzer.ui.figure_widget import FigureWidget
from sound_analyzer.audio.frame_level_features import extract_volume, extract_ste, audio_to_frames, extract_zcr, \
	detect_silence_ranges


class AppWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.audio: Optional[np.ndarray] = None
		self.sample_rate: Optional[int] = None

		self.audio_info_panel = AudioInfoPanel()
		self.audio_ctl_panel = AudioControlPanel()
		self.figure = FigureWidget(n_plots = 4)

		layout = QVBoxLayout()
		layout.addWidget(self.audio_info_panel)
		layout.addWidget(self.audio_ctl_panel)
		layout.addWidget(self.figure)

		central_widget = QWidget()
		central_widget.setLayout(layout)

		self.audio_info_panel.load_audio_button.clicked.connect(self.open_file_dialog)
		self.audio_ctl_panel.frame_len_slider.add_observer(self.on_frame_len_change)
		self.audio_ctl_panel.silence_threshold_vol_slider.add_observer(self.on_silence_threshold_vol_change)
		self.audio_ctl_panel.silence_threshold_zcr_slider.add_observer(self.on_silence_threshold_zcr_change)

		self.setCentralWidget(central_widget)

		self.figure.add_plot(np.array([]), 1, title = 'Signal', silence_ranges = [])
		self.figure.add_plot(np.array([]), 1, title = 'Volume', silence_ranges = [])
		self.figure.add_plot(np.array([]), 1, title = 'STE', silence_ranges = [])
		self.figure.add_plot(np.array([]), 1, title = 'ZCR', silence_ranges = [])
		self.figure.show_plots()

	def load_audio(self, path: str):
		self.audio, self.sample_rate = sf.read(path)
		self.audio_info_panel.set_audio(path, self.sample_rate)
		self.__update_plots__()

	def open_file_dialog(self):
		audio_path, _ = QFileDialog.getOpenFileName(self, 'Load audio', '*.wav', 'WAV files')
		if audio_path:
			self.load_audio(audio_path)

	def on_frame_len_change(self, frame_len: float):
		self.__update_plots__(frame_len_ms = int(frame_len))

	def on_silence_threshold_vol_change(self, silence_threshold_vol: int):
		self.__update_plots__(silence_vol_threshold = silence_threshold_vol)

	def on_silence_threshold_zcr_change(self, silence_threshold_zcr: int):
		self.__update_plots__(silence_zcr_threshold = silence_threshold_zcr)

	def __update_plots__(
			self, frame_len_ms: Optional[int] = None,
			silence_vol_threshold: Optional[float] = None,
			silence_zcr_threshold: Optional[float] = None
	):
		if self.audio is None or self.sample_rate is None:
			return

		if frame_len_ms is None:
			frame_len_ms = int(self.audio_ctl_panel.frame_len_slider.value())

		if silence_vol_threshold is None:
			silence_vol_threshold = self.audio_ctl_panel.silence_threshold_vol_slider.value()

		if silence_zcr_threshold is None:
			silence_zcr_threshold = self.audio_ctl_panel.silence_threshold_zcr_slider.value()

		if frame_len_ms is None:
			frame_len_ms = int(self.audio_ctl_panel.frame_len_slider.value())

		audio_frames, samples_per_frame = audio_to_frames(self.audio, self.sample_rate, frame_len_ms)
		vol = extract_volume(audio_frames, samples_per_frame)
		ste = extract_ste(audio_frames, samples_per_frame)
		zcr = extract_zcr(audio_frames, samples_per_frame)
		silences = detect_silence_ranges(
			audio_frames, samples_per_frame,
			vol_threshold = silence_vol_threshold,
			zcr_threshold = silence_zcr_threshold
		)

		self.figure.reset()
		self.figure.add_plot(self.audio, self.sample_rate, title = 'Signal', silence_ranges = silences)
		self.figure.add_plot(vol, self.sample_rate, title = 'Volume', silence_ranges = silences)
		self.figure.add_plot(ste, self.sample_rate, title = 'STE', silence_ranges = silences)
		self.figure.add_plot(zcr, self.sample_rate, title = 'ZCR', silence_ranges = silences)
		self.figure.show_plots()

from typing import Callable

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QSlider, QGridLayout, QLabel, QHBoxLayout


class SmartSlider(QWidget):
	def __init__(self, parent, min_val: float, max_val: float, step: float):
		super().__init__()

		self.observers = []
		self.scaler = step

		self.slider = QSlider(Qt.Orientation.Horizontal, parent)
		self.slider.setRange(int(min_val / step), int(max_val / step))
		self.slider.valueChanged.connect(self.__on_value_changed__)

		layout = QHBoxLayout()
		layout.addWidget(self.slider)
		self.setLayout(layout)

	def add_observer(self, callback: Callable[[float], None]):
		self.observers.append(callback)

	def value(self) -> float:
		return self.slider.value() * self.scaler

	def __on_value_changed__(self, value: int):
		for callback in self.observers:
			callback(value * self.scaler)


class AudioControlPanel(QWidget):
	def __init__(self):
		super().__init__()

		self.frame_len_slider = SmartSlider(self, min_val = 10, max_val = 40, step = 5)
		self.silence_threshold_vol_slider = SmartSlider(self, min_val = 0.0, max_val = 0.2, step = 0.01)
		self.silence_threshold_zcr_slider = SmartSlider(self, min_val = 0.0, max_val = 0.2, step = 0.01)

		self.frame_len_label = self.__create_label__(text = str(self.frame_len_slider.value()))
		self.silence_threshold_vol_label = self.__create_label__(text = str(self.silence_threshold_vol_slider.value()))
		self.silence_threshold_zcr_label = self.__create_label__(text = str(self.silence_threshold_zcr_slider.value()))

		self.frame_len_slider.add_observer(self.__on_frame_len_changed__)
		self.silence_threshold_vol_slider.add_observer(self.__on_silence_threshold_vol_changed__)
		self.silence_threshold_zcr_slider.add_observer(self.__on_silence_threshold_zcr_changed__)

		layout = QGridLayout()
		layout.setHorizontalSpacing(20)

		layout.addWidget(self.__create_label__('Frame length [ms]'), 0, 0)
		layout.addWidget(self.frame_len_label, 0, 1)
		layout.addWidget(self.frame_len_slider, 1, 0, 1, 2)
		layout.addWidget(self.__create_label__('Volume silence threshold'), 0, 2)
		layout.addWidget(self.silence_threshold_vol_label, 0, 3)
		layout.addWidget(self.silence_threshold_vol_slider, 1, 2, 1, 2)
		layout.addWidget(self.__create_label__('ZCR silence threshold'), 0, 4)
		layout.addWidget(self.silence_threshold_zcr_label, 0, 5)
		layout.addWidget(self.silence_threshold_zcr_slider, 1, 4, 1, 2)

		self.setLayout(layout)

	def __create_label__(self, text: str, font_size: int = 11) -> QLabel:
		label = QLabel(text, self)
		label.setFont(QFont('Serif', font_size))
		return label

	def __on_frame_len_changed__(self, frame_len):
		self.frame_len_label.setText(str(frame_len))

	def __on_silence_threshold_vol_changed__(self, silence_threshold_vol):
		self.silence_threshold_vol_label.setText(str(round(silence_threshold_vol, ndigits = 2)))

	def __on_silence_threshold_zcr_changed__(self, silence_threshold_zcr):
		self.silence_threshold_zcr_label.setText(str(round(silence_threshold_zcr, ndigits = 2)))

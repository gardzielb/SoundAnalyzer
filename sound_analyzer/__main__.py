from PyQt5.QtWidgets import QApplication

from sound_analyzer.ui.app_window import AppWindow

if __name__ == '__main__':
	app = QApplication([])
	# app.setStyle("Fusion")

	app_window = AppWindow()
	app_window.setWindowTitle('Sound analyzer')
	app_window.show()

	app.exec_()

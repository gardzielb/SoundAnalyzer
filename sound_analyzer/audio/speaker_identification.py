from math import ceil
from pathlib import Path

import numpy as np
import pandas as pd
import soundfile as sf
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC

from sound_analyzer.audio.mfcc import pre_emphasis, frame_and_window, create_filter_bank, calculate_mfcc
from sound_analyzer.audio.plot import plot_confusion_matrix, plot_sound, plot_filter_bank
from sound_analyzer.audio.util import pad_audio


def extract_mfcc(
		path: str | Path, frame_len_ms = 40, frame_overlap_ms = 10,
		n_filters = 20, include_energy = False, n_samples = None, show_plots = False
) -> np.ndarray:
	path = Path(path)
	audio, sample_rate = sf.read(path)
	audio = pad_audio(audio, target_n_samples = sample_rate if n_samples is None else n_samples)
	emphasised_audio = pre_emphasis(audio)
	hamming_frames = frame_and_window(audio, sample_rate, frame_len_ms, frame_overlap_ms)
	power_spectrum = np.abs(np.fft.rfft(hamming_frames)) ** 2
	filter_bank = create_filter_bank(sample_rate, nfft = power_spectrum.shape[1], n_filters = n_filters)

	if show_plots:
		plot_sound(audio, sample_rate, title = path.stem)
		plot_sound(emphasised_audio, sample_rate, title = f'Emphasised {path.stem}')
		plot_filter_bank(filter_bank, sample_rate)

	mfcc = calculate_mfcc(power_spectrum, filter_bank)
	if include_energy:
		frame_sq = hamming_frames ** 2
		energy = np.log10(np.sum(frame_sq, axis = 1, keepdims = True))
		mfcc = np.append(mfcc, energy, axis = 1)

	return mfcc


def test_models(x_train, x_test, y_train, y_test, labels):
	models = [
		(RandomForestClassifier(n_jobs = 12), 'Random forest'),
		(SVC(), 'SVM'),
		(MLPClassifier(), 'MLP')
	]

	for model, name in models:
		print(f'Training and testing {name}...')
		model.fit(x_train, y_train)
		pred = model.predict(x_test)
		accuracy = accuracy_score(y_test, pred)
		print(f'{name} accuracy = {accuracy}')
		plot_confusion_matrix(y_test, pred, labels = labels, title = f'{name}: accuracy {accuracy:0.2f}')


def split_dataset(
		dataset: pd.DataFrame, features: pd.DataFrame, method: str | None = None
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
	if method == 'separate':
		test_words = ['zero', 'jeden', 'dwa', 'trzy', 'cztery', 'siedem', 'osiem']
		test_idx = dataset['content'].isin(test_words)
		x_train = features[~test_idx]
		x_test = features[test_idx]
		y_train = dataset.loc[~test_idx, 'speaker']
		y_test = dataset.loc[test_idx, 'speaker']
		return x_train, x_test, y_train, y_test

	if method == 'shared':
		speakers = list(dataset['speaker'].unique())
		n_speaker_test_samples = ceil(0.2 * len(dataset) / len(speakers))
		test_idx = pd.Series(data = [False] * len(dataset))

		for speaker in speakers:
			speaker_test_idx = (dataset['speaker'] == speaker) & (dataset['path'].str.contains('_2'))
			test_idx |= speaker_test_idx[speaker_test_idx].sample(n_speaker_test_samples)

		x_train = features[~test_idx]
		x_test = features[test_idx]
		y_train = dataset.loc[~test_idx, 'speaker']
		y_test = dataset.loc[test_idx, 'speaker']
		return x_train, x_test, y_train, y_test

	return train_test_split(features, dataset['speaker'], test_size = 0.2)

import numpy as np
from scipy.fftpack import dct

from sound_analyzer.audio.frame_level_features import audio_to_frames


def pre_emphasis(signal: np.ndarray, alpha = 0.97) -> np.ndarray:
	return np.append(signal[0], signal[1:] - alpha * signal[:-1])


def frame_and_window(signal: np.ndarray, sample_rate: int, frame_len_ms: int, frame_overlap_ms = 0) -> np.ndarray:
	frames, samples_per_frame = audio_to_frames(signal, sample_rate, frame_len_ms, frame_overlap_ms)
	return frames * np.hamming(samples_per_frame)


def hz_to_mel(hz: float | np.ndarray) -> float | np.ndarray:
	return 2595 * np.log10(1 + hz / 700)


def mel_to_hz(mel: float | np.ndarray) -> float | np.ndarray:
	return 700 * (10 ** (mel / 2595) - 1)


def create_filter_bank(sample_rate: int, nfft: int, n_filters = 20):
	f_min_mel = 0
	f_max_mel = hz_to_mel(sample_rate / 2)

	mel_pts = np.linspace(f_min_mel, f_max_mel, num = n_filters + 2)
	hz_pts = mel_to_hz(mel_pts)
	fft_bins = np.floor((nfft + 1) * hz_pts / sample_rate).astype(int)

	filter_bank = np.zeros((n_filters, nfft))
	for m in range(1, n_filters + 1):
		for k in range(fft_bins[m - 1], fft_bins[m]):
			filter_bank[m - 1, k] = (k - fft_bins[m - 1]) / (fft_bins[m] - fft_bins[m - 1])
		for k in range(fft_bins[m], fft_bins[m + 1] + 1):
			filter_bank[m - 1, k] = (fft_bins[m + 1] - k) / (fft_bins[m + 1] - fft_bins[m])

	return filter_bank


def calculate_mfcc(power_spectrum: np.ndarray, filter_bank: np.ndarray) -> np.ndarray:
	frames_energies = np.log10(np.dot(power_spectrum, filter_bank.T))
	return dct(frames_energies, type = 2, axis = 1, norm = 'ortho')

import numpy as np


def audio_to_frames(audio: np.ndarray, sample_rate: int, frame_len_ms: int) -> tuple[np.ndarray, int]:
	samples_per_frame = int(frame_len_ms * sample_rate / 1000)
	last_idx = (audio.shape[0] // samples_per_frame) * samples_per_frame
	frames = audio[:last_idx].reshape(-1, samples_per_frame)
	return frames, samples_per_frame


def extract_frames_ste(audio_frames: np.ndarray, samples_per_frame: int) -> np.ndarray:
	audio_frames_sq = audio_frames ** 2
	return audio_frames_sq.sum(axis = 1, keepdims = True) / samples_per_frame


def extract_frames_volume(audio_frames: np.ndarray, samples_per_frame: int) -> np.ndarray:
	ste = extract_frames_ste(audio_frames, samples_per_frame)
	return np.sqrt(ste)


def extract_frames_zcr(audio_frames: np.ndarray, samples_per_frame: int) -> np.ndarray:
	sign = np.sign(audio_frames)
	sign_diff = np.abs(sign[:, 1:] - sign[:, :-1])
	return sign_diff.sum(axis = 1, keepdims = True) / (2 * samples_per_frame)


def extract_volume(audio_frames: np.ndarray, samples_per_frame: int) -> np.ndarray:
	ste = extract_ste(audio_frames, samples_per_frame)
	return np.sqrt(ste)


def extract_ste(audio_frames: np.ndarray, samples_per_frame: int) -> np.ndarray:
	frames_ste = extract_frames_ste(audio_frames, samples_per_frame)
	ste = np.repeat(frames_ste, samples_per_frame, axis = 1)
	return ste.reshape(-1)


def extract_zcr(audio_frames: np.ndarray, samples_per_frame: int) -> np.ndarray:
	frames_zcr = extract_frames_zcr(audio_frames, samples_per_frame)
	zcr = np.repeat(frames_zcr, samples_per_frame, axis = 1)
	return zcr.reshape(-1)


def detect_silence_ranges(
		audio_frames: np.ndarray, samples_per_frame: int, vol_threshold: float, zcr_threshold: float
) -> list[tuple[int, int]]:
	volume = extract_frames_volume(audio_frames, samples_per_frame).reshape(-1)
	zcr = extract_frames_zcr(audio_frames, samples_per_frame).reshape(-1)
	silence = (volume < vol_threshold) & (zcr < zcr_threshold)

	silence_range_indices, = np.nonzero(np.r_[1, np.diff(silence)[:-1]])
	silence_ranges = []

	for i, idx in enumerate(silence_range_indices):
		if silence[idx]:
			end_idx = silence_range_indices[i + 1] if i + 1 < len(silence_range_indices) else silence.shape[0]
			silence_ranges.append((idx * samples_per_frame, end_idx * samples_per_frame))

	return silence_ranges

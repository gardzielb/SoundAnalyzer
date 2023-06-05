from pathlib import Path

import numpy as np
import soundfile as sf


def pad_audio(audio: np.ndarray, target_n_samples: int) -> np.ndarray:
	if target_n_samples <= len(audio):
		return audio[:target_n_samples]
	return np.append(audio, np.zeros(target_n_samples - len(audio)))


def track_info(path: Path) -> tuple[int, int]:
	sound, sr = sf.read(path)
	return len(sound), sr

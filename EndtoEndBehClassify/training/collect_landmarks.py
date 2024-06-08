"""
Landmark data collection.
"""
import os
import time
from typing import Sequence

import numpy as np

from noddingpigeon.video import Feature, video_to_landmarks
from noddingpigeon.config import Config
from noddingpigeon.model import load_landmarks


def collect_landmarks_with_webcam(
        labels: Sequence[str] = (Config.stationary_label,) + Config.gesture_labels,
        npz_path: str = Config.npz_filename,
        max_num_frames: int = 1600,
        sleep_seconds: float = 3.0,
        update_file: bool = True
) -> None:
    if os.path.isfile(npz_path) and update_file:
        landmark_dict = load_landmarks(npz_path)
    else:
        landmark_dict = {}

    for label in labels:
        landmark_dict[label] = video_to_landmarks(None, max_num_frames)
        time.sleep(sleep_seconds)

    feature_names = [f.name for f in Feature]
    np.savez_compressed(npz_path, feature_names=feature_names, **landmark_dict)


if __name__ == "__main__":
    collect_landmarks_with_webcam()

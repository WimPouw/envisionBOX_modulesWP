"""
Landmark data collection.
"""
import os
import time
from typing import Sequence
import importlib.util
import numpy as np
import glob

#from noddingpigeon.video import Feature, video_to_landmarks
from noddingpigeon.config import Config
#from noddingpigeon.model import load_landmarks

# import importlib.util
import sys
from pathlib import Path

import os

# load model and config locally
path_model = os.path.abspath('../noddingpigeon/modelfortraining.py')
path_config = os.path.abspath('../noddingpigeon/config.py')
path_video = os.path.abspath('../noddingpigeon/videofortraining.py')

spec_model = importlib.util.spec_from_file_location("model", path_model)
model_module = importlib.util.module_from_spec(spec_model)
sys.modules["model"] = model_module
spec_model.loader.exec_module(model_module)

spec_video = importlib.util.spec_from_file_location("video", path_video)
video_module = importlib.util.module_from_spec(spec_video)
sys.modules["video"] = video_module
spec_video.loader.exec_module(video_module)

spec_config = importlib.util.spec_from_file_location("Config", path_config)
config_module = importlib.util.module_from_spec(spec_config)
sys.modules["Config"] = config_module
spec_config.loader.exec_module(config_module)

# Use the imported functions and classes
Config = config_module.Config
load_landmarks = model_module.load_landmarks

# Use the imported functions and classes
Feature = video_module.Feature
video_to_landmarks = video_module.video_to_landmarks

def collect_landmarks_with_webcam(
        labels: Sequence[str] = (Config.stationary_label,) + Config.gesture_labels,
        npz_path: str = Config.npz_filename,
        max_num_frames: int = 800,
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
    
def collect_landmarks_from_videos(
    labels: Sequence[str] = (Config.stationary_label,) + Config.gesture_labels,
    npz_path: str = Config.npz_filename,
    max_num_frames: int = 1600,
    update_file: bool = True,
    videofol: str = os.path.abspath('../trainingvideos')
)  -> None:
    landmark_dict = {}
    for label in labels:
        print(label)
        print(videofol + '/' + label + '.mp4')
        # check how many videos there are that have the label in the filename using glob
        glob_list = glob.glob(videofol + '/' + label + '*.mp4')

        # first initialize the keys
        landmark_dict[label] = []
        
        # now add the landmarks for each video using extend
        for video in glob_list:
            print('processing video: ' + video)
            landmark_dict[label].extend(video_to_landmarks(video, max_num_frames))
        
    feature_names = [f.name for f in Feature]
    np.savez_compressed(npz_path, feature_names=feature_names, **landmark_dict)

if __name__ == "__main__":
    collect_landmarks_from_videos()

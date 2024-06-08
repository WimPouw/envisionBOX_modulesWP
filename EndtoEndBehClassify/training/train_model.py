"""
Train model for classifying landmark movements.
"""
import os
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import tensorflow as tf
from tensorflow.keras import losses
from tensorflow.keras.models import Model

#from noddingpigeon.config import Config
#from noddingpigeon.model import load_landmarks, make_model

import importlib.util
import sys

# load model and config locally
path_model = os.path.abspath('../noddingpigeon/modelfortraining.py')
path_config = os.path.abspath('../noddingpigeon/config.py')

spec_model = importlib.util.spec_from_file_location("model", path_model)
model_module = importlib.util.module_from_spec(spec_model)
sys.modules["model"] = model_module
spec_model.loader.exec_module(model_module)

spec_config = importlib.util.spec_from_file_location("Config", path_config)
config_module = importlib.util.module_from_spec(spec_config)
sys.modules["Config"] = config_module
spec_config.loader.exec_module(config_module)

# Use the imported functions and classes
Config = config_module.Config
make_model = model_module.make_model
load_landmarks = model_module.load_landmarks

tf.random.set_seed(0)

def setup_accelerators_and_get_strategy() -> tf.distribute.Strategy:
    os.environ["CUDA_VISIBLE_DEVICES"] = "0,1"
    gpu_devices = tf.config.list_physical_devices("GPU")
    if gpu_devices:
        # Strategy for GPU or multi-GPU machines.
        strategy = tf.distribute.MirroredStrategy()
        print(f"Number of accelerators: {strategy.num_replicas_in_sync}")
    else:
        strategy = tf.distribute.OneDeviceStrategy("/cpu:0")
        print("Using single CPU.")
    return strategy


def make_y(label_idx: int) -> List[int]:
    has_motion = 1 if label_idx > 0 else 0
    y = [has_motion] + [0] * len(Config.gesture_labels)
    if has_motion == 1:
        y[label_idx] = 1
    # Note:
    # Format of y is [has_motion, <one-hot-gesture-class-vector>], e.g.,
    # [1, 0, 1, ..., 0] for the 2nd gesture,
    # [0, ..., 0] for stationary case.
    return y


def make_ds_train(
        landmark_dict: Dict[str, Sequence[Sequence[float]]],
        seq_length: int,
        num_features: int,
        seed: int
) -> tf.data.Dataset:
    # Note: stationary label must come first in this design, see make_y.
    labels = (Config.stationary_label,) + Config.gesture_labels
    rng = np.random.default_rng(seed=seed)

    def gen() -> Tuple[List[List[float]], int]:
        while True:
            label_idx = int(rng.integers(len(labels), size=1))
            landmarks = landmark_dict[labels[label_idx]]
            seq_idx = int(rng.integers(len(landmarks) - seq_length, size=1))
            features = landmarks[seq_idx: seq_idx + seq_length]
            yield features, make_y(label_idx)

    return tf.data.Dataset.from_generator(
        gen,
        output_signature=(
            tf.TensorSpec(shape=(seq_length, num_features), dtype=tf.float32),
            tf.TensorSpec(shape=(len(labels),), dtype=tf.int32)
        )
    )


def loss(y_true: tf.Tensor, y_pred: tf.Tensor) -> tf.Tensor:
    has_motion_true = y_true[:, :1]
    has_motion_pred = y_pred[:, :1]
    has_motion_loss = losses.BinaryCrossentropy(
        reduction=tf.keras.losses.Reduction.NONE
    )(has_motion_true, has_motion_pred)

    # The gesture loss is designed in the way that, if has_motion is 0,
    # the box values do not matter.
    mask = y_true[:, 0] == 1
    weight = tf.where(mask, 1.0, 0.0)
    gesture_true = y_true[:, 1:]
    gesture_pred = y_pred[:, 1:]
    gesture_loss = losses.CategoricalCrossentropy(
        label_smoothing=0.05,
        reduction=tf.keras.losses.Reduction.NONE
    )(gesture_true, gesture_pred, sample_weight=weight)

    return (has_motion_loss + gesture_loss) * 0.5


class CustomAccuracy(tf.keras.metrics.Metric):

    def __init__(
            self,
            motion_threshold: float = 0.5,
            gesture_threshold: float = 0.9,
            name: str = "custom_accuracy"
    ) -> None:
        super(CustomAccuracy, self).__init__(name=name)
        self.motion_threshold = motion_threshold
        self.gesture_threshold = gesture_threshold
        self.acc = tf.keras.metrics.CategoricalAccuracy()

    def update_state(
            self,
            y_true: tf.Tensor,
            y_pred: tf.Tensor,
            sample_weight: Optional[tf.Tensor] = None
    ) -> None:
        # IMPORTANT - the sample_weight parameter is needed to solve:
        # TypeError: tf__update_state() got an unexpected keyword argument 'sample_weight'
        y_pred = tf.where(y_pred[:, :1] >= self.motion_threshold, y_pred, 0.0)
        y_pred = tf.where(y_pred >= self.gesture_threshold, 1.0, 0.0)
        self.acc.update_state(y_true[:, 1:], y_pred[:, 1:])

    def result(self) -> tf.Tensor:
        return self.acc.result()

    def reset_state(self) -> None:
        self.acc.reset_state()


def compile_model(model: Model) -> None:
    model.compile(
        loss=loss,
        optimizer=tf.keras.optimizers.Adam(amsgrad=True),
        metrics=[CustomAccuracy()],
    )


def get_steps_per_epoch(
        landmark_dict: Dict[str, Sequence[Sequence[float]]]
) -> int:
    # Kind of arbitrary here.
    mean_data_size = int(np.mean([len(v) for v in landmark_dict.values()]))
    steps_per_epoch = int(mean_data_size * 0.7)
    return steps_per_epoch


def train_and_save_weights(
        landmark_dict: Dict[str, List[List[float]]],
        model: Model,
        weights_path: str,
        seed: int = 42
) -> None:
    ds_train = make_ds_train(
        landmark_dict, Config.seq_length, Config.num_original_features, seed
    )
    ds_train = ds_train.batch(16).prefetch(tf.data.AUTOTUNE)

    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(
            filepath=weights_path, monitor="loss", mode="min",
            save_best_only=True, save_weights_only=True, verbose=1
        ),
        tf.keras.callbacks.EarlyStopping(
            monitor="loss", min_delta=1e-04, patience=10,
            restore_best_weights=True, verbose=1
        ),
    ]
    model.fit(
        ds_train,
        epochs=500,
        steps_per_epoch=get_steps_per_epoch(landmark_dict),
        callbacks=callbacks,
        verbose=1,
    )


def main() -> None:
    strategy = setup_accelerators_and_get_strategy()
    with strategy.scope():
        model = make_model(weights_path=None)
        compile_model(model)
    landmark_dict = load_landmarks(Config.npz_filename)
    try:
        train_and_save_weights(landmark_dict, model, Config.weights_filename)
    except KeyboardInterrupt:
        print("Training interrupted.")


if __name__ == "__main__":
    main()

# How to perform 3D tracking using 3 webcams (anipose + deeplabcut pretrained)

# Contact
wim.pouw@donders.ru.nl

# Background

Here there is a example code and data to infer from three webcams capturing 2D data the 3D pose data. We do this first by finding the angles between the cameras using anipose and three synced videos of a charucoboard (see below). Then we run deeplabcut pre-trained human model on each of the three test videos where someone is doing silly movements. Having the deeplabcut output, we use this as input for the second stage of anipose, which is a triangulation of the 2D data to 3D given the information of the calibration of the cameras.

While we largely follow the anipose materials (https://anipose.readthedocs.io/en/latest/aniposelib-tutorial.html) it still took some time to get going due to several reasons (e.g., opencv has been updated and is not compatible with anipose anymore if we use a charucoboard; there is no test data that one can use) and therefore this module provides hopefully a easier way to try it out with your own data.

Make sure you install the requirements.txt for running this module (pip install -r requirements.txt).
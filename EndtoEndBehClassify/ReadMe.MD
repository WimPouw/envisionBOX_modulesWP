# End-to-End Human Behavioral Classification Using Convulational Neural Networks

<br>
<div align="center">Wim Pouw (wim.pouw@donders.ru.nl)</div>

<img src="Images/envision_banner.png" alt="isolated" width="300"/>

<img src="Images/example_1_auto_annotated_1.gif" alt="isolated" width="300"/>

## Info
The current code allows you to train your own labeled videos, train a convolutional neural network that takes in body, hand, and face features from mediapipe holistic, and outputs behavioral classifications. Then you can apply the CNN to classify new videos with annotated data saved to csv's and the videos labeled for checking. Convolutional neural networks are great for classifying patterns in spatial and temporal data patterns. In this case we use CNN's to take a bunch of features of hand,body,face and to detect certain behaviors. To summarize, this code does the following:

* extract features with Mediapipe Holistic for training and inference
* train a CNN based on labels of the training data 'trainingvideos' folder
* loop over video snippets produce inferences on new videos in the 'videos_to_label' folder
* save the labeled videos and automatic annotations (in csvs) to the output folder

To code your own behaviors. Just change the gesture in the config code chunk below, and make sure that your training videos start with the name of the label. I advice that the videos are minimally as long as your window of inference (here 25 frames).

* location current Repository: https://github.com/WimPouw/envisionBOX_modulesWP/EndtoEndBehClassify/

* location Jupyter notebook: https://github.com/WimPouw/envisionBOX_modulesWP/EndToEndBehClassify/HumanBehavioralClassificationEndtoEnd.ipynb


### Some further background
I think there is currently a lack of easily usable computer vision pipelines that can allow you to do some automatic behavioral coding based on your own training data. A computer scientist might feel much more comfortable to adapt code for their usecase, but social scientists need a little bit more of a plug-and-play approach, and might benefit from a linear presentation as is provided here, in this notebook.

Importantly, I am not a computer scientist, and I do not know the intricacies of convolutional neural networks and how to let them perform at the state of the art as you would expect from computer scientists. However, that does not mean that we can use these tools and assess ourselves whether they can be helpful for us by looking at annotator agreement between machine and some hand-labeled data. If it works, and we can verify that it works, then we can use it. In parrelel of course we can all work more to become more literate in machine learning if we want to make use of it more responsibly.

## Current code
The basic routine overviewed here is mostly from the NoddingPigeon code provided here: https://github.com/bhky/nodding-pigeon/. I have adapted it quite a bit, to make it more versatile for recognition of other types of gestures, and made the code completely linear, so that it is usable end-to-end. I have modified the following things:

* instead of only taking simple features from a different 2d head mediapipe into account, we take the richer information of mediapipe holistic to get body, head, and hand information
* I have added head rotations derived from mediapipe as they are important for head nodding and turning
* I made the CNN model a bit more complex with more layers (i.e., a deeper network), to account for the more complex feature set, and added regularization and maxpooling (which should help with overfitting issues)
* further I have made the code such that you just run it from beginning to end, adapting a good bit to accomodate the linear working style that we use for envisionBOX

Please feel free to help out and improve the code. I will change the names in the citation of this module accordingly if you like. The current dataset is quite small, but I was still impressed with the accuracy for the three gestures, so im curious to know with more data how it performs on other types of data (see concluding remarks at the end).

## Installation
pip install -r requirements.txt

But note, if you want install tensorflow with gpu, you need to have cuda etc installed. Not necessary however.

## citation for the current pipeline
Pouw, W. (2024). End-to-End Human Behavioral Classification Using Convolutional Neural Networks [the day you viewed the site]. Retrieved from: https://github.com/WimPouw/envisionBOX_modulesWP/EndToEndBehClassify/

## citation for the noddingpigeon
Nodding-Pigeon. Nodding-Pigeon, (2013), GitHub repository, https://github.com/bhky/nodding-pigeon/

### Citation for Mediapipe
citation: Lugaresi, C., Tang, J., Nash, H., McClanahan, C., Uboweja, E., Hays, M., ... & Grundmann, M. (2019). Mediapipe: A framework for building perception pipelines. arXiv preprint arXiv:1906.08172.
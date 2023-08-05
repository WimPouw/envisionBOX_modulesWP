# Dynamic data dashboard
In multimodal communication research we often face the challenge of showing general statistical patterns and pointing back to the real phenomenon that often consist of audiovisual information. This is not always done, and this means that we often only report general statistical patterns without helping readers understand how it relates to the there-and-then of the data that supported your analyses. Data dashboards allow for integrating the large-scale statistical patterns with the individual audiovisual events (and much more), and this is a reason I believe we should be using this more in our future research. Here a simple example of a app is presented that can be easily modified or reused with your data. Have fun!

## How to run the app yourself
The app.py contains the code for running a python Dash plotly application (app) on your local server. If you run the script in python, it will print a local server address that you can paste in your browser. 

## Input app
The application by default will look in the assets folder to grab files or styles (reset.css). So here is were your static or audiovisual data lives. In the case of this app the input is a dataset with x, y, coordinates of gestures in a kinematic space and the associated videos, plus the videos themselves. In the app they are then linked and presented concurrently. 

## Aesthetics of the app
Part of the app is handled by the reset.css file in the assets folder. This allows you to change font type etc, or set font schemes for different headings, like you with with any website.

## Launching it online?
If you want to launch the app so that other people can access it from the web, you need to host it on a server dedicated to running applications like this. This app has been launched on a Radboud University server (https://tsg-131-174-75-200.hosting.ru.nl/dynamicvisualizer/) that uses Apache2 (a commonly used interface for implementing apps on a server). If your university or institution does not provide this service, another option is to launch it on a commercial server, like heroku.

## Want to learn more?
There are really helpful tutorials to get started with data dashboards. I found @CharmingData youtuber really helpful and I recommend it (https://www.youtube.com/@CharmingData). He also goes into launching applications on Heroku.

# Feel free to reach out with questions
wim.pouw@donders.ru.nl

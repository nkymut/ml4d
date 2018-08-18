# ml4d: machine learning for design


![](https://d2mxuefqeaa7sj.cloudfront.net/s_9842357C3BAF1E4621B39662A8FD188EB03D41C268175FE55C053D8FF415A3A6_1534595007503_Scanbinet-03.jpg)


ml4d: machine learning for design is a design platform module conducted by @nkymut at the [Division of Industrial Design SDE NUS](http://did.nus.edu.sg/) during the 2017/2018 semester. Students have
design&built interactive hardware prototypes to explore how the latest machine learning technologies can serve as a design tool to improve our of life.

The concept of the platform was inspired by [The Wekinator](http://www.wekinator.org/) and [Machine Learning for Musicians and Artists](https://www.kadenze.com/courses/machine-learning-for-musicians-and-artists/info) by Dr. Rebecca Fiebrink and [ml4a](http://ml4a.github.io/) by Gene Kogan.
 
This repository contains a collection of sample codes used during the platform. 
The codes are written in Python using cross-platform modules to enable seamless development between both Windows/Mac and Raspberry Pi. This feature allows rapid-prototyping of an interactive system using machine learning techniques.


![](https://d2mxuefqeaa7sj.cloudfront.net/s_9842357C3BAF1E4621B39662A8FD188EB03D41C268175FE55C053D8FF415A3A6_1534595007444_collectiveStories.jpg)
![](https://d2mxuefqeaa7sj.cloudfront.net/s_9842357C3BAF1E4621B39662A8FD188EB03D41C268175FE55C053D8FF415A3A6_1534595007401_detector.jpg)
![](https://d2mxuefqeaa7sj.cloudfront.net/s_9842357C3BAF1E4621B39662A8FD188EB03D41C268175FE55C053D8FF415A3A6_1534595007331_scanbinet.jpg)

## Requirements
----------
1. Python 3.6
2. RaspberryPi 2 or newer ([Raspbian Stretch](https://www.raspberrypi.org/downloads/raspbian/)) 
3. OpenCV
4. pyglet
5. pyFirmata


## Installation
----------


1. Install Python 3.6
  - [Win/Mac] Anaconda [https://anaconda.org/](https://www.anaconda.com/download/)download/
  - [Raspberry Pi] `sudo apt-get install python3.6` 
2. Install pyglet, python-osc, opencv-python, pyserial, pyFirmata modules. 

[Win/Mac] start Anaconda Prompt and 

    pip install pyglet python-osc opencv-python pyserial pyfirmata

[Raspberry Pi]

    sudo pip3 install pyglet python-osc opencv-python pyserial pyfirmata
3. Download the repository.

[Win/Mac]

    git clone https://github.com/nkymut/ml4d.git
    cd ml4d/week1_pyglet
    python 01helloWorld.py

[Raspberry Pi]

    git clone https://github.com/nkymut/ml4d.git
    cd ml4d/week1_pyglet
    python3 01helloWorld.py
![](https://d2mxuefqeaa7sj.cloudfront.net/s_9842357C3BAF1E4621B39662A8FD188EB03D41C268175FE55C053D8FF415A3A6_1534594423320_image.png)

## ToDo:
----------
- More detailed instructions 
- Face Recognition with dlib https://github.com/davisking/dlib
- Object Recognition with pytorch-yolo-v3 https://github.com/ayooshkathuria/pytorch-yolo-v3
## References
----------

ml4a: http://ml4a.github.io/
Kadenze Machine Learning for Musicians and Artists: https://www.kadenze.com/courses/machine-learning-for-musicians-and-artists Wekinator: http://www.wekinator.org/
pyglet: [https://bitbucket.org/pyglet/pyglet/wiki/Home](https://bitbucket.org/pyglet/pyglet/wiki/Home)
python-osc: https://github.com/attwad/python-osc
pyfirmata: https://github.com/tino/pyFirmata


## Image Credits
----------

These files are licensed under the [Creative Commons](https://en.wikipedia.org/wiki/en:Creative_Commons) [Attribution-Share Alike 3.0 Unported](https://creativecommons.org/licenses/by-sa/3.0/deed.en) license.
([rock.jpg](https://commons.wikimedia.org/wiki/File:Rock-paper-scissors_(rock).png), [paper.jpg](https://commons.wikimedia.org/wiki/File:Rock-paper-scissors_(paper).png), [scissors.jpg](https://commons.wikimedia.org/wiki/File:Rock-paper-scissors_(scissors).png)): Author: [Sertion](https://commons.wikimedia.org/wiki/User:Sertion) 


# Bachelor-thesis
# Author: Minnich Marian-Alin
# Date: 22.06.2020
This repository contains an application that detects facial expressions and trigger some actions based on a sequence of expressions

The application can be found on BetaApplication directory and it represents my work for my bachelor thesis. This application detects 
5 facial expressions (Angry, Sad, Surprise, Happy and Neutral) and trigger some actions based on a sequence of these expressions.

For example: you can execute an expression that represents an emotion, let's say Angry and after that you will execute another expression, 
like Surprise. After the execution of these two expressions, you will execute a final expression (the third expression) which is Angry.
This combination of expressions will trigger an action, which is in this case, the opening of a web page (Youtube in this case) in your main browser.

Of course, the application will "help" you to execute these sequences of expressions through an application interface. Unfortunately, this
version of application supports only Romanian language (code documentation it's also in Romanian), but as soon as I can I will create 
a version that will support English as well.


The main purpose of this application is to inspire other people to work on this project, because this application has the potential to help 
people in need (people who can't move, persons without hands, or deaf persons) to control and use a computer/laptop/almost anything.

Also, the application can detect emotions because of a trained model (convolutional neural network, CNN), that can be found at path: Bachelor-thesis/EmotionModel/EmotionDetectorModel.h5.
This CNN was developed using Keras and trained through Colab platform. The code for this model can be found at path: Bachelor-thesis/CNN_EmotionDetector.py

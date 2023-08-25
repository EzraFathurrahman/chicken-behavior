# Chicken Behavior Analyzer Web Application

## Introduction

Chicken Behavior Analyzer is a web application created to track and analyze the behavior of chickens from an inserted video. 
It is designed as a bachelor thesis final project and serves as proof of concept for the researcher in IPB University Faculty of Animal Science. 
There are two main detection features on this website:
1. Chicken aggressivity detection
2. Chicken movement anomaly detection

## Development Environment
- Text Editor: Visual Studio Code
- Operating System: Windows 11
- Programming Language: Python, HTML, CSS, Javascript
- Framework: Flask

## Chicken Aggressivity Detection
This feature is a solution provided to answer one of the animal welfare challenge which is to detect chicken aggressive behavior and helping the cattleman to supervise the chicken by preventing them from hurting each other.

This feature implement YOLOv4 algorithm and loading the models which are the weight, config, and labels then processing video input through them, the output of this feature is labeled video and short analysis about it.

## Chicken Movement Anomaly Detection
The purpose of this feature is to detect whether a chicken with an anomaly exist in the inserted video. 
This feature integrates MobileNet-SSD object detection algorithm with Isolation Forest anomaly detection algorithm. 

A chicken is classified as an anomaly if the chicken rarely moves and usually stays in one place, unlike the other chickens.
The cause of this chicken laziness is too much feeding.
Too much feeding results in their leg muscle weight increase, making them harder to move to reach foods and other nutrients.
This cause the chicken to be easily sick and sometimes die, causing an increase in cost and potential loss in the poultry industry.

Through surveillance of chickens in their coop, the breeder needs only to insert a chicken surveillance video to this web, 
and it will show chickens that are potentially sick. 
The steps are as follows:

1. Open the chicken behavior analyzer web.
![image](https://github.com/EzraFathurrahman/chicken-behavior/assets/63547189/fb8614af-851f-4cad-b374-e58121bf1c57)


2. Choose Anomaly Behavior from the left side menu, or Detect Chicken Movement Anomaly Button
![image](https://github.com/EzraFathurrahman/chicken-behavior/assets/63547189/44060277-76c9-4c60-a98c-c57a8096c505)


3. Insert the chicken surveillance video by pressing Upload Video button or drag a video. Make sure the format is in MP4.
![image](https://github.com/EzraFathurrahman/chicken-behavior/assets/63547189/ec246408-22a7-4b7e-abc9-8e6a56a6ea16)


4. Press the Run Detector button. Wait for the web to process the video.
![image](https://github.com/EzraFathurrahman/chicken-behavior/assets/63547189/15e10309-24ce-4fa2-af98-053d13e37098)


5. The are three results from the video processing. Those outputs are

- Video with ID attached to detected chickens
![image](https://github.com/EzraFathurrahman/chicken-behavior/assets/63547189/1b110f40-8166-4b5a-9440-466cfadd71dd)

- Chickens movement plot
![image](https://github.com/EzraFathurrahman/chicken-behavior/assets/63547189/6171ca00-9f14-4d28-ae48-9e26f44c0704)

- Table describing chickens as normal or as anomaly (potentially sick chicken)
![image](https://github.com/EzraFathurrahman/chicken-behavior/assets/63547189/fe7c21ed-3706-4570-ac57-fb129e9ff6ce)

6. These results can be downloaded by pressing the Download Results button. It will return a zip file containing the results.
![image](https://github.com/EzraFathurrahman/chicken-behavior/assets/63547189/fc0cf39c-ca9d-4d20-ade2-dc9954101ea0)

## Public Usage
For the moment, the application is used only for IPB University internals.
 

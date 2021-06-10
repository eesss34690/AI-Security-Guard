# AI-Security-Guard
By integrating Raspberry Pi with Dlib+OpenCV, the simple but useful, portable facial recognition tool is shown.

## Structure
- The usage is like the below flow chart
![](https://i.imgur.com/mmrOHYq.png)


|Usage|Description|
|-|-|
|Computing|Raspberry Pi 4b|
|Display|Monitor|
|Input|Keyboard|
|Capture|Webcam|
|OS|2021-05-07-raspios|
|Python|3.7.1|
|Opencv-contrib-python|4.5.2.54|
|Dlib|19.22.0|

## Installation guide
- Seperate the project with the tools, the following are three parts to deal with.
### Dlib
- Install OpenCV and Dlib like the instruction in other websites for Raspberry Pi.
- Download 2 files from web and put them in a folder named ```datasource```:
    - ```dlib_face_recognition_resnet_model_v1.dat```
    - ```shape_predictor_68_face_landmarks.dat```

- Then use ```get_face_from_camera.py``` to add face snapshot.
- Use ```get_features_into_CSV.py```to turn the image into attribute vector
- Use ```face_reco_from_camera.py``` to test whether it is success or not.

### Line BOT
- Construct an offcial account for the line notification
- Use the ```Client ID```, ```User ID```, ```Account Private Key``` for authorization in code.
- To put your code running in raspberry pi on remote server, use some tools like ```ngrok```as the bridge to communicate with local server and remote line server.
![](https://i.imgur.com/gqVlLSq.png)



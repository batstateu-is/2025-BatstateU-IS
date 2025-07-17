# Open & Obstacle Challenge Source Code

This directory contains the source code for both the **Open Challenge** and **Obstacle Challenge**. All files needed to run the robot programs are included and organized for clarity.

- The subdirectory `camera/` contains the scripts used by the **OpenMV Cam H7 Plus**, which processes visual data like blob detection and transmits information to the hub.
- The subdirectory `hub/` includes the code running on the **SPIKE™ Prime Hub**, responsible for driving logic, navigation, obstacle detection, and decision-making based on input from the camera and sensors.

The files:

- `hub/pupremote_hub.py`  
- `camera/lpf2.py`  
- `camera/pupremote.py`  

are by [antonvh](https://github.com/antonvh) and come from the repository [PUPRemote](https://github.com/antonvh/PUPRemote). They handle the communication between the camera and hub using the LEGO® Wireless Protocol and are essential for seamless integration of vision data.

> 📁 Each script has been customized or wrapped to fit the specific needs of this project, especially for real-time response, efficiency, and compatibility across both Open and Obstacle Challenges.

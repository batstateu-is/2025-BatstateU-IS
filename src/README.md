# 📁 `src/` Directory -  Open & Obstacle Challenge Source Code

This directory contains the source code for both the **Open Challenge** and **Obstacle Challenge**. All files needed to run the robot programs are included and organized for clarity.

### 📁 [`camera/`](./camera/) – OpenMV Cam Scripts

Contains scripts used by the **OpenMV Cam H7 Plus**, which handles visual processing tasks like color blob detection and transmits processed data to the hub via Bluetooth.

### 📁 [`hub/`](./hub/) – SPIKE™ Prime Hub Code

Contains the programs that run on the **LEGO SPIKE™ Prime Hub**, managing:
- Driving and navigation
- Obstacle detection and avoidance
- Decision-making based on sensor and camera inputs

### 📄 External Files from [PUPRemote](https://github.com/antonvh/PUPRemote):

The following files are adapted from [antonvh](https://github.com/antonvh)’s project [PUPRemote](https://github.com/antonvh/PUPRemote):

- [`hub/pupremote_hub.py`](./hub/pupremote_hub.py)  
- [`camera/lpf2.py`](./camera/lpf2.py)
- [`camera/pupremote.py`](./camera/pupremote.py)

These files handle **LEGO® Wireless Protocol** communication between the camera and the hub. They are essential for relaying vision data in real time.

### 📁 [`lms-esp32/`](./lms-esps32/) – ESP32 Ultrasonic Interface

Contains firmware for the ESP32 microcontroller, which manages three HC-SR04 ultrasonic sensors connected to the hub.
This module handles:

Distance measurement from all three sensors

Data filtering and communication with the SPIKE™ Prime Hub

Efficient serial or Bluetooth data transmission for obstacle proximity awareness

> 📁 Each script has been customized or wrapped to fit the specific needs of this project, especially for real-time response, efficiency, and compatibility across both Open and Obstacle Challenges.

***
# Batangas State University - Integrated School
[![](https://img.shields.io/badge/FE-Rulebook-2e52af)](https://wro-association.org/wp-content/uploads/WRO-2024-Future-Engineers-Self-Driving-Cars-General-Rules.pdf)
[![](https://img.shields.io/badge/YouTube-OPEN_CHALLENGE-df3e3e?logo=youtube)]()
[![](https://img.shields.io/badge/YouTube-OBSTACLE_CHALLENGE-df3e3e?logo=youtube)]()

<!--  -->
*intro text, blah blah blah*
***
<!-- Table of Contents -->
## Table of Contents

* [Introduction](#introduction)
* [Team Profile](#team-profile)

***
## Introduction

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Engineering is the heart of innovation that gives life to initiatives. It bridges science, technology, and creativity to provide solutions for real-world problems. In the field of robotics, engineering allows everyone to think and design beyond the current possibilities, highlighting that a future with numerous solutions can be made. Thus, through this, we were able to challenge ourselves to integrate various engineering concepts in autonomous navigation. As a team of student innovators and future engineers, we embraced this opportunity to create a self-driving robot that exemplifies the spirit of modern engineering. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This engineering documentation provides a comprehensive record of the BatStateU Spartan Team’s design process, program construction,  problem-solving strategies, and technical decisions throughout the development of our self-driving robot. This provides insight into our robot’s architecture, programming approach, and the challenges we encountered and overcame along the way. Intended for the Future Engineers Category in the 24th Philippine Robot Olympiad, this documentation reflects the dedication and initiative of our team to produce an innovation that goes beyond the boundaries of autonomous technology. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;We have featured key aspects involved in the development of our robot such as the Robot Specifications which provides information about the architecture of the robot, and selection of sensors, motors, and mechanical components with consideration to different aspects like speed, power, and specifications; Mobility Management that focuses on the specific movements that the robot can do; Power and Sense Management that is responsible for the description of the programming language and libraries utilized, algorithm explanations, and program logic flow; Challenge Strategies which features code snippets with explanations of its purpose, and the strategies we came up for the Open Challenge, Obstacle Challenge, traffic sign avoidance, and parking; and performance testings which includes setup conditions, observed issues, and video demonstrations. In addition, the engineering innovations integrated into the robot and a guide for its construction were added. To further support the technical information, the team added visual documentation that features actual and 3D model images of the robot. With these, the team aimed and continuously aims to demonstrate engineering discipline rooted in teamwork, determination, rigorous testing, and excellence with a purpose of being able to think of and design an innovative and modern solution as future engineers. 

***

## Team Profile
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Batangas State University - Integrated School is a group of passionate and curious young engineers driven by a shared goal: to innovate through robotics. Each member believes that learning through doing, as well as failing, has shaped us into better innovators, thinkers, and collaborators. Together, we have combined our skills and passion for robotics, engineering, and programming to create our own innovation of a self-driving robot for the Future Engineers category. 

### **John Angelo M. Bautista**

<center><img url></center>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Angelo is an incoming Grade 12 student at Batangas State University - The National Engineering University - Integrated School and is currently 17 years old. This year marks his third time participating in the Philippine Robot Olympiad (PRO) and his second time in the Future Engineers category. Drawing from his previous experiences, he ensures that the robot is built with consideration to its efficiency and functionality, making him a key pillar of the team.

### **Airvin James L. Medina

<center><img url></center>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Airvin is stepping into his first journey at Philippine Robot Olympiad this year. At 15 years old, this incoming Grade 10 student at Batangas State University - The National Engineering University - Integrated School has shown a remarkable interest in robotics and programming. His enthusiasm for solving problems and thinking critically allow him to develop and troubleshoot codes effectively, bringing the robot’s function to life.

### **Cshenizylle Nicole M. Ligayada

<center><img url></center>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Cshenizylle is a 16-year-old incoming Grade 11 student at Batangas State University - The National Engineering University - Integrated School who is also participating in the Philippine Robot Olympiad for the first time. With a strong interest in research and writing, she takes on the role of documenting the team’s engineering journey. As she enters this new environment, she looks forward to gaining new experiences and growing alongside her teammates. 

The following pictures feature the members of Batangas State University - Integrated School (BatStateU-IS) participating in the Future Engineers category along with their robot. 

<img src = "">

## Robot Specifications

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Our team, the Batangas State University - Integrated School, introduces a self-driving robot that is developed for the Philippine Robot Olympiad 2025, under the Future Engineers category. This robot represents our vision of combining creativity and technical skill to design a robot capable of autonomous navigation, obstacle handling, and real-time decision-making. Through teamwork, perseverance, and continuous improvement that has shaped its development, we have ensured that this is carefully engineered to meet the demands of the competition. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The following specifications provide a detailed overview of the key physical and mechanical characteristics of our team’s self-driving robot. We designed this while giving importance to precision, agility, and durability, so the features of the robot have been carefully optimized to balance speed and stability during runs. 

<img src = "">
<img src = "">

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Additionally, the team’s selection of materials and electronic components is intended to create a strong yet lightweight robot platform, designed to deliver reliable and consistent performance. The list of the main components and its corresponding description presented in the table below emphasize these critical design choices and technical details that enhance the robot’s overall functionality.

<img src = "">

# 1. Mobility Management

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This section will highlight the important aspects of the hardware system that constitutes the mobility and movement specifications of the self-driving robot that we have developed. This includes the reasons behind the selection of the drive system, steering mechanism, wheels, motor, and their respective placements, which all play a vital role in ensuring our robot moves smoothly, accurately, and reliably throughout the challenges. 


### 1.1. Motor Selection

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;One of the most important things that we have considered to enhance the maneuverability of the self-driving robot is to properly select motors that meet the requirements needed for the Open Challenge and Obstacle Challenge. Within the LEGO® Education SPIKE™ Prime Set, we had two primary motor options to choose from: the Medium Angular Motor and the Large Angular Motor. To determine the most suitable motor, we evaluated key specifications such as speed (RPM), torque (rotational force), connectivity, and the intended application in our design. 

<img src = "">

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Table 3 shows the difference between the large motor and medium motor in terms of different specifications, with all performance data being based on a 7.2V power supply. The Technic™ Medium Motor, while more small and lightweight, offers faster rotation speeds but lower torque. This makes it ideal for lightweight mechanisms, low-profile design with limited space or tasks requiring quick response but low-resistance motion. In addition to wheels, it is ideal for driving attachments like arms, lifts, or actuators on robots. However, for driving the entire robot, where it must carry multiple components, handle tight turns, and maintain stability over long distances, more torque and control are required. This makes the Large Motor more appropriate for its strength and ability to handle resistance. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;After comparing both options, we decided to integrate the Technic™ Large Angular Motor for our robot’s driving and steering system. This features a built-in advanced Rotation Sensor that can report speed, angle changes, and absolute position within a range of -180° to +180°. It can also sense direct user input or manual rotation which allows responsive input during calibration or testing. While powered by a 7.2V system, the motor can achieve a torque of 25 Ncm at stall, and performs most efficiently at 8 Ncm with 135 RPM. Its speed with no load reaches up to 175 RPM. Its sensor offers a resolution of 360 counts per revolution, an accuracy that is less than or equal to ±3 degrees, and a fast update rate of 100 Hz for real-time feedback. In terms of design, the motor has a Technic build geometry and includes a 250 mm LEGO® Power Functions 2.0 (LPF2) cable and dual crosshole outputs, making it easy to integrate securely into complex builds. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Overall, it provides higher torque which is essential for maintaining a consistent speed while carrying the weight of the hub, sensors, camera, and LEGO and 3D-printed components. This motor also offers smoother acceleration and deceleration, and more responsive driving system, helping the robot to maintain its stability when turning. Thus, we have utilized three Technic™ Large Angular Motor in our self-driving robot, with the first one being connected to the steering wheel, second for the drive system, and the third motor for the rotating camera and distance sensor. 

### 1.2. Steering and Driving Mechanism

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;After carefully evaluating several options, our team decided to use a rear-wheel drive (RWD) system combined with a parallel steering mechanism. This combination closely resembles the movement of a real car, which can provide consistent and reliable results. 

<img src = "">

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;For the robot’s steering mechanism, one Technic™ Large Angular Motor is integrated at the front of the self-driving robot to steer the front wheels, where they turn in the same direction at the same angle. This method is referred to as parallel steering and is similar to how steering works in real cars. We chose this steering geometry over other options such as Differential Steering, where one wheel moves faster than the other in order to turn; Ackermann, in which the inner wheel turns at a greater angle than the outer wheel, as well as the counterpart of Ackermann, Anti-Ackermann. It offers simplicity compared to other options that are more complex to build and control. Furthermore, both the Open and Obstacle Challenge requires maneuverability; thus, the smaller turning radius offered by parallel steering is advantageous especially for tight spaces like parking. This steering geometry also solves our problem with an uneven and irregular field as it improves the stability and handling of movement and turns of the self-driving robot. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Consequently, we selected rear-wheel drive (RWD) because it provides better traction, especially when the robot needs to travel consistently. Our team also believes that RWD is better than front-wheel drive (FWD), which can make the robot harder to balance, especially when it needs to carry sensors and components at the front. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;By combining RWD and parallel steering, we achieved a movement system that was both stable and precise. The rear wheels provided consistent driving force, while the front wheels helped for smooth turning without affecting the robot's balance. This setup made it easier for our robot to navigate around tight corners and spaces, maintain alignment, and avoid obstacles effectively.

### 1.3. Mechanical Design

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The structure of our self-driving robot is made mostly out of LEGO® Technic™ elements, with a combination of 3D-printed materials. Drawing from last year’s experience — where the robot is constructed using only LEGO® Technic™ materials — we have learned that it is essential to integrate engineering factors, with creativity and originality in mind. Therefore, for this year’s competition, our team has developed various 3D-printed components that made our self-driving robot unique and innovative. For instance, from a camera case made out of LEGO, we have designed a 3D-printed case that incorporated a slide-lock mechanism, which offers something new, but still efficient, functional, and reliable for our team’s robot. Further explanation about this case is discussed at Chapter 5: Engineering Factor, 5.1. 3D-Printed Camera Case. 

<img src = "">

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Additionally, the length of the robot is built to be longer, given that while the length of the robot increases, the larger the space will be intended for the parking area. We have utilized two different materials for the robot: the LEGO Wheel 75 mm x 17mm with Motorcycle Tire 94.2 mm x 20 mm and Technic™ White Wheels with a diameter of 43 mm, which handles the driving and steering mechanism, respectively. The large wheels were used for the rear-wheel drive system since a larger wheel possesses a larger circumference, and thus, having the ability to travel longer distances per rotation. It also increases the maximum speed limit a robot can travel per unit of time. Consequently, smaller wheels were utilized for the steering mechanism since they have a smaller turning radius, which makes it easier for the robot to handle tight turns in navigating obstacles, corners, and small spaces. Moreover, larger wheels cannot be used at the front part of the robot as these can block the view of the distance sensor, disabling the sensor to detect objects properly and accurately. The Technic™ White Wheels also offer more precision and finer control, preventing slips that makes the robot’s movement smooth and quick. 

<img src = "">

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;To balance the weight distribution of the robot throughout its body, the Technic™ Large Hub was placed between the drive and steer system. This central placement evenly distributed the weight across all wheels, and significantly improved the robot’s overall stability, turning accuracy, and movement consistency.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In addition, while our team were testing runs, we noticed how the rear part of the robot was lighter than other sections, causing unstable turns and movements. Thus, we have integrated an EV3 Steel Ball to increase the weight on the rear side of the robot. This balanced weight distribution enhanced the wheel’s traction and consistency, and prevented  tilting, making it more responsive to directional changes.

<img src = "">

# 2. Power and Sense Management

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The performance of our self-driving robot relies heavily on the integration of electrical components and the development of programs. Mainly developed with Python programming language, the robot was structured to carry out specific tasks for both the Open Challenge and Obstacle Challenge of the Future Engineers category. This section will discuss the elements that power and control the robot, including the power source, sensors, and its vision system. Each component that constitutes the robot was carefully selected and evaluated based on their specifications that meets the demand for ensuring real-time responsiveness, accuracy, and reliability during autonomous navigation and handling of obstacles. 

## 2.1. Power Management

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A reliable power source is essential for the consistent and uninterrupted performance of the robot. In managing and choosing the right power system, our team ensured that all electrical components, such as the sensors and motors, will receive stable and sufficient energy throughout countless testings.  It is essentially what gives life to the robot. Consequently, this is the most important aspect to consider especially during competition runs, as we don’t want delays or power interruptions that could lead to performance issues. Our robot uses a rechargeable lithium-ion battery specifically designed for the SPIKE™ Prime Large Hub. This battery provides the necessary voltage and current to support motor movements and sensor readings. 

<img src = "">

### 2.1.1. Technic™ Prime Large Hub

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The SPIKE™ Prime Technic™ Large Hub is the main controller of our self-driving robot. It is a programmable control unit that connects to LEGO® motors and sensors through six input/output (I/O) ports, labeled A to F. These ports allow the hub to power motors, read sensor values, and control various functions of the robot.

<img src = "">

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The hub runs on a MicroPython operating system, allowing us to write and execute advanced programs using Python. It features a built-in 6-axis Gyro Sensor with three-axis accelerometer and three-axis gyroscope that helps the robot detect rotation, orientation, and motion. This is especially useful for tracking turns and maintaining direction during navigation. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Physically, the hub includes a 5x5 LED matrix display, a three-button interface consisting of center, left, and right, and a speaker for feedback sounds. It supports both USB and Bluetooth connectivity, with Bluetooth 4.2 used for wireless communication and firmware updates. A rechargeable lithium-ion battery powers the hub, and it can be charged directly via a micro USB cable. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;With its compact size of 88.0 mm x 56.0 mm x 32.0 mm and compatibility with LEGO® Technic™ building elements, the SPIKE™ Large Hub is ideal for building smart and responsive robots like our self-driving robot. It provides 32 MB memory which is enough for programs and data, as well as a processing power of 100MHz M4 320 KB RAM 1M FLASH to support real-time decision-making and multitasking during both Open and Obstacle Challenge runs.

### 2.1.2. Technic™ Large Hub Rechargeable Battery

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The Technic™ Large Hub Rechargeable Battery is the partner and intended power source for the SPIKE™ Prime Hub. It is a lithium-ion polymer (Li-ion) battery with a capacity of 2100 mAh at 7.3 volts that provides enough energy to power the hub, motors, and connected sensors during the operation of the self-driving robot. This battery is designed with the perfect dimension and structure to fit securely inside the Technic™ Large Hub. One of its main advantages is that it can be charged directly while it is inside the hub via a standard micro USB cable. This way, there is no need for the battery to be removed during charging. However, when needed, the battery can also be removed easily without using any mechanical tools, which makes maintenance quick and easy for everyone to do.

<img src = "">

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The battery is built for durability, with a minimum lifespan of over 500 charge cycles. After 500 full charge/discharge cycles, it is expected to retain at least 30% of its original capacity, making it reliable for long-term use. This rechargeable battery supports the robot’s need for consistent and portable power, which is essential for the several autonomous tasks that the robot is programmed to do during both the Open and Obstacle Challenge rounds. Its high energy capacity, ease of use, and compatibility with the SPIKE™ system make it a critical component of our robot's electronics and system.

## 2.2. Sense Management

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The self-driving robot wouldn’t be in its form and purpose without its sensors and vision system. These components serve as the robot’s eyes, allowing it to perceive and respond to its surroundings with accuracy and intelligence. Through sensors such as the color sensor, distance sensor, and built-in gyro, the robot can detect objects, measure distances, identify markers that will decide its path or direction, and maintain orientation. Additionally, the integration of the OpenMV Cam H7 enables the robot to recognize traffic signs and make real-time decisions during navigation. The proper selection and programming of these sensing devices are critical to ensure that the robot’s performance will be reliable. 

<img src = "">

### 2.2.1. Technic™ Distance Sensor

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The Technic™ Distance Sensors are one of the core components of our robot that makes navigation and obstacle detection possible. Equipped with Time-of-Flight (ToF) technology, it can measure the distance a nearby object is from itself. By integrating this at the front and rear part of our robot, the sensor allows it to detect walls, track spacing, and avoid collisions with boundary walls during both the Open and Obstacle Challenge. The sensor can measure distances from 50 to 2000 mm with a ±20 mm accuracy. For faster sensing, its range measures from 50 to 300 mm and an accuracy of ±15 mm. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In addition to distance measurement, the sensor includes two built-in programmable LEDs that can also be viewed as its eyes. This can detect small objects or gestures when used at close range. However, in our application, the Distance Sensors are primarily used to detect obstacles and proximity from the boundary and parking walls. Consequently, the sensors communicate data to the hub at a frequency of up to 100 Hz, which allows the robot to quickly respond to changing surroundings. Its compact and design that is compatible with Technic build geometry makes it easy to integrate into the robot, and in our case, the first one is attached to a motor that rotates, similar to the eyes that can move sideways for a wider field of view and the second sensor is attached at the rear part of the robot to improve its capability to sense obstacles that are located behind it, specifically the parking wall. Overall, the two Technic™ Distance Sensors play a vital role in ensuring safe and accurate navigation by continuously monitoring the environment and helping the robot make decisions.

<img src = "">

### 2.2.2. Gyro Sensor 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In addition to external sensors, the SPIKE™ Prime Hub includes built-in motion sensors: a three-axis gyroscope and a three-axis accelerometer. These internal sensors play a crucial role in helping our self-driving robot detect its orientation, motion, and rotation during its operation. The accelerometer measures the direction of gravity along three axes — X, Y, and Z — allowing the hub to determine which side is facing up or down. This helps the robot identify its current orientation, such as whether it is upright, tilted, or falling. It also enables the detection of gestures such as taps, free fall, and shaking.

<img src = "">

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The gyro sensor measures the robot’s angular rotation across the three axes. It tracks changes in pitch (forward or backward tilt), roll (side-to-side tilt), and yaw (rotational direction). Furthermore, it can also provide both the rate of rotation in degrees per second and the total angle turned in degrees. This makes it possible for the robot to perform accurate turns, such as 90° or 180° rotations, and maintain straight paths when necessary. Together, the built-in gyroscope and accelerometer improve our robot’s ability to move precisely and respond to different conditions, especially in tasks that require accuracy in reading directions like wall avoidance, alignment, and parking. 

### 2.2.3. OpenMV Cam H7 Plus 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The OpenMV Cam H7 Plus serves as the self-driving robot’s vision system, enabling it to detect and interpret visual cues such as traffic signs in the Obstacle Challenge. This camera is small, low-power microcontroller, compact, and programmable with high-level Python scripts, allowing us to easily implement applications using machine vision in the real world.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The camera features an STM32H7 Arm® Cortex® M7 processor running at 480 MHz, with 512 KB of RAM and 2 MB of flash memory. It is equipped with an image sensor capable of taking 2592 x 1944 (5MP) images.  Our team chose to work on LAB thresholding because it works best under different lighting conditions, separating values based on human perception rather than raw RGB. To be able to identify objects based on the density of color pixels detected, the camera analyzes pixel density, which results in a more precise detection. A higher pixel density of the nearby object reveals its color, allowing the robot to evaluate this information, convey it through the central hub, and take the necessary action to avoid the obstacle.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In our setup, the OpenMV Cam H7 is mounted at the front of the robot, enclosed within a 3D-printed case that we designed ourselves. It is positioned and aligned to directly face the traffic signs that it will encounter across its laps. When the camera detects a traffic sign that is colored red or green, it processes the image and determines the appropriate direction where the robot should turn; left for green and right for red. We also programmed the camera to send its output by flashing a specific LED color (red or green). This helps us identify what the camera is seeing, allowing for easy and quick troubleshooting. 

<img src = "">

# 3. Open Challenge Strategy 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The Open Challenge Round of the Future Engineers category requires the self-driving robot to autonomously travel and complete three full laps around the game field with random placements of the inside track walls while ensuring that the robot will not make any contact with the outer boundary wall. The goals that we have established for our robot to accomplish in this round is to be able to accurately determine its driving direction at the beginning, maintain a stable motion and control across the entire loop, consistently avoid collisions with both the inner and outer walls, and successfully complete three full laps by making the turns, movement, and counter precise. Thus, we have considered various techniques and movement strategies for determining driving direction, wall detection and avoidance, and lap counting. 

<img src = "">

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In line with the flowchart above, the starting condition we implemented for the Open Challenge round involves the self-driving robot resetting its sensors and heading, then beginning its movement by driving forward at a constant speed, specifically 500 degrees per second. It continues this motion until its front-facing distance sensor detects a wall closer than a preset threshold. This initial forward movement ensures that the robot consistently reaches a defined checkpoint before making any directional decisions.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Once this threshold is met, the robot stops and proceeds to determine its driving direction: either clockwise or counterclockwise. To do this, the sensor mounted on a rotating motor scans both directions — first rotating to the left, measuring the distance, and then to the right. The robot then compares the measured values. If the right side has a greater distance, it sets the direction clockwise; otherwise, it sets it counterclockwise. This step is essential for adjusting the robot's path depending on the randomized starting location and ensuring that the robot follows the correct path and direction around the field.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;However, before turning, the rotating sensor must rotate along with the chosen direction to signal the upcoming turn. This can also assist with determining mistakes and debugging since it can communicate its movement with us. After performing the 90-degree turn, the sensor motor will then return to its original position — facing forward — to indicate that the turn has been completed and is prepared for the next turn or section. Moreover, while driving forward after each section and checking the distance from the preceding wall, the Technic™ Distance Sensor’s LEDs are programmed to light up on the side based on its direction. This action functions as a visual cue for the team, assisting in debugging and monitoring direction.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The robot then enters the lap execution loop, where it repeats a drive-turn sequence until it completes three full laps. As it moves forward, the robot uses PID control (as outlined in the flowchart) to maintain smooth and accurate motion, adjusting based on real-time distance measurements. When the front distance falls below the target proximity, the robot resets its PID settings, updates its target heading by 90 degrees (multiplied by its set direction), executes the turn, and increments the lap counter by 0.25, representing one segment of a full lap. This loop continues until the lap counter reaches 3.0, signaling that the three laps are complete.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;To finish, the robot executes a final command to drive straight to the center of the starting section using its distance sensor and then stops, completing the Open Challenge run. This process ensures both consistency and accuracy in lap tracking and navigation, allowing the robot to adapt to changing conditions while maintaining reliable performance.

## 3.1. Determining Drive Direction 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;At the start of the Open Challenge, the self-driving robot must decide which direction it should take around the field, which is either clockwise or counterclockwise. This decision that the robot will make depends on its position and surroundings at the beginning of the run. This step is one of the most crucial tasks, as it sets the course of the robot. Therefore, our team made sure to select the most appropriate strategy and components to ensure that the detection of direction will be accurate and consistent. This involved integrating the necessary sensors and programming logic that would allow the robot to make the correct decision. 

<img src = "">

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Once arrived on a certain position away from the wall, the robot executes a scanning sequence — rotating the sensor motor to the left, recording the measured distance, then repeating the process to the right. These two values are compared to determine which direction offers more open space. If the left side has more distance, meaning it's farther to a wall, the robot infers that this side is clearer and sets its course counterclockwise. Conversely, if the right distance is greater or larger, the robot will move clockwise.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;As explained in Section 2.2.1: Technic™ Distance Sensor under the Sense Management section, this distance sensor setup expands the robot’s field of view and enables it to assess space on both sides before beginning full movement. This strategy allows the robot to adapt to varying starting positions and ensures accurate detection into its navigation sequence.

## 3.2. Wall Detection and Avoidance

<img src = "">

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;To ensure that the robot can properly avoid collisions with both the randomly placed inner wall and the outer boundary walls of the game field, we implemented a dynamic wall detection strategy using a Technic™ Distance Sensor mounted on a Technic™ Large Angular Motor. We thought that giving it the ability to rotate sideways is a better technique for detection instead of keeping the sensor fixed, thus the robot’s field of view is increased, allowing it to detect walls in multiple directions without requiring the robot to physically change its orientation. Moreover, this design allows the robot to scan its surroundings at key decision points such as straight paths or before a turn, and determine the relative position of nearby walls. It allows the robot to compensate for the limitations of a fixed-sensor design, especially when the robot is driving alongside long stretches of wall or in unpredictable inner wall placements. 

<img src = "">
<img src = "">

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;To ensure consistency and accuracy, the sensor resets to its original position; it faces forward after each detection cycle. The scanning movement is also synchronized with the robot’s movement speed, so that sensor rotation does not delay navigation or cause imbalance. This wall detection system is one of the key innovations that makes our robot's Open Challenge performance more reliable and intelligent, especially under randomized field conditions.

# 4. Obstacle Challenge Strategy

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;After completing the Open Challenge, our team moved on to accomplishing the Obstacle Challenge, one of the main tasks in the Future Engineers category. In this round, the robot must autonomously complete three laps around the game field while avoiding randomly placed obstacles. Consequently, the placement of the obstacles will be determined before the commencement of the challenge. These obstacles include traffic signs colored red or green, which the robot must detect and respond to correctly. When a green traffic sign is detected, the robot is required to pass on the left side, while a red traffic sign indicates that it must pass on the right. In addition to obstacle avoidance, the robot must also begin the lap by moving out of the parking space and perform parallel parking at the end of the third lap. Additionally, the size of the parking space is based on the length of the robot and must be entered precisely without touching the boundary walls. This round tests the robot’s ability to recognize colors, make  real-time decisions according to what was detected, and move accurately under changing conditions. The following aspects described below are the essential techniques and movement strategies that we have considered for this challenge. 

<img src = "">

## 4.1. Traffic Sign Detection	
## 4.2. Parallel Parking Strategy
## 4.3. Machine Learning Strategy

# 5. Problems Encountered

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The process of developing and improving our robot would not be complete without encountering difficulties that tested both its mechanical and technical capabilities. However, these challenges became a valuable learning experience that pushed us to improve our strategies. This section will describe the most significant issues we faced and how we addressed them to improve the robot’s performance and reliability during the Open and Obstacle Challenge.

## 5.1. Continuous Detection to Single-Instance Detection
    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;It is clear from previous experience with the Future Engineers' Obstacle Challenge that continuous detection, in terms of execution, performs far better than single-instance detection. As a result, our team agreed on using continuous detection for reading traffic signs as our initial plant. In this strategy, the robot would constantly scan its environment while traveling around the field and responding to its readings. However, while we were trying to develop how the self-driving robot will perform this strategy, we have realized that it is not convenient to use. This method caused several issues such as delayed responses, overlapping detections, especially when the traffic signs are conflicting in the robot’s field of view. These problems led to wrong movements and inconsistent performance in obstacle avoidance. We also thought that it would be challenging to modify and troubleshoot the continuous detection program during the actual competition. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;To address this, we decided to shift our strategy into single-instance detection. With this method, the robot is programmed to recognize and react to a traffic sign only at specific intervals and at a designated spot. This made the program easier to manage and debug and the robot can detect the traffic signs more accurately by moving and stopping at specified points. It prevented conflicting inputs and allowed the robot to make a clear, one-time decision before moving forward. 

## 5.2. Frequent Disconnection of Camera Wiring

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;One of the most important components that powers our self-driving robot to function in the Obstacle Challenge is the OpenMV Cam HV Plus. Without this, it would be difficult to navigate around the field, making it more prone for mistakes in avoiding the randomly-placed obstacles. However, our team encountered numerous times where the connection of the camera was disrupted due to loose connection of wires. As a result, the self-driving robot was not able to complete three full laps and suddenly stopped its movement. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;From our previous design, we utilized electrical tape to connect the jumper wires attached in the pins of the OpenMV Cam H7 Plus to the wire connected in the SPIKE™ Prime Hub. However, this tape — over time — lost its adhesive, which resulted in disconnection and disruption of the camera from sensing and reading the obstacles,  affecting the overall performance of the robot in this challenge. To solve this issue, we decided to alter the connection and replace the electrical tape with a heat shrink tubing, which is a type of plastic tubing that shrinks when heated. It offers efficient electrical insulation and protection for electrical wires, cables, and other components. Additionally, the tubing comes in a range of diameters and colors to suit different purposes and is usually composed of materials like fluoropolymers, polyvinyl chloride (PVC), or polyolefin. The process of shrinking occurs when heat is applied to the tubing; thus, we have used a blower for easy accessibility and safety.  As the diameter of the tubing decreases, it firmly takes on the shape of the wire it is covering. This offers a strong defence against physical harm such as bending and breaking of wires, chemicals, moisture, and dust, firmly connecting the wires together and decreases the risk of disconnection. This material also creates a protective barrier around wires, preventing short circuits and electrical hazards. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Moreover, we also realized that the pins of the OpenMV Cam H7 Plus were having contact with one another, further disrupting it from functioning. Thus, we wrapped electrical tape around the jumper wires connected to the pins to prevent them from touching, as well as to secure the connection. This additional insulation helped to minimize the risk of short circuits caused by unintended pin contact, which could otherwise lead to sudden malfunctions or even permanent damage to the camera module.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;After reinforcing the connections with electrical tape and heat shrink tubing, we conducted multiple test runs to ensure that the camera functions reliably. We observed a significant improvement in the robot’s ability to maintain a continuous feed from the camera, allowing it to detect and avoid obstacles more effectively. The robot was now able to complete full laps without unexpected stops, proving that the modifications we made were effective.

## 5.3. Uneven and Unclean Field

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;As previously mentioned, the Obstacle and Open Challenge requires extreme focus in improving the robot’s precision in movement, obstacle detection, and turning. However, one of the problems we encountered during testing was the uneven, unclean, and unstable surface of the game field.  Certain areas, especially near the corners, had noticeable bumps, accumulated dust, gaps, or slight inclines that affected the robot’s movement. These surface irregularities caused unexpected tilting, loss of balance, and occasional slipping, particularly when the robot was executing tight turns or moving in a straight path. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This issue made it difficult for the robot to follow a consistent path and it occasionally interfered with the camera’s sensing and reading accuracy. To solve this issue, we performed several troubleshooting and adjustments in the values of our program and we also made structural modifications to improve the robot’s stability and ground contact, such as choosing the best wheels for both the steering and driving mechanism of the robot. These changes helped reduce the impact of the uneven field and allowed the robot to maintain smoother, more stable movement during its run.

## 5.4. Constant Necessity of Cleaning the Wheels

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;During the whole process, our team observed how the performance of the robot varied significantly on how clean and how dirty the wheels are. When the wheels accumulated dirt, the robot became more prone to drifting, especially during sharp or narrow turns. However, when the wheels were too clean, they caused slipping due to reduced friction which led to less reliable movement and poorer traction. We considered this as an issue since it is difficult to maintain the robot’s state where it performs well. Additionally, with continuous runs, the wheels naturally picked up dust and debris from the surface of the field, gradually affecting the robot’s ground contact and stability. This made it harder to maintain smooth and consistent movement throughout each test. As a result, we had to frequently check and clean the wheels to reduce the impact of this issue and ensure the robot could perform accurately and reliably.

# 6. 3D Printing Management

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Dedicated not only in improving the aesthetics of the self-driving robot, but also in enhancing its innovative principles, we have integrated multiple 3D-printed components that our team designed ourselves. Every part was thoughtfully engineered based on the specific requirements that we want to achieve for the improvement of our robot. This section will discuss and enumerate the process we underwent for designing and developing 3D-printed components that promotes the robot’s engineering factor. 

## 6.1. 3D Modeling

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;To design our 3D-printed parts, we used Blender, an open-source 3D modeling software known for its powerful tools for creating animation, visual effects, and accurate models suitable for 3D printing. We chose Blender because it allowed us to build detailed and customized components that were not possible using standard LEGO parts alone. The parts we created were carefully dimensioned to fit securely with existing LEGO Technic elements. 

<img src = "">

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In our workflow, we started by sketching the design based on the robot’s needs, then used Blender’s modeling tools to build the 3D geometry. We paid close attention to scale and alignment especially for parts that needed tight fits or moving mechanisms. Blender’s precise measurement tools and modifier system helped us refine each model before exporting them as STL files for slicing and 3D printing.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Overall, Blender was a great tool for us to quickly iterate, visualize, and finalize our parts with control and creativity. It played a crucial role in enhancing the robot’s functionality and design, making our build more advanced and innovative.

## 6.2. Material Selection 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;We selected FlashForge PLA filament with a 1.75 mm diameter as the primary material for all 3D-printed components because it is easy to print and provides reliable accuracy. PLA is one of the most commonly used filaments in 3D printing, and it offers several advantages that make it ideal for our robot design. First, PLA is easy to print with and has excellent dimensional accuracy, which is important for parts that need to fit precisely with LEGO elements and electronic components, such as the OpenMV Cam H7. It also has a low tendency to warp, allowing for reliable printing even on standard, non-heated surfaces.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Another advantage of PLA is its rigidity. This helps maintain the alignment and stability of mounted structural parts. While it is not as flexible or impact-resistant as materials like PETG or ABS, its stiffness is an important element for components that require shape retention under load. PLA is also biodegradable and more environmentally friendly than many other plastics, which aligns with responsible engineering practices. Given its ease of use, good surface finish, and suitability for fine details, PLA was the most practical and efficient choice for producing custom parts quickly and reliably throughout our development process.

## 6.3. 3D Printing Settings

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;After designing our custom components in Blender, we prepared them for printing using slicing software, FlashPrint 5 configured with optimized settings for PLA filament. Our goal in printing the components was to achieve a balance between strength, accuracy, weight, and print time while ensuring each part met the functional requirements of our robot.

<img src = "">

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In the setting, we’ve set the FlashForge PLA filament (1.75 mm) and a 0.4 mm nozzle throughout all prints. For layer height, we selected 0.2 mm, which provided a good compromise between surface quality and print speed. This layer height also helped maintain tight tolerances that are important for components like the slide-lock camera case that required precise fits with LEGO Technic parts. (Edit for other possible 3D-printed parts to be printed) Our infill density was set to 15% using a concentric pattern. This level of infill was strong enough for most structural parts while keeping the prints lightweight.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Print orientation was carefully chosen to improve strength. For example, parts that would experience vertical stress were printed lying flat so that the layer lines ran perpendicular to the direction of the force, reducing the risk of cracking. When prints involved overhangs or bridging, such as on the holes of the camera case, we used custom support structures enabled directly in the slicer, ensuring they were easy to remove without damaging critical surfaces. With these printing settings and careful preparation, we were able to produce durable, accurate, and functional parts that integrated seamlessly into the robot's structure and performance.

## 6.4. Printing

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;We used the FlashForge Adventurer 4 3D printer to print all the parts we have created and spliced. This printer was chosen for its reliability, ease of use, and compatibility with PLA filament. It features a fully enclosed printing chamber, which helps maintain a stable temperature during prints and reduces the risk of warping, especially useful when printing parts with larger surface areas or fine details. 

<img src = "">

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The Adventurer 4’s built-in camera and touchscreen interface allowed us to monitor progress in real time, making it easy to pause or stop a print if an error was detected. Its removable build plate also simplified part removal, reducing the risk of damaging delicate components. The use of the FlashForge Adventurer 4 played a key role in bringing our 3D designs to life and maintaining the overall quality of the robot’s construction.

<img src = "">

# 7. Engineering Factor

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Behind every successful robot is a series of problems, decisions, creative solutions, and innovative engineering. As a team of student innovators, we didn’t just focus on making the robot work—we focused on making it work smarter. Every engineering factor described in this section represents a solution that makes our robot more efficient, consistent, reliable, and adaptable, just as great engineering should. 

## 7.1. 3D-Printed Camera Case 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;One of the key engineering features we developed was a 3D-printed case for the OpenMV Cam H7, which serves as one of the robot’s vision. We created this case to hold the camera securely while also making it easy to access and remove when necessary. Instead of using a fixed mount that would waste time for disassembling, we designed a slide-lock mechanism. This lets us attach or remove the camera quickly, which is very helpful during testing, troubleshooting, or rewiring. The slide-lock also protects the camera from movement or shaking during runs, keeping it stable throughout each challenge. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The process involved several iterations to ensure that the case we create is both secure and easy to use. We began by creating a basic design of the case. The original plan was to use a simple screw to hold the camera in place. However, we couldn’t find the right screw size that could perfectly close the camera case. To solve this, we decided to redesign a case with a slide-lock mechanism. This would let us attach and remove the camera more easily without needing any mechanical materials or tools. The second version with a slide-lock design was printed, but the dimensions were slightly off compared to the actual size of the camera. However, we used this initial print to test the locking mechanism, and we found that it functioned properly. 

<img src = "">

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In our third attempt, we carefully measured the dimensions of the camera and adjusted the case with slide-lock design to ensure a more accurate fit. A 3D-printed beam was attached at the bottom of this case  to be able to mount it on the LEGO-built structure of the robot. This version successfully held the camera in place, allowed quick access, and ensured the wiring remained manageable and secure. 

<img src = "">

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;We created all designs using Blender, a 3D modeling software. Once the design was complete, we sliced the file using FlashPrint, and then printed the case using a FlashForge Adventurer 4 3D printer. Using 3D printing allowed us to customize the case that fits the camera perfectly. This step-by-step design process helped us build a camera case that was functional, durable, and easy to maintain.

## 7.2. Rotating Camera and Distance Sensor

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;To maximize the functionality of both the camera and the distance sensor, the robot is equipped with a Technic™ Large Angular Motor that enables these sensors to rotate approximately (degrees) in both directions from a central starting position. This rotational mechanism significantly expands the sensors' field of view, allowing the robot to better observe its surroundings, detect walls and obstacles from multiple angles, and respond more accurately to changes in the environment. This feature was developed in response to the limited number of available ports on the Technic™ Large Hub, which restricted the number of sensors that could be connected at once. By mounting both the OpenMV Cam H7 and the Technic™ Distance Sensor on a rotating platform powered by a single motor, we were able to simulate the presence of multiple sensors while conserving ports. The rotating sensor system plays a key role in obstacle detection, wall tracking, and situational awareness across both the Open and Obstacle Challenge rounds.

<img src = "">

## 7.3. Side Free Wheels

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;To enhance the safety, stability, and wall-tracking performance of the self-driving robot, the team integrated six medium-sized gears along the left and right sides of its frame. These gears function as free-rolling support wheels, strategically placed to help the robot maintain smooth movement when traveling close to walls. Unlike having a frame without these gears, these rotate freely, enabling the robot to glide alongside the walls without resistance.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This design allows the robot to self-correct its path by using the gears as passive alignment guides. When slight contact with a wall occurs, the gears help redirect the robot without causing it to tilt, stop, or lose speed. This is especially valuable in narrow spaces or during tight turns, where precise positioning is essential. Additionally, by minimizing the risk of direct collision between the robot’s core components and the wall, the system becomes more robust and consistent—even when facing unexpected environmental shifts or alignment errors. This solution significantly contributes to the robot’s overall reliability and control during both Open and Obstacle Challenge rounds.

# 8. Mechanical Improvements



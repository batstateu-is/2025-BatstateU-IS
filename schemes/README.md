Electromechanical diagrams
====

## 🔌 One-Button Power Mechanism Schematic Diagram

<center>
  
| ![Figure ](../docu-photos/schematic.png) |
|:---------------------:|
| One-Button Power Mechanism Schematic Diagram

Wire Connection is as follows:

Ultrasonic Rear Sensor (U2)
- VCC → ESP32 +5V
- TRIG → ESP32 IO27
- ECHO → ESP32 IO32
- GND → ESP32 GND

Ultrasonic Right Sensor (U3)
- VCC → ESP32 +5V
- TRIG → ESP32 IO33
- ECHO → ESP32 IO19
- GND → ESP32 GND

Ultrasonic Left Sensor (U4)
- VCC → ESP32 +5V
- TRIG → ESP32 IO21
- ECHO → ESP32 IO22
- GND → ESP32 GND

Additional Power Lines
- +5V (Battery) → ESP32 5V Pin
- GND (Switching Circuit) → ESP32 GND

</center>

---

## 🔌 One-Button Power Mechanism Switching Circuit

<center>
  
| ![Figure ](../docu-photos/switchingcircuit.png) |
|:---------------------:|
| One-Button Power Mechanism Switching Circuit

Wire Connection is as follows:

- GND (LMS–ESP32) → MOSFET Source (Q1, IRF3205)
- MOSFET Drain (Q1) → GND (Battery)
- MOSFET Gate (Q1) → Junction between R1 (10kΩ) and R2 (470Ω)
- R1 (10kΩ) → Between Gate and GND (Battery)
- R2 (470Ω) → Between Gate and +3.3V (from LPF2 connector)
- +3.3V (from LPF2 connector) → External logic power input
- GND (from LPF2 connector) → Common circuit ground

</center>

---

## 🔌 UART via SPIKE Port

<center>
  
| ![Figure ](../docu-photos/Cam.png) |
|:---------------------:|
| Camera Connection Wiring Diagram

Wire Connection is as follows: 

-  OpenMV 3.3 V (or VIN) → SPIKE Prime 3.3 V
-  OpenMV GND → SPIKE Prime GND
-  OpenMV TX → SPIKE Prime RX
-  OpenMV RX → SPIKE Prime TX

</center>

---

## 🔌SPIKE™ Prime Sensor to SPIKE™ Prime Hub

<center>

| ![Figure ](../docu-photos/spikehub.png) |
|:---------------------:|
| SPIKE™ Prime Hub Wiring Diagram

Wire Connection is as follows: 

-  Steering Motor → Port A
-  Driving Motor → Port B
-  First Distance Sensor → Port C
-  Second Distance Sensor → Port D
-  Vision Motor → Port E
-  OpenMV Cam H7 Plus → Port F

</center>




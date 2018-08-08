# Device Against Distracted Driving (DADD)
<p align="center">
  <img / ![](https://github.com/morganjlw/CPII/blob/master/images/dadd.png)>
  ![](https://github.com/morganjlw/CPII/blob/master/images/texting%20and%20driving.jpg)
</p>

## Summary
A device to accomodate an adaptation of the Canadian Ignition Interlock Program (IIP) to addresses increased cell phone distraction related accidents and offences. Raspberry Pi based project that uses Cell Phone and Driver's License authentication protocol to actuate vehicle ignition interlock. This project is a preliminary prototype, later revisions will comprise of a full OBDII interfacing system running specialized IC's with minimal power requirements (MCP and STN variants). Additionally, a variety of protocols will be addressed (SAE PWM and VPW J1850, ISO 9141-2, and J1939).

## Objective
The objective of this project is to prove the design concept. Lessons learned will guide future revisions. 

## Prototype Specifications
Raspberry Pi Zero used to authenticate cell phone using developer device ID, generic magnetic stripe reader to verify BC Drivers License, with a box employing closure detection. Mechanical relay used to control ignition signal path. Relay is actuated by Pi GPIO driven optocoupler. LED UI provides authentication status.

## System Design
High-level system schematic can be found in the images folder.
<p align="center">
![](https://github.com/morganjlw/CPII/blob/master/images/SystemDesign.JPG)
</p>

### Pi Zero Daughter PCB
Electrical schematics can be found in the schematics folder

### Software FSM
<p align="center">
![](https://github.com/morganjlw/CPII/blob/master/images/SoftwareFSM.JPG)
<\p>

Python is used to leverage a variety of open source Pi libraries to enable GPIO control and read phone ID and Drivers License data via the USB interfacing magnetic stripe reader.

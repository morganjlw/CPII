# Cell Phone Ignition Interlock (CPII)
![](https://github.com/morganjlw/CPII/blob/master/images/texting%20and%20driving.jpg)
# Device Against Distracted Driving (DADD)
![](https://github.com/morganjlw/CPII/blob/master/images/dadd.png)


## Summary
A device to accomodate an adaptation of the Canadian Ignition Interlock Program (IIP) to addresses increased cell phone distraction related accidents and offences. Raspberry Pi based project that uses Cell Phone and Driver's License authentication protocol to actuate vehicle ignition interlock. This project is a preliminary prototype, later revisions will comprise of a full OBDII interfacing system running specialized IC's with minimal power requirements (MCP and STN variants). Additionally, a variety of protocols will be addressed (SAE PWM and VPW J1850, ISO 9141-2, and J1939).

## Objective
The objective of this project is to prove the design concept. Lessons learned will guide future revisions. 

## Prototype Specifications
Raspberry Pi Zero used to authenticate cell phone using developer device ID, generic magnetic stripe reader to verify BC Drivers License, with a box employing closure detection. Mechanical relay used to control ignition signal path. Relay is actuated by Pi GPIO driven optocoupler. LED UI provides authentication status.

## System Design
High-level system schematic can be found in the images folder.
### Pi Zero Daughter PCB
![](https://github.com/morganjlw/CPII/blob/master/images/PCBLayout.JPG)

### Software FSM
![]()

Python code leverages a variety of Pi libraries to read phone ID, Drivers License data via the USB interfacing magnetic stripe reader, and GPIO control.

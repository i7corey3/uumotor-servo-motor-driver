# uumotor-servo-motor-driver
This repository uses pyserial communication to control the uumotor servo motor driver model **sdv48v30a** for python applications
This interface currently is incomplete with but does serve the necessay purpose of full directionaly motor control for both motor A and motor B outputs with absolute encoder readouts

> Not every feature has been implemented by the user manual that included the respected hex commands for every and all feature is included in this repository for reference or for potentional expansion if necessary.

## Setup

Before use please run the setup.sh script which will install all the dependencies required to use this interface.

```
./setup.sh
```

## How To Use

An example python script is included whihc menu items that are displayed for driving, calibrating and reading encoder inputs from the driver. This example can be ran by using the following command

```
python3 controller.py
```

## Disclaimer
This interface has not been fully tested and may result in bugs and or other software issue. please refer to the manual included in this repositroy for any unforeseen issues and feel free to fix any problems with this driver. I am open to any and all recommendations.

Happy Coding!
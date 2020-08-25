# eurobot2020-main

## installation

- install I2c tools to get i2cdetect utility
- `sudo apt install -y i2c-tools`

- Install node >= 10 with [this bash script](https://github.com/retrobox/console-modules/blob/master/v3.06/installnode.sh)
    - `wget https://github.com/retrobox/console-modules/blob/master/v3.06/installnode.sh && ./installnode.sh && rm installnode.sh`
- Install `arduino-cli`:
    - Go to [release page of arduino-cli repository on GitHub](https://github.com/arduino/arduino-cli/releases)
    - Choose binary file & wget this binary file
    - Extract binary from archive
    - Copy the binary to a dir contained in path (`/usr/bin` for example)
    - For example with raspberry pi on armv7:
        - `cd ~`
        - `wget -O arduino-cli.tar.gz https://github.com/arduino/arduino-cli/releases/download/0.9.0/arduino-cli_0.9.0_Linux_ARMv7.tar.gz`
        - `tar -xf arduino-cli.tar.gz`
        - `mv arduino-cli /usr/bin`
        - `rm arduino-cli.tar.gz`
- Install AccelStepper lib `arduino-cli lib install AccelStepper`
- Install LiquidCrystal_PCF8574 lib `arduino-cli lib install LiquidCrystal_PCF8574`
- Install lib udev `sudo apt install -y libudev-dev`
- Install lib usb `sudo apt install libusb-1.0`
- Follow [installation guide](https://serialport.io/docs/guide-installation#raspberry-pi-linux) for serialport node.js lib 

- Install TFMINI
    - run raspi-config > interface
        - say no to access the login prompt by serial
        - say yes to access the serial interface
    - [working code](https://gist.github.com/lefuturiste/b30491bd0758af9cf26cbc696270d49a)
    - edit /boot/cmdline.txt
        - `dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait`
    - edit /boot/config.txt, add the following line:
      - `dtoverlay=pi3-miniuart-bt`
    - [docs](https://wiki.dfrobot.com/TF_Mini_LiDAR_ToF__Laser_Range_Sensor_SKU__SEN0259)
    - pip3 install pyserial
    - [base tutorial](https://github.com/TFmini/TFmini-RaspberryPi/blob/master/README.md)
    - White = TX
    - Green = RX
    - only need RX

## Python installation

- pip3 install -r ./requirements.txt
- pip3 install PyEventEmitter && pip3 install adafruit-pca9685 && pip3 install websocket-server

## Library used

- https://github.com/Pithikos/python-websocket-server
- https://github.com/orb/pygments-json

### dualshock via node

- PyEventEmitter
- websockets

## Architecture

- interface hardware-software pour l'assemblage ascenseur
    - ouvrir pince
    - fermer pince
    - niveau supra eceuil
    - niveau attrape eceuil
    - niveau depilage rat/bas
    - niveau depilage haut
    - init pince
        - go to direction and click with end switch
        - close pince

- interface hardware-software pour l'assemblage tiroir
    - sortir tiroir
    - rentrer tiroir
    - init tiroir
        - go to endswitch

- routine attraper goblet (une routine par ascenseur)
    - si il est pas au bon niveau, se mettre au niveau haut
    - ouvrir pince
    - descendre au niveau eceuil
    - fermer pince
    - se mettre au niveau haut

- routine dépiller (une routine par ascenseur)
    - s'il il n'est pas ouvert, ouvrir le tiroir
    - s'il il est pas au bon niveau, se mettre au niveau depiller bas
    - ouvrir pince
    - se mettre au niveau depiller haut
    - fermer pince
    - fermer squeezer
    - se mettre au niveau deplier supra haut
    - ouvrir squeezer
    - (ranger tiroir)

## Communication protocol via Serial:

- 0: Drawer stepper
- 1: Left/Front Elevator
- 2: Right/Back Elevator

- positiveDirection: if true, step are positives

- STEPPERS
    - GO_TO_ORIGIN(int stepperId, bool positiveDirection)
    - GO_TO(int stepperId, int position)
    - DISABLE_ALL()
- LED
    - SET_FLASHING_MODE(array pulses)
    - DISABLE()
- BUTTON (will receive an event when button at falling edge of the push button: with the time)
    - ENABLE()
    - DISABLE()
- SCREEN
    - SET_FIRST_LINE()
    - SET_SECOND_LINE()
    - CLEAR()
    - ENABLE()
    - DISABLE()

## bluetooth

rfkill unblock bluetooth

## TODO

- disable feature on elevator
- disable elevator until go to origin to prevent steps jumps

### _note for recovery system

```
tmpfs /python-recovery tmpfs nodev,nosuid,size=2M 0 0
```

## Introduction

This is an USB rubber ducky workflow program written in **C++** utilizing the `Arduino mbed Framework` made for a `RP2040` MCU. By taking advantage of emulating an hid keyboard device, this small program can execute workflows to speed up work. It is intended to work with **Linux** as your primary operating system


<img width="1599" height="389" alt="" src="https://github.com/user-attachments/assets/b0f49d0f-1f93-4520-ae0e-9ab3bb91f927" />

*Holding/Bridging the GPIO12 to GND button to change workflows*

## Microcontroller Installation
* Download the [latest release](https://github.com/awesomebrownies/hid-workflow-emulator/releases/latest) `hid-workflow-emulator.uf2` file
* Insert installation medium
* Enter bootloader mode either by:
  * Pressing the boot button while inserting
  * OR, Bridging gnd & reset pin
* Copy `hid-workflow-emulator.uf2` file to the boot drive in your file manager
 
## Modifying the Code & Recompiling
* Install [PlatformIO](https://platformio.org/install) on VSCode
* Clone/Fork [this](https://github.com/awesomebrownies/hid-workflow-emulator) repository
  * Modify the code in `hid-workflow-emulator/src/hid-workflow-emulator.cpp`
* Use PlatformIO commands/VSCode GUI
  * "Upload and Monitor" button

**Improved the code?** Feel free to create a [Pull Request](https://github.com/awesomebrownies/hid-workflow-emulator/pulls)

## Features
* Select a different workflow by bridging the `GPIO12 pin` to a `GND pin` while using an internal pull-resistor on your MCU -- most effectively with a button
* Saves current workflow settings into flash
## Workflows
* [0] Programming:
  * Queries for subworkflows
  * Opens "GitHub Desktop", & "Intellij"
  * Runs a github repo analyzation script -- **requires** [mgitstatus](https://github.com/fboender/multi-git-status) utility to be installed
* [1] Dual Boot:
  * Stores current OS, allows for an easy insert to switch operating systems
  * Temporarily changes efibootmgr settings to one-time reboot to windows
* [2] Circuits:
  * Opens "KiCAD", & "VSCode"
* [3] _System Administration_:
  * **!** Intended for automating backups, not currently implemented

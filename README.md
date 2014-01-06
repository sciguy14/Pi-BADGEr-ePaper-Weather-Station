Pi BADGEr ePaper Weather Station
================================ 
The Pi BADGEr ePaper Weather Station is a simple, self-updating, weather station that utilizes a Raspberry Pi, a Wyolum ePaper OHS 2013 Badge Display, and an optional serially-controlled RGBW LED alert light to display current weather data for your area. Simple adjustable options at the top of the main Python file make it easy to disable use of the warning light, or to add your own serial commands that match up with a serially-controlled LED light that you can make. The instructions that go along with this hack focus on BADGEr, and not the light.

Instructions for Use
--------------------
A complete run-down on how to use these files, and how to get this project running on your Pi/BADGEr can be found on my website.  
*LINK COMING SOON*

Relevant Links and Libraries
----------------------------
This hack makes use of several other projects. Here are some links to things you'll need/want:
* [PySerial](http://pyserial.sourceforge.net/): The PySerial library is used to communicate between the Pi Python script and the BADGEr/light.
* [Python Weather API Library](https://code.google.com/p/python-weather-api/): This is a library that makes getting weather data in python super easy.
* [Wyolum Image Format](http://wyolum.com/introducing-wif-the-wyolum-image-format/): This is the format for the images that are stored on the SD Card.
* [Wyolum BADGEr ePaper Arduino Libraries](http://wyolum.com/wyolum-ereader-library/): These are the Arduino libraries that enable the BADGEr software to talk to the ePaper display.

Included Folders and Repo Contents
----------------------------------
### /BADGEr_Display
This folder contains the Arduino source code that should be loaded onto the BADGEr ePaper Display.
### /Hanger
These are the 3D-printed design files for the BADGEr hanging aparatus. They were created in sketchup, and you may want to tweak them to make it easier to hang the BADGEr unit from whatever you desire.
### /Weather Checker
This folder contains the Python file that should be placed in the home directory on your Raspberry Pi. It includes configuration options.
### /Weather Images
These are weather images that are used by the Yahoo Weather API. I have already converted them to WIF files that can be displayed on BADGEr. You just need to put them on the SD card that goes in BADGEr.

License
-------
Pi BADGEr ePaper Weather Station by Jeremy Blum  
Copyright 2014 Jeremy Blum, Blum Idea Labs, LLC.  
http://www.jeremyblum.com  
  
Licensed under the Apache License, Version 2.0
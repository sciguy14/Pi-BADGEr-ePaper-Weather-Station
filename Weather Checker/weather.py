#!/usr/bin/python

# Pi BADGEr ePaper Weather Station by Jeremy Blum
# Copyright 2014 Jeremy Blum, Blum Idea Labs, LLC.
# http://www.jeremyblum.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.  See the License for the specific language
# governing permissions and limitations under the License.

###########################
## CONFIGURATION OPTIONS ##
###########################

use_SUNN           = True                 # Enable updating SUNN (or compatible light display)
SUNN_dev           = '/dev/ttyUSB0'       # SUNN USB-Serial Device Location
SUNN_baud_rate     = 57600                # SUNN USB-Serial Baud Rate
rain_trigger       = 30                   # Above this percentage probably of precipitation, show the rain alert
rain_command       = '.a:3:0,0,10,0,500'  # Send this command when there is a rain alert
heat_trigger       = 75                   # Above this high (F) temperature, show the heat alert
heat_command       = '.a:3:10,0,0,0,500'  # Send this command when there is a heat alert
cold_trigger       = 50                   # Below this low (F) temperature, show the cold alert
cold_command       = '.a:3:0,0,0,10,500'  # Send this command when there is a cold alert
off_command        = '.a:3:0,0,0,0,500'   # If there are no special weather alerts, send this command

use_BADGEr         = True                 # Enable the BADGEr
BADGEr_dev         = '/dev/ttyUSB1'       # BADGEr USB-Serial Device Location
BADGEr_baud_rate   = 9600                 # BADGEr USB-Serial Baud Rate
write_delay        = 1.0                  # Delay between Serial Write Operations

serial_setup_local = True                 # True for Serial config in this file, False if you're doing it at boot


####################################
## MAIN PROGRAM                   ##
## Do Not modify below this point ##
####################################
import pywapi, serial, time, argparse, sys

parser = argparse.ArgumentParser()
parser.add_argument("zipcode", help="The zipcode of the city you want to display")
args = parser.parse_args()

#Get the weather for the provided Zip Code
print "Getting weather for zipcode " + args.zipcode + "...",
sys.stdout.flush()
yahoo = pywapi.get_weather_from_yahoo(args.zipcode, 'imperial')
weathercom = pywapi.get_weather_from_weather_com(args.zipcode)

#Parse chances of precipitation from weather.com
if weathercom['forecasts'][0].has_key('day'):
    chance_precip = weathercom['forecasts'][0]['day']['chance_precip']
else:
    chance_precip = weathercom['forecasts'][0]['night']['chance_precip']

print "Got weather for " + yahoo['location']['city'] + ", " + yahoo['location']['region'] + "!"

# Setup Serial Interfaces (Don't Reset on Connect)
# Note: DTR must be disabled for both USB serial ports.
# Make the raspberry pi do this on boot by adding these lines to /etc/rc.local:
# stty -F /dev/ttyUSB0 -hupcl
# stty -F /dev/ttyUSB1 -hupcl
# We can also do it directly in this file.
if serial_setup_local:
    from subprocess import call
    if use_SUNN:
        print "Setting up SUNN Serial port...",
        call(["stty", "-F", SUNN_dev, "-hupcl"])
        print "Done!"
    if use_BADGEr:
        print "Setting up BADGEr Serial port...",
        call(["stty", "-F", BADGEr_dev, "-hupcl"])
        print "Done!"

#Generate Sunn Lighting Commands
if use_SUNN:
    print "Generating SUNN Light warning settings...",
    if int(chance_precip) > rain_trigger:
        color = rain_command; #It might rain! Blue is for umbrella.
    elif int(yahoo['forecasts'][0]['high']) > heat_trigger:
        color = heat_command; #It's gonna be hot! Red is for heat.
    elif int(yahoo['forecasts'][0]['low']) < cold_trigger:
        color = cold_command; #It's gonna be cold! White is for cold.
    else:
        color = off_command; #Nothing special, turn the light off.
    print "Done!"
else:
    print "Skipping SUNN Light warning generation."

#ePaper Commands
if use_BADGEr:
    print "Generating BADGEr command strings...",
    image = "0/IMAGES/" + yahoo['forecasts'][0]['code'] + ".WIF\n"
    title = "1Weather Report\n"
    location = "2" + yahoo['location']['city'] + ", " + yahoo['location']['region'] + "\n"
    date = "3" + yahoo['forecasts'][0]['date'] + "\n"
    sunrise = "4Sunrise: " + yahoo['astronomy']['sunrise'] + "\n"
    sunset = "5Sunset: " + yahoo['astronomy']['sunset'] + "\n"
    conditions = "6Conditions: " + yahoo['forecasts'][0]['text'] + "\n"
    precip = "7Chance of Precipitation: " + chance_precip + "%\n"
    low = "8Low: " + yahoo['forecasts'][0]['low'] + "F\n"
    high = "9High: " + yahoo['forecasts'][0]['high'] + "F\n"
    commit = "A\n"
    print "Done!"
else:
    print "Skipping BADGEr command string generation."

#Control SunnLight
if use_SUNN:
    print "Connecting to SUNN Light...",
    sunnLight = serial.Serial(SUNN_dev, SUNN_baud_rate)
    print "Sending command...",
    sunnLight.write(color)
    time.sleep(.6)
    sunnLight.close()
    print "Done!"
else:
    print "Skipping SUNN Light control."

#Control ePaper
if use_BADGEr:
    print "Connecting to BADGEr..."
    ePaper = serial.Serial(BADGEr_dev, BADGEr_baud_rate)

    print "Setting Image,",
    ePaper.write(image)
    sys.stdout.flush()
    time.sleep(write_delay)

    print "Title,",
    ePaper.write(title)
    sys.stdout.flush()
    time.sleep(write_delay)

    print "Location,",
    ePaper.write(location)
    sys.stdout.flush()
    time.sleep(write_delay)

    print "Date,",
    ePaper.write(date)
    sys.stdout.flush()
    time.sleep(write_delay)

    print "Sunrise Time,",
    ePaper.write(sunrise)
    sys.stdout.flush()
    time.sleep(write_delay)

    print "Sunset Time,",
    ePaper.write(sunset)
    sys.stdout.flush()
    time.sleep(write_delay)

    print "Conditions,",
    ePaper.write(conditions)
    sys.stdout.flush()
    time.sleep(write_delay)

    print "Precipitation,",
    ePaper.write(precip)
    sys.stdout.flush()
    time.sleep(write_delay)

    print "Low,",
    ePaper.write(low)
    sys.stdout.flush()
    time.sleep(write_delay)

    print "and High."
    ePaper.write(high)
    sys.stdout.flush()
    time.sleep(write_delay)

    print "Updating Screen...",
    ePaper.write(commit)
    time.sleep(write_delay)

    ePaper.close()
    print "Done!"
else:
    print "Skipping BADGEr control."


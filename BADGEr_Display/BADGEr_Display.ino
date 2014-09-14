// Pi BADGEr ePaper Weather Station by Jeremy Blum
// Copyright 2014 Jeremy Blum, Blum Idea Labs, LLC.
// http://www.jeremyblum.com
// EPaper Libraries Copyright 2013 WyoLum, LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at:
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
// express or implied.  See the License for the specific language
// governing permissions and limitations under the License.

#include <inttypes.h>
#include <ctype.h>
#include <SPI.h>
#include <SD.h>
#include "EPD.h"
#include "S5813A.h"
#include "EReader.h"

int cmd;
char buffer[50];

/*
Commands:
0  Write Image with given location
1  Write Title
2  Write Location
3  Write Date
4  Write Sunrise Time
5  Write Sunset Time
6  Write Conditions
7  Write Precipitation Info
8  Write Low
9  Write High
A  Update display
*/

void setup()
{
  Serial.begin(9600);
  ereader.setup(EPD_2_7);
}


void loop()
{
  
  if(Serial.available() > 0)
  { 
    memset(buffer, 0, sizeof(buffer));   
    cmd = Serial.read();
    Serial.readBytesUntil('\n', buffer, 50);
    ereader.spi_attach();
    if (cmd == '0')
      ereader.display_wif(buffer, 132, 20);
    else if (cmd == '1')
      ereader.put_ascii(10, 5, buffer, false);
    else if (cmd == '2')
      ereader.put_ascii(10, 26, buffer, true);
    else if (cmd == '3')
      ereader.put_ascii(160, 5, buffer, true);
    else if (cmd == '4')
      ereader.put_ascii(10, 50, buffer, true);
    else if (cmd == '5')
      ereader.put_ascii(10, 66, buffer, true);
    else if (cmd == '6')
      ereader.put_ascii(10, 106, buffer, true);
    else if (cmd == '7')
      ereader.put_ascii(10, 122, buffer, true);
    else if (cmd == '8')
      ereader.put_ascii(10, 138, buffer, true);
    else if (cmd == '9')
      ereader.put_ascii(10, 154, buffer, true);
    else if (cmd == 'A')
    {
      ereader.show();
      ereader.spi_detach();  //To avoid screen washout.
    }
  }
  
}


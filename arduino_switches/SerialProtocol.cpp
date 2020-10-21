#include "SerialProtocol.h"

SerialProtocol::SerialProtocol() {}

void SerialProtocol::loop()
{
    if (Serial.available())
    {
        this->hasCommand = true;
        command = Serial.readStringUntil('\n');
        if (command != "") {
            this->commandName = command.substring(0, command.indexOf("#"));
            // Parse command arguments (1, 2, 3)
            String raw1 = command.substring(command.indexOf("#") + 1, command.length());
            if (raw1 != command) {
                this->commandParam1 = raw1.substring(0, raw1.indexOf("#")).toInt();

                String raw2 = raw1.substring(raw1.indexOf("#") + 1, raw1.length());
                //        Serial.println(raw2);

                if (raw2 != raw1) {
                    if (raw2.indexOf("#") != -1) {
                        this->commandParam2 = raw2.substring(0, raw2.indexOf("#")).toInt();

                        String raw3 = raw2.substring(raw2.indexOf("#") + 1, raw2.length());
                        if (raw3 != raw2) {
                            if (raw3.indexOf("#") != -1) {
                                this->commandParam3 = raw3.substring(0, raw3.indexOf("#")).toInt();
                                // last param is a string
                                this->commandParam4 = raw3.substring(raw3.indexOf("#") + 1, raw3.length());
                            } else {
                                this->commandParam3 = raw3.substring(0, raw3.length()).toInt();
                            }
                        }
                    } else {
                        this->commandParam2 = raw2.substring(0, raw2.length()).toInt();
                    }
                }
            }
        }
    } else {
        this->hasCommand = false;
    }
}

void SerialProtocol::reset()
{
    this->commandName = "";
    this->commandParam1 = 0;
    this->commandParam2 = 0;
    this->commandParam3 = 0;
    this->commandParam4 = "";
}
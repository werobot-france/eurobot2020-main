#pragma once
#include <Arduino.h>

class SerialProtocol
{
    private:
        String command = "";

    public:
        String commandName = "";
        int commandParam1 = 0;
        int commandParam2 = 0;
        int commandParam3 = 0;
        bool hasCommand = false;
        String commandParam4 = "";
        SerialProtocol();
        void loop();
        void reset();
};
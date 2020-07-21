int frontSwitches[2] = {12,9};
int rightSwitches[2] = {11,8};
int leftSwitches[2] = {10,7};
int emergSwitch = 5;
int startSwitch = 6;

int fs[2] = {1,1};
int rs[2] = {1,1};
int ls[2] = {1,1};
int es = 1;
int ss = 1;

bool f = false;
bool r = false;
bool l = false;
bool e = false;
bool s = false;

void setup(){
    Serial.begin(9600);
    Serial.println("F:OFF");
    Serial.println("R:OFF");
    Serial.println("L:OFF");

    for (int i = 0; i < 2; i++) {
      pinMode(frontSwitches[i], INPUT);
      pinMode(rightSwitches[i], INPUT);
      pinMode(leftSwitches[i], INPUT);
    }
    
    pinMode(emergSwitch, INPUT);
    pinMode(startSwitch, INPUT);
}

void loop() {

    for (int i = 0; i < 2; i++) {
      fs[i] = digitalRead(frontSwitches[i]);
      rs[i] = digitalRead(rightSwitches[i]);
      ls[i] = digitalRead(leftSwitches[i]);
    }
    es = digitalRead(emergSwitch);
    ss = digitalRead(startSwitch);

    
    if (es == 1) {
        if (e) {
            Serial.println("EmergencySwitch:OFF");
            e = false;
        }
    }
    if (es == 0) {
        if (!e) {
            Serial.println("EmergencySwitch:ON");
            e = true;
        }
    }

    
    if (ss == 1) {
        if (s) {
            Serial.println("StartSwitch:OFF");
            s = false;
        }
    }
    if (ss == 0) {
        if (!s) {
            Serial.println("StartSwitch:ON");
            s = true;
        }
    }



    if (fs[0] == 1 && 1 == fs[1]) {
        if (f) {
            Serial.println("F:OFF");
            f = false;
        }
    }
    if (fs[0] == 0 && 0 == fs[1]) {
        if (!f) {
            Serial.println("F:ON");
            f = true;
        }
    }


    if (rs[0] == 1 && 1 == rs[1]) {
        if (r) {
            Serial.println("R:OFF");
            r = false;
        }
    }
    if (rs[0] == 0 && 0 == rs[1]) {
        if (!r) {
            Serial.println("R:ON");
            r = true;
        }
    }


    if (ls[0] == 1 && 1 == ls[1]) {
        if (l) {
            Serial.println("L:OFF");
            l = false;
        }
    }
    if (ls[0] == 0 && 0 == ls[1]) {
        if (!l) {
            Serial.println("L:ON");
            l = true;
        }
    }

    delay(10); 
}
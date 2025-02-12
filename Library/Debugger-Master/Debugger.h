#ifndef DEBUGGER_H
#define DEBUGGER_H

#include <Arduino.h>

class DebuggerClass {
  public:
    template <typename T>  
    void Debugger(byte index, T data) { 
        String strData = String(data); // Converte o valor em string      
        if(strData == "Break"){
            Serial.print("B");    
            Serial.print(index);   
            Serial.println(":"); 
            delay(100);  
            while (!Serial.available());
        }else{
            Serial.print("V");    
            Serial.print(index);   
            Serial.print(":"); 
            Serial.println(strData);
            delay(100); 
        }
    }
};

extern DebuggerClass Debugger;

#endif

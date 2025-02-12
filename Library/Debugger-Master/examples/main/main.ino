/*
  Data: 05/01/2025
  Autor: DALÇÓQUIO AUTOMAÇÃO
  Projeto: Supervisório em Visual Basic para Arduino Uno
  Descrição: Envia valores de variável para o aplicativo Variavel-GUI.exe
 
*/

#include <Debugger.h>

///////////////////////////////////////////////////////////////////
// FUNÇÃO DE SETUP
void setup() {
  Serial.begin(9600);

  pinMode(2, INPUT_PULLUP);
  pinMode(13, OUTPUT);

  Debugger(0, "Pass");
  delay(100);

  Debugger(1, "Break");
  while(!Serial.available());
  
}// end setup

///////////////////////////////////////////////////////////////////
// FUNÇÃO DE LOOP
void loop() {
    static bool value_variavel;

    digitalWrite(13, HIGH);
    Debugger(1, "1");
    delay(1000);

    digitalWrite(13, LOW);
    Debugger(1, "0");
    delay(1000);

    if(digitalRead(2) == LOW){
      Debugger(2, "Close");
    }else{
      Debugger(2,"Open");
    }
    delay(100);

    int value_analog = analogRead(A0);
    Debugger(3, value_analog);
    delay(100);

    value_variavel = !value_variavel;
    Debugger(4, value_variavel);
    delay(100);

} // end loop

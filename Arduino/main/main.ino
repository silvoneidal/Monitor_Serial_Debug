/*
  Data: 05/01/2025
  Autor: DALÇÓQUIO AUTOMAÇÃO
  Projeto: Supervisório em Visual Basic para Arduino Uno
  Descrição: Envia valores de variável para o aplicativo Variavel-GUI.exe
 
*/


///////////////////////////////////////////////////////////////////
// FUNÇÃO DE SETUP
void setup() {
  Serial.begin(9600);

  pinMode(2, INPUT_PULLUP);
  pinMode(13, OUTPUT);

  Serial.println("V0:Pass");
  delay(100);

  Serial.println("B1:");
  while(!Serial.available());
  
}// end setup

///////////////////////////////////////////////////////////////////
// FUNÇÃO DE LOOP
void loop() {
    static bool value_variavel;

    digitalWrite(13, HIGH);
    Serial.println("V1:1");
    delay(1000);

    digitalWrite(13, LOW);
    Serial.println("V1:0");
    delay(1000);

    if(digitalRead(2) == LOW){
      Serial.println("V2:Close");
    }else{
      Serial.println("V2:Open");
    }
    delay(100);

    int value_analog = analogRead(A0);
    Serial.println("V3:" + String(value_analog));
    delay(100);

    value_variavel = !value_variavel;
    Serial.println("V4:" + String(value_variavel));
    delay(100);

} // end loop

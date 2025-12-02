#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27 ,16,2);
int credito = 0; int box = 1;
bool boton1 = 0; bool boton2 = 0; bool boton3 = 0;  
bool boton4 = 0; bool boton5 = 0;
bool flag = 0;
bool iniciado = 0;
unsigned long currentmillis = 0;
unsigned long previousmillis = 0;
int tiempo = 30;
int cuentaregresiva = 0;
int lastSeconds = -1;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  lcd.begin(16,2);
  lcd.init();

  pinMode(3,INPUT); pinMode(4,INPUT);
  pinMode(5,INPUT); pinMode(6,INPUT); pinMode(7,INPUT);
  pinMode(8,OUTPUT); pinMode(9,OUTPUT);pinMode(10,OUTPUT); 
  pinMode(11,OUTPUT);pinMode(12,OUTPUT);
}
void loop() {
  digitalWrite(8,HIGH);
  digitalWrite(9,HIGH);
  digitalWrite(10,HIGH);
  digitalWrite(11,HIGH);
  digitalWrite(12,HIGH);
  if (credito == 0 && Serial.available()) {
    String mensaje = Serial.readStringUntil('\n');
    mensaje.trim();

    if (mensaje.length() > 0 && mensaje.charAt(0) == 'C') {
      // Acción si la primera letra es 'C'
      int cantidad = mensaje.substring(1).toInt();
      credito = cantidad;
    }
    if (mensaje.length() > 0 && mensaje.charAt(0) == '?') {
      Serial.println(String(box) + "off");
    }
    if (mensaje.length() > 0 && mensaje.charAt(0) == 'T') {
      int cantidad = mensaje.substring(1).toInt();
      tiempo = cantidad;
    }
  }
  if (credito != 0 && iniciado == 0){
      iniciado = 1;
      cuentaregresiva = tiempo*credito;
      flag = 1;
      lcd.backlight();
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("   BIENVENIDO   ");
      delay(1000);
      lcd.setCursor(0,0);
      lcd.print("ELIJA EL LAVADO ");
      lcd.setCursor (2,1);
      lcd.print("Credito: ");
      lcd.setCursor (12,1);
      lcd.print(credito);
    }
  while (credito != 0){
    if(digitalRead(3)!=1||digitalRead(4)!=1||digitalRead(5)!=1||digitalRead(6)!=1||digitalRead(7)!=1){
      if (flag==1){
          previousmillis = millis();
          flag = 0;
        }
      if(digitalRead(3)==0){
        boton1 = 1;
        boton2 = 0; boton3 = 0; boton4 = 0; boton5 = 0;   
      }
      if(digitalRead(4)==0){
        boton2 = 1;
        boton1 = 0; boton3 = 0; boton4 = 0; boton5 = 0;      
      }
      if(digitalRead(5)==0){
        boton3 = 1;
        boton1 = 0; boton2 = 0; boton4 = 0; boton5 = 0;                  
      }
      if(digitalRead(6)==0){
        boton4 = 1;
        boton1 = 0; boton2 = 0; boton3 = 0; boton5 = 0;    
      }
      if(digitalRead(7)==0){
        boton5 = 1;
        boton1 = 0; boton2 = 0; boton3 = 0; boton4 = 0;              
      }
    }     
    if (boton1==1 || boton2==1 || boton3==1 || boton4==1 || boton5==1){
      currentmillis = millis();
      if(cuentaregresiva > 0){
        cuentaregresiva = (tiempo*credito) - ((currentmillis-previousmillis)/1000);
        if (cuentaregresiva < 0) cuentaregresiva = 0;
        int minutes = cuentaregresiva / 60;
        int seconds = cuentaregresiva % 60;
        lcd.setCursor (0,1);
        lcd.print("Tiempo:   ");
        lcd.setCursor(10, 1);
        lcd.print(minutes < 10 ? "0" : "");
        lcd.print(minutes);
        lcd.print(":");
        lcd.print(seconds < 10 ? "0" : "");
        lcd.print(seconds); 

        if (seconds != lastSeconds) {
          Serial.print(String(box) + "T");
          Serial.print(minutes);
          Serial.print(":");
          Serial.println(seconds);
          lastSeconds = seconds;
        }
      
        if (boton1 == 1)  jabon_prelavado();
        if (boton2 == 1)  jabon_en_lanza();
        if (boton3 == 1)  espuma_en_cepillo();
        if (boton4 == 1)  enjuague_en_lanza();
        if (boton5 == 1)  cera_en_lanza();
      }
      else{
        boton1=boton2=boton3=boton4=boton5=0;
        credito = 0;
        iniciado = 0;
        digitalWrite(8,HIGH);
        digitalWrite(9,HIGH);
        digitalWrite(10,HIGH);
        digitalWrite(11,HIGH);
        digitalWrite(12,HIGH);
        cuentaregresiva = 0;
        lcd.noBacklight();
        lcd.clear();
      }
    } 
}}

void jabon_prelavado(){   //Micro Reles 8,9,10,11 y 12 activo por "0".
  lcd.setCursor(0,0);
  lcd.print(" DESENGRASANTE ");
  Serial.println(String(box) + "D");
  digitalWrite(8,LOW);
  digitalWrite(9,HIGH);
  digitalWrite(10,HIGH);
  digitalWrite(11,HIGH);
  digitalWrite(12,HIGH);
}
void jabon_en_lanza(){
  lcd.setCursor(0,0);
  lcd.print("  HIDRO JABON  ");
  Serial.println(String(box) + "J");
  digitalWrite(9,LOW);
  digitalWrite(8,HIGH);
  digitalWrite(10,HIGH);
  digitalWrite(11,HIGH);
  digitalWrite(12,HIGH);
}
void espuma_en_cepillo(){
  lcd.setCursor(0,0);
  lcd.print("      FOAM     ");
  Serial.println(String(box) + "F");
  digitalWrite(10,LOW);
  digitalWrite(8,HIGH);
  digitalWrite(9,HIGH);
  digitalWrite(11,HIGH);
  digitalWrite(12,HIGH);  
}
void enjuague_en_lanza(){
  lcd.setCursor(0,0);
  lcd.print("   HIDRO AGUA   ");
  Serial.println(String(box) + "A");
  digitalWrite(11,LOW);
  digitalWrite(8,HIGH);
  digitalWrite(9,HIGH);
  digitalWrite(10,HIGH);
  digitalWrite(12,HIGH);
}
void cera_en_lanza(){
  lcd.setCursor(0,0);
  lcd.print("   HIDRO CERA    ");
  Serial.println(String(box) + "C");
  digitalWrite(12,LOW);
  digitalWrite(8,HIGH);
  digitalWrite(9,HIGH);
  digitalWrite(10,HIGH);
  digitalWrite(11,HIGH);
}
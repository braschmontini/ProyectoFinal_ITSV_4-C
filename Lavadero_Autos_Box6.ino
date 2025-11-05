#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27 ,16,2); // si no te sale con esta direccion  puedes usar (0x3f,16,2) || (0x27,16,2)  ||(0x20,16,2) 
int teclado = 0; int credito = 0;
bool boton1 = 0; bool boton2 = 0; bool boton3 = 0;  
bool boton4 = 0; bool boton5 = 0;
bool flag = 0;
unsigned long currentmillis = 0;
unsigned long previousmillis = 0;
int cuentaregresiva = 0; int cuentaregresiva2 = 0;
long lastDebounceTime = 0;  // the last time the output pin was toggled
long debounceDelay = 150;   // the debounce time; increase if the output flickers

void setup() {
  Wire.begin();
  lcd.begin(16,2);
  lcd.init();
  attachInterrupt(digitalPinToInterrupt(2), coin, FALLING);
  attachInterrupt(digitalPinToInterrupt(3), service, FALLING);
  pinMode(2,INPUT); pinMode(3,INPUT); pinMode(4,INPUT);
  pinMode(5,INPUT); pinMode(6,INPUT); pinMode(7,INPUT);
  pinMode(8,OUTPUT); pinMode(9,OUTPUT);pinMode(10,OUTPUT); 
  pinMode(11,OUTPUT);pinMode(12,OUTPUT);pinMode(13,OUTPUT);
}
void loop() {
  digitalWrite(8,HIGH);
  digitalWrite(9,HIGH);
  digitalWrite(10,HIGH);
  digitalWrite(11,HIGH);
  digitalWrite(12,HIGH);
  if (credito == 1 || credito == 2){
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
    lcd.setCursor (12,1);  lcd.print(credito);
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
      if(currentmillis - previousmillis <= (270000*credito)){
        cuentaregresiva = (270*credito) - ((currentmillis-previousmillis)/1000);
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
        //delay(100);       
        if (boton1 == 1)  jabon_prelavado();
        if (boton2 == 1)  jabon_en_lanza();
        if (boton3 == 1)  espuma_en_cepillo();
        if (boton4 == 1)  enjuague_en_lanza();
        if (boton5 == 1)  cera_en_lanza();
      }
      else{
        boton1=boton2=boton3=boton4=boton5=0;
        credito = 0;
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
  digitalWrite(8,LOW);
  digitalWrite(9,HIGH);
  digitalWrite(10,HIGH);
  digitalWrite(11,HIGH);
  digitalWrite(12,HIGH);
}
void jabon_en_lanza(){
  lcd.setCursor(0,0);
  lcd.print("  HIDRO JABON  ");
  digitalWrite(9,LOW);
  digitalWrite(8,HIGH);
  digitalWrite(10,HIGH);
  digitalWrite(11,HIGH);
  digitalWrite(12,HIGH);
}
void espuma_en_cepillo(){
  lcd.setCursor(0,0);
  lcd.print("      FOAM     ");
  digitalWrite(10,LOW);
  digitalWrite(8,HIGH);
  digitalWrite(9,HIGH);
  digitalWrite(11,HIGH);
  digitalWrite(12,HIGH);  
}
void enjuague_en_lanza(){
  lcd.setCursor(0,0);
  lcd.print("   HIDRO AGUA   ");
  digitalWrite(11,LOW);
  digitalWrite(8,HIGH);
  digitalWrite(9,HIGH);
  digitalWrite(10,HIGH);
  digitalWrite(12,HIGH);
}
void cera_en_lanza(){
  lcd.setCursor(0,0);
  lcd.print("   HIDRO CERA    ");
  digitalWrite(12,LOW);
  digitalWrite(8,HIGH);
  digitalWrite(9,HIGH);
  digitalWrite(10,HIGH);
  digitalWrite(11,HIGH);
}

void coin() {
  if ((millis() - lastDebounceTime) > debounceDelay) {
    if(digitalRead(2)==0){
      delay(10);
      if(digitalRead(2)==0){
        credito++;
        lastDebounceTime = millis();
  }}}
}
void service() {
  if ((digitalRead(5) == LOW) && (digitalRead(6) == LOW)) {
    credito = 2;
  }
}
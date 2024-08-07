#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x3F,16,2);  //Change the HEX address

#include <Servo.h> 

Servo myservo1;

int IR1 = 2;
int IR2 = 4;

int Slot = 4;           //Enter Total number of parking Slots

int flag1 = 0;
int flag2 = 0;

int LED1 = 6; //green
int LED2 = 7; //red
int LED3 = 8; //white

void setup() {
  lcd.begin();
  lcd.backlight();
pinMode(IR1, INPUT);
pinMode(IR2, INPUT);
  
myservo1.attach(3);
myservo1.write(100);

lcd.setCursor (0,0);
lcd.print("      SMART   ");
lcd.setCursor (0,1);
lcd.print(" PARKING SYSTEM ");
delay (2000);
lcd.clear();
pinMode(LED1,OUTPUT);
pinMode(LED2,OUTPUT);
pinMode(LED3,OUTPUT);
digitalWrite(LED3,HIGH);
}

void loop(){ 

if(digitalRead (IR1) == LOW && flag1==0){
if(Slot>0){flag1=1;
if(flag2==0){myservo1.write(0); Slot = Slot-1;}
}else{
digitalWrite(LED1,LOW);
digitalWrite(LED2,HIGH);
lcd.setCursor (0,0);
lcd.print("    SORRY :(    ");  
lcd.setCursor (0,1);
lcd.print("  Parking Full  "); 
delay (3000);
lcd.clear(); 
}
}

if(digitalRead (IR2) == LOW && flag2==0){flag2=1;
if(flag1==0){myservo1.write(0); Slot = Slot+1;}
}

if(flag1==1 && flag2==1){
delay (500);
myservo1.write(100);
flag1=0, flag2=0;
}

lcd.setCursor (0,0);
lcd.print("    WELCOME!    ");
lcd.setCursor (0,1);
lcd.print("  Slot Left: ");
lcd.print(Slot);
delay(500);
digitalWrite(LED2,LOW);

digitalWrite(LED1,HIGH);

}

#include <ESP8266WiFi.h>                      //Librería de conexión WiFi del módulo ESP8266
#include <ESP8266WebServer.h>                 //Librería ESP8266WebServer (simplifica la creación del servidor)
#include <ESP8266HTTPClient.h>
#include "FS.h"                               //Librería del Sistema de Archivos para Memoria Flash (SPIFFS)
#include <Arduino_JSON.h> 
  
//add the servo library --------------------------------------------------------------------
#include <Servo.h>

//define our servos
Servo servo_leftRight;
Servo servo_upDown;

int x2;     
int y2;

static const uint8_t D1 = 5;
static const uint8_t D2 = 4;

int center_x = 115;
int center_y = 75;

int previous_x = center_x;
int previous_y = center_y;

int pos_x = center_x;
int pos_y = center_y;

int time2delay = 20;

//-------------------------------------------------------------------------------------------

const char *ssid = "BetancesRiverasHome";        // Credenciales del Punto de Acceso
const char *password = "ldbm4243444546474849";   
const char* serverName = "http://192.168.2.228:81/json/";


void setup() {
  
  // attaches our servos on pins D1 and D2 -----------------------------------------------
  servo_leftRight.attach(D1);
  servo_upDown.attach(D2);
 //-------------------------------------------------------------------------------------------

  Serial.begin(115200); // Inicialización del Puerto Serie
  
  servo_leftRight.write(center_x);  // colocar X en la posicion central
  servo_upDown.write(center_y);  // colocar Y en la posicion central

  
  //WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password); //Conectar a wifi local
 
  // Esperar a que nos conectemos 
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print("\nConnecting..");
 
  }
 
  // Mostrar mensaje de exito y dirección IP asignada
  Serial.println();
  Serial.print("Conectado a:\t");
  Serial.println(WiFi.SSID()); 
  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());

 
 //-------------------------------------------------------------------------------------------
}



//-------------------------------------------------------------------------------------------
String httpGETRequest(const char* serverName) {
  HTTPClient http;
    
  // Your IP address with path or Domain name with URL path 
  http.begin(serverName);
  
  // Send HTTP POST request
  int httpResponseCode = http.GET();
  
  String payload = "{}"; 
  
  if (httpResponseCode>0) {
    payload = http.getString();
  }
  else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
  // Free resources
  http.end();

  return payload;
}
//-------------------------------------------------------------------------------------------



void loop() {
      String outputsState = httpGETRequest(serverName);
      JSONVar myObject = JSON.parse(outputsState);
      int x = (int)myObject["dx"];   // Convierte los datos de tipo String a Int      
      int y = (int)myObject["dy"];

      if(outputsState != "{}"){
        //set the servo position---------------------------------------------------------------------
        x2 = map(x, 180, 0, 80, 150); 
        
        if (previous_x <= x2){
          for (pos_x = previous_x; pos_x <= x2; pos_x++) { 
                servo_leftRight.write(pos_x);
                delay(time2delay);      
           }
        }
        else if (previous_x >= x2){
          for (pos_x = previous_x; pos_x >= x2; pos_x--) { 
              servo_leftRight.write(pos_x);
              delay(time2delay);      
           }
        }
  //      // llevar el motor al punto medio de forma suave
  //      if ((previous_x <= (x2-2)) && (x2==center_x)){
  //        for (pos_x = previous_x; pos_x <= x2; pos_x++) { 
  //              servo_leftRight.write(pos_x);
  //              delay(time2delay);      
  //         }
  //      }
  //      else if ((previous_x >= (x2+2)) && (x2==center_x)){
  //        for (pos_x = previous_x; pos_x >= x2; pos_x--) { 
  //            servo_leftRight.write(pos_x);
  //            delay(time2delay);      
  //         }
  //      }
  //      else{servo_leftRight.write(x2);}
      
        y2 = map(y, 0, 180, 55, 95);
        
        // llevar el motor al punto medio de forma suave
        if (previous_y <= y2){
          for (pos_y = previous_y; pos_y <= y2; pos_y++) { 
                servo_upDown.write(pos_y);
                delay(time2delay);      
           }
        }
        else if (previous_y >= y2){
          for (pos_y = previous_y; pos_y >= y2; pos_y--) { 
              servo_upDown.write(pos_y);
              delay(20);      
           }
        }
        
  //      y2 = map(y, 0, 180, 45, 105);
  //      // llevar el motor al punto medio de forma suave
  //      if (previous_y <= y2-2 && y2==center_y){
  //        for (pos_y = previous_y; pos_y <= y2; pos_y++) { 
  //              servo_upDown.write(pos_y);
  //              delay(20);      
  //         }
  //      }
  //      else if (previous_y >= y2+2 && y2==center_y){
  //        for (pos_y = previous_y; pos_y >= y2; pos_y--) { 
  //            servo_upDown.write(pos_y);
  //            delay(20);      
  //         }
  //      }
  //      else{servo_upDown.write(y2);} 
  
          
        
        previous_x = x2;   
        previous_y = y2;
  //         
        Serial.print(x2); Serial.print("  "); Serial.println(y2); 
      }   
}


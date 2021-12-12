#include <ESP8266WiFi.h>

#include "DHT.h"


#define DHTPIN 4 //DHT pin
#define DHTTYPE DHT11 //DHT Type
#define RAINPIN 3 //Rain sensor pin

float t, h;
float tfinal,hfinal;
String rain, result,result2;

int port = 8888; //Port number
WiFiServer server(port);

//Server connect to WiFi Network
const char * ssid = "ezone2019_salon"; //Enter your wifi SSID
const char * password = "ezone2019"; //Enter your wifi Password

DHT dht(DHTPIN, DHTTYPE);

void setup() {
    pinMode(RAINPIN, INPUT);
    Serial.begin(9600);
    Serial.println();

    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password); //Connect to wifi

    // Wait for connection
    Serial.println("Connecting to Wifi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
        delay(500);
    }

    Serial.println("");
    Serial.print("Connected to ");
    Serial.println(ssid);

    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
    server.begin();
    Serial.print("Open Telnet and connect to IP:");
    Serial.print(WiFi.localIP());
    Serial.print(" on port ");
    Serial.println(port);
}

String returns(float t ,float h) {
    String result="";
   
    rain = "False";

    if (digitalRead(RAINPIN) == LOW) {
        Serial.println("Digital value : wet");
        rain = "true";
    } else {
        Serial.println("Digital value : dry");
        rain = "false";
    }
    
    result.concat((String)t);
    result.concat("/");
    result.concat((String)h);
    result.concat("/");
    result.concat(rain);
    return result;
}

void loop() {

    WiFiClient client = server.available();
    
    h = dht.readHumidity();
    t = dht.readTemperature();
    if( isnan(t) ||isnan(h)){
      //Serial.println("ERROR !! check cables");
      result2 = "error";
    }
    else {
      tfinal = t;
      hfinal = h;
    }
    
    
      
      
      if (client) {
        if (client.connected()) {
            Serial.println("Client Connected");
            result = returns(tfinal,hfinal);
            
            if (result2 == "error") {
                Serial.println("ERROR !! check cables");
                client.print(result2);
             
            } else {
                Serial.println(result);
                client.print(result);
            }
        }

        client.stop();
        Serial.println("Client disconnected");
    }
}

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#define LEDOPENCOMMAND "AT+LEDO"
#define LEDCLOSECOMMAND "AT+LEDC"
#define FANOPENCOMMAND "AT+FANO"
#define FANCLOSECOMMAND "AT+FANC"
#define TESTCOMMANDLENGTH 7

const char* ssid = "";                   // wifi ssid
const char* password =  "";         // wifi password
const char* mqttServer = "";    // IP adress Raspberry Pi
const int mqttPort = 1883;
const char* mqttUser = "pi";      // if you don't have MQTT Username, no need input
const char* mqttPassword = "pipass";  // if you don't have MQTT Password, no need input

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {

  Serial.begin(115200);
  
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");

  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);

  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");

    if (client.connect("ESP8266Client", mqttUser, mqttPassword )) {

      Serial.println("connected");

    } else {

      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);

    }
  }

//  client.publish("esp8266", "Hello Raspberry Pi");
//  client.subscribe("esp8266");

}

bool str_cmp(char s1[TESTCOMMANDLENGTH],char s2[TESTCOMMANDLENGTH])
{
  bool is_similar = true;
  for (int i=0;i<TESTCOMMANDLENGTH;i++)
  {
    if(s1[i] != s2[i])
    {
      is_similar = false;
    }
  }
  return is_similar;
}

void callback(char* topic, byte* payload, unsigned int length) {
  char metin[TESTCOMMANDLENGTH];
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);

  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
    if(i<TESTCOMMANDLENGTH)
    metin[i]=(char)payload[i];
  }
  Serial.print("metin:");
  Serial.println(metin);

  if(str_cmp(metin,LEDOPENCOMMAND))
  {
  Serial.println("Isik Acma kodu");
  }
  else if(str_cmp(metin,LEDCLOSECOMMAND))
  {
  Serial.println("Isik Kapama kodu");
  }
  Serial.println();
  Serial.println("-----------------------");

}
void loop() {
    //client.publish("esp8266", "Hello Raspberry Pi");
    client.subscribe("esp8266");
    delay(300);
    client.loop();
}

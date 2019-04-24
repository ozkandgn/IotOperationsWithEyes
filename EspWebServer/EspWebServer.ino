#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <Servo.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x3f, 16, 2);

#ifndef Wifi_Name
#define Wifi_Name "Connectify-tez"
#define Wifi_Pass  "[Wifi Şifre]"
#endif

#define KullaniciAdi "[Kullanici Adi]"
#define KullaniciSifre "[Kullanici Şifre]"

const char* ssid = Wifi_Name;
const char* password = Wifi_Pass;
String kullaniciadi = "";


//GPIO Çıkış durumları için
String Indoor_Lighting_State = "off";
String Night_Light_State = "off";
String PerdeState   = "off";
String Channel = "";

// GPIO pinleri tanımlandı.
const int Indoor_Lighting_Pin = 14;
const int Night_Light_Pin = 0;
const int servoPin = 2;

ESP8266WebServer server(80);
Servo servo;
int servoAngle = 0;

//Doğrulama yapıldığında...
bool is_authenticated() {
  Serial.println("Enter is_authenticated");
  if (server.hasHeader("Cookie")) {
    Serial.print("Found cookie: ");
    String cookie = server.header("Cookie");
    Serial.println(cookie);
    if (cookie.indexOf("ESPSESSIONID=1") != -1) {
      Serial.println("Authentication Successful");
      return true;
    }
  }
  Serial.println("Authentication Failed");
  return false;
}
//Çıkış yapıldığında
void handleLogin() {
  String msg;
  if (server.hasHeader("Cookie")) {
    Serial.print("Found cookie: ");
    String cookie = server.header("Cookie");
    Serial.println(cookie);
  }
  if (server.hasArg("DISCONNECT")) {
    Serial.println("Disconnection");
    server.sendHeader("Location", "/login");
    server.sendHeader("Cache-Control", "no-cache");
    server.sendHeader("Set-Cookie", "ESPSESSIONID=0");
    server.send(301);
    return;
  }
  if (server.hasArg("USERNAME") && server.hasArg("PASSWORD")) {
    kullaniciadi = server.arg("USERNAME");
    if (server.arg("USERNAME") == KullaniciAdi &&  server.arg("PASSWORD") == KullaniciSifre) {
      server.sendHeader("Location", "/");
      server.sendHeader("Cache-Control", "no-cache");
      server.sendHeader("Set-Cookie", "ESPSESSIONID=1");
      server.send(301);
      Serial.println("Log in Successful");
      return;
    }
    msg = "Wrong username/password! try again.";
    Serial.println("Log in Failed");
  }

  msg = "Wrong username/password! try again.";
  String content = "<meta http-equiv=Content-Type";
  content += "text/html charset=utf-8 />";
  content += "<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}";
  content += ".buttongiris { background-color: darkgreen; border: none; color: black; padding: 1px 92px;";
  content += "text-decoration: none; font-size: 20px; margin: -9px; cursor: pointer;}";
  content += "</style></head>";
  content += "<html><body><form action='/login' method='POST'>Lütfen Giriş Yapınız!<br>";
  content += "Kullanıcı Adı &nbsp:<input type='text' name='USERNAME' placeholder='Kullanıcı Adı'><br>";
  content += "Kullanıcı Şifre:<input type='password' name='PASSWORD' placeholder='Kullanıcı Şifre'><br>";
  content += "<p><button class=\"buttongiris\">Giriş yap</button></p>";
  content += "Tez hakkında bilgi almak için: <a href='/inline'>Buraya Tıklayınız.</a></body></html>";
  server.send(200, "text/html", content);
}

//Giriş sayfası
void handleRoot() {
  Serial.println("Enter handleRoot");
  String header;
  if (!is_authenticated()) {
    server.sendHeader("Location", "/login");
    server.sendHeader("Cache-Control", "no-cache");
    server.send(301);
    return;
  }
  String content = "<meta http-equiv=Content-Type";
  content += "text/html charset=utf-8 />";
  content += "<html><body><H2>AnaSayfa</H2> ";
  if (server.hasHeader("User-Agent")) {
    content += "Giriş Başarılı   ";
    content += "<p>Hoş Geldin " + kullaniciadi + "</p>";

    content += "<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}";
    content += ".button { background-color: #195B6A; border: none; color: white; padding: 16px 40px;";
    content += "text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}";
    content += ".button2 {background-color: #77878A;}</style></head>";
    content += "<h1>ESP8266 Web Server</h1>";

    String pin14durumu = "Kapalı";
    if (Indoor_Lighting_State == "on")
      pin14durumu = "Açık";
    content += "<p>Oda Işığı - Durumu " + pin14durumu + "</p>";

    if (!digitalRead(Indoor_Lighting_Pin))
    {
      content += "<p><a href=\"/14/on\"><button class=\"button\">Aç</button></a></p>";
    }
    else
    {
      content += "<p><a href=\"/14/off\"><button class=\"button button2\">Kapat</button></a></p>";
    }

    String pin0durumu = "Kapalı";
    if (Night_Light_State == "on")
      pin0durumu = "Açık";
    content += "<p>Gece Lambası - Durumu " + pin0durumu + "</p>";

    if (!digitalRead(Night_Light_Pin))
    {
      content += "<p><a href=\"/0/on\"><button class=\"button\">Aç</button></a></p>";
    }
    else
    {
      content += "<p><a href=\"/0/off\"><button class=\"button button2\">Kapat</button></a></p>";
    }

    String pin2durumu = "Kapalı";
    if (PerdeState == "on")
      pin2durumu = "Açık";
    content += "<p>Perde - Durumu " + pin2durumu + "</p>";

    if (!(PerdeState == "on"))
    {
      content += "<p><a href=\"/2/on\"><button class=\"button\">Aç</button></a></p>";
    }
    else
    {
      content += "<p><a href=\"/2/off\"><button class=\"button button2\">Kapat</button></a></p>";
    }


    String channelstate = "Yok";
    if (Channel == "Kanal 1")
      channelstate = "Kanal 1";
    else if (Channel == "Kanal 2")
      channelstate = "Kanal 2";
    content += "<p>Açık Kanal - " + channelstate + "</p>";

    if (!(Channel == "Kanal 1"))
    {
      content += "<p><a href=\"/3/kanal1\"><button class=\"button\">Kanal1</button></a></p>";
    } 
    else
    {
      content += "<p><a href=\"/3/kanal2\"><button class=\"button button2\">Kanal2</button></a></p>";
    }
    if ((Channel == "Kanal 1")or(Channel == "Kanal 2"))
    {
      content += "<p><a href=\"/3/kapat\"><button class=\"button\">Kapat</button></a></p>";
    }


    content += "Çıkış yapmak için: <a href=\"/login?DISCONNECT=YES\">Çıkış Yap</a></body></html>";
    server.send(200, "text/html", content);
  }

  server.send(200, "text/html", content);
}

//Authentication istenmediği durumlar
void handleNotFound() {
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET) ? "GET" : "POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i = 0; i < server.args(); i++) {
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  if (server.uri() == "/14/on")
  {
    if (server.hasHeader("User-Agent"))
    {

      Indoor_Lighting_State = "on";
      //server.send(200,"text/plain","1");
      server.uri() = "";
      digitalWrite(Indoor_Lighting_Pin, HIGH);
      handleRoot();

    }
    else
      server.send(404, "text/plain", message);
  }
  if (server.uri() == "/14/off")
  {
    if (server.hasHeader("User-Agent"))
    {
      Indoor_Lighting_State = "off";
      //server.send(200,"text/plain","0");
      server.uri() = "";
      digitalWrite(Indoor_Lighting_Pin, LOW);
      handleRoot();
    }
    else
      server.send(404, "text/plain", message);
  }
  if (server.uri() == "/14")
  {
    if (server.hasHeader("User-Agent"))
    {
      Indoor_Lighting_State = digitalRead(Indoor_Lighting_Pin);
      server.send(200, "text/plain", Indoor_Lighting_State);
    }
    else
      server.send(404, "text/plain", message);
  }
  if (server.uri() == "/0/on")
  {
    if (server.hasHeader("User-Agent"))
    {

      Night_Light_State = "on";
      //server.send(200,"text/plain","1");
      server.uri() = "";
      digitalWrite(Night_Light_Pin, HIGH);
      handleRoot();

    }
    else
      server.send(404, "text/plain", message);
  }
  if (server.uri() == "/0/off")
  {
    if (server.hasHeader("User-Agent"))
    {
      Night_Light_State = "off";
      //server.send(200,"text/plain","0");
      server.uri() = "";
      digitalWrite(Night_Light_Pin, LOW);
      handleRoot();
    }
    else
      server.send(404, "text/plain", message);
  }
  if (server.uri() == "/0")
  {
    if (server.hasHeader("User-Agent"))
    {
      Night_Light_State = digitalRead(Night_Light_Pin);
      server.send(200, "text/plain", Night_Light_State);
    }
    else
      server.send(404, "text/plain", message);
  }
  if (server.uri() == "/2/on")
  {
    if (server.hasHeader("User-Agent"))
    {

      PerdeState = "on";
      //server.send(200,"text/plain","1");
      server.uri() = "";
      servo.write(0);
      delay(2000);
      servo.write(90);
      handleRoot();

    }
    else
      server.send(404, "text/plain", message);
  }
  if (server.uri() == "/2/off")
  {
    if (server.hasHeader("User-Agent"))
    {
      PerdeState = "off";
      //server.send(200,"text/plain","0");
      server.uri() = "";
      servo.write(180);
      delay(2000);
      servo.write(90);
      handleRoot();
    }
    else
      server.send(404, "text/plain", message);
  }
  if (server.uri() == "/2")
  {
    if (server.hasHeader("User-Agent"))
    {
      if (PerdeState == "on")
        server.send(200, "text/plain", "1");
      if (PerdeState == "off")
        server.send(200, "text/plain", "0");
    }
    else
      server.send(404, "text/plain", message);
  }
  if (server.uri() == "/3/kanal1")
  {
    if (server.hasHeader("User-Agent"))
    {
      Channel = "Kanal 1";
      //server.send(200,"text/plain","0");
      server.uri() = "";
      lcd.setCursor(0, 0);
      lcd.print(Channel);
      lcd.setCursor(0, 1);
      lcd.print("Engin Ozan Ozkan");
      handleRoot();
    }
    else
      server.send(404, "text/plain", message);
  }
  if (server.uri() == "/3/kanal2")
  {
    if (server.hasHeader("User-Agent"))
    {
      Channel = "Kanal 2";
      //server.send(200,"text/plain","0");
      server.uri() = "";
      lcd.setCursor(0, 0);
      lcd.print(Channel);
      lcd.setCursor(0, 1);
      lcd.print("Engin Ozan Ozkan");
      handleRoot();
    }
    else
      server.send(404, "text/plain", message);
  }
  if (server.uri() == "/3/kapat")
  {
    if (server.hasHeader("User-Agent"))
    {
      Channel = "           ";
      //server.send(200,"text/plain","0");
      server.uri() = "";
      lcd.setCursor(0, 0);
      lcd.print(Channel);
      lcd.setCursor(0, 1);
      lcd.print("                ");
      handleRoot();
    }
    else
      server.send(404, "text/plain", message);
  }
   if (server.uri() == "/3")
  {
    if (server.hasHeader("User-Agent"))
    {
      if (Channel == "Kanal 2")
        server.send(200, "text/plain", "2");
      else if (Channel == "Kanal 1")
        server.send(200, "text/plain", "1");
      else
      server.send(200, "text/plain", "0");
    }
    else
      server.send(404, "text/plain", message);
  }
  else
    server.send(404, "text/plain", message);
}

void setup(void) {
  Serial.begin(115200);
  lcd.begin();
  lcd.backlight();
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");
  servo.attach(servoPin);
  //servo.write(0);
  pinMode(Indoor_Lighting_Pin, OUTPUT);
  pinMode(Night_Light_Pin, OUTPUT);

  digitalWrite(Indoor_Lighting_Pin, LOW);
  digitalWrite(Night_Light_Pin, LOW);

  // Bağlantı beklenir
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());


  server.on("/", handleRoot);
  server.on("/login", handleLogin);
  server.on("/inline", []() {
    server.send(200, "text/plain", "Tez hakkinda bilgi verilecektir.");
  });

  server.onNotFound(handleNotFound);

  const char * headerkeys[] = {"User-Agent", "Cookie"} ;
  size_t headerkeyssize = sizeof(headerkeys) / sizeof(char*);

  server.collectHeaders(headerkeys, headerkeyssize);
  server.begin();
  Serial.println("HTTP server started");



}

void loop(void) {
  server.handleClient();
}

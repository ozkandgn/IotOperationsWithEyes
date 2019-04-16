#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

#ifndef Wifi_Name
#define Wifi_Name "Connectify-tez"
#define Wifi_Pass  "[pass]"
#endif

#define KullaniciAdi "[kullanıcı adı]"
#define KullaniciSifre "[şifre]"

const char* ssid = Wifi_Name;
const char* password = Wifi_Pass;
String kullaniciadi="";


//GPIO Çıkış durumları için
String output5State = "off";
String output4State = "off";

// GPIO pinleri tanımlandı.
const int output5 = 5;
const int output4 = 4;

ESP8266WebServer server(80);

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
    kullaniciadi=server.arg("USERNAME");
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
  String content="<meta http-equiv=Content-Type";
  content+="text/html charset=utf-8 />";
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
  String content="<meta http-equiv=Content-Type";
  content+="text/html charset=utf-8 />";
  content += "<html><body><H2>AnaSayfa</H2><br>";
  if (server.hasHeader("User-Agent")) {
    content += "Giriş Başarılı" "<br><br>";
    content += "<p>Hoş Geldin " + kullaniciadi + "</p>";
  
  content += "<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}";
  content += ".button { background-color: #195B6A; border: none; color: white; padding: 16px 40px;";
  content += "text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}";
  content += ".button2 {background-color: #77878A;}</style></head>";
  content += "<body><h1>ESP8266 Web Server</h1>";
  String pin5durumu="Kapalı";
  if(output5State=="on")
  pin5durumu="Açık";
  content += "<p>Işık 5 - Durumu " + pin5durumu + "</p>";
  if (!digitalRead(5)) {
     content +="<p><a href=\"/5/on\"><button class=\"button\">Aç</button></a></p>";
            } else {
           content +="<p><a href=\"/5/off\"><button class=\"button button2\">Kapat</button></a></p>";
            } 
   String pin4durumu="Kapalı";
  if(output4State=="on")
  pin4durumu="Açık";
  content += "<p>Işık 4 - Durumu " + pin4durumu + "</p>";
  if (!digitalRead(4)) {
     content +="<p><a href=\"/4/on\"><button class=\"button\">Aç</button></a></p>";
            } else {
           content +="<p><a href=\"/4/off\"><button class=\"button button2\">Kapat</button></a></p>";
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
  if(server.uri()=="/5/on")
  {
    if (server.hasHeader("User-Agent"))
    {
    
    output5State="on";
    //server.send(200,"text/plain","1");
    server.uri()="";
    digitalWrite(output5, HIGH);
    handleRoot();
    
    }
    else
    server.send(404, "text/plain", message);
  }
    if(server.uri()=="/5/off")
  {
    if (server.hasHeader("User-Agent"))
    {
    output5State="off";
    //server.send(200,"text/plain","0");
    server.uri()="";
    digitalWrite(output5, LOW);
    handleRoot();
    }
    else
    server.send(404, "text/plain", message);
  }
  if(server.uri()=="/5")
  {
    if (server.hasHeader("User-Agent"))
    {
    output5State=digitalRead(5);
    server.send(200,"text/plain",output5State);
    }
    else
    server.send(404, "text/plain", message);
  }
  if(server.uri()=="/4/on")
  {
    if (server.hasHeader("User-Agent"))
    {
    
    output4State="on";
    //server.send(200,"text/plain","1");
    server.uri()="";
    digitalWrite(output4, HIGH);
    handleRoot();
    
    }
    else
    server.send(404, "text/plain", message);
  }
   if(server.uri()=="/4/off")
  {
    if (server.hasHeader("User-Agent"))
    {
    output4State="off";
    //server.send(200,"text/plain","0");
    server.uri()="";
    digitalWrite(output4, LOW);
    handleRoot();
    }
    else
    server.send(404, "text/plain", message);
  }
  if(server.uri()=="/4")
  {
    if (server.hasHeader("User-Agent"))
    {
    output4State=digitalRead(4);
    server.send(200,"text/plain",output4State);
    }
    else
    server.send(404, "text/plain", message);
  }
  else
  server.send(404, "text/plain", message);
}

void setup(void) {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");
  pinMode(output5, OUTPUT);
  pinMode(output4, OUTPUT);
 
  digitalWrite(output5, LOW);
  digitalWrite(output4, LOW);

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

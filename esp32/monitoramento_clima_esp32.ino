#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <DHT.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>
#include <ArduinoJson.h>

#define DHTPIN 4
#define DHTTYPE DHT22
#define PINO_CHUVA 34
#define PINO_LDR 35

const char* ssid = "SEU_WIFI";
const char* password = "SENHA_WIFI";
const char* serverUrl = "http://IP_DO_PC:8000/api/clima/leituras";
const char* codigoDispositivo = "ESP-CLIMA-01";

DHT dht(DHTPIN, DHTTYPE);
Adafruit_BMP280 bmp;

void conectarWiFi() {
  Serial.print("Conectando ao Wi-Fi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi conectado");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
}

void setup() {
  Serial.begin(115200);
  dht.begin();
  Wire.begin(21, 22);

  if (!bmp.begin(0x76)) {
    Serial.println("BMP280 não encontrado. Verifique a ligação SDA/SCL.");
  }

  conectarWiFi();
}

void loop() {
  float temperatura = dht.readTemperature();
  float umidade = dht.readHumidity();
  float pressao = bmp.readPressure() / 100.0F;
  int chuvaBruta = analogRead(PINO_CHUVA);
  int ldrBruto = analogRead(PINO_LDR);

  if (isnan(temperatura) || isnan(umidade)) {
    Serial.println("Falha ao ler DHT22.");
    delay(5000);
    return;
  }

  float chuvaPercentual = map(chuvaBruta, 4095, 0, 0, 100);
  float luminosidadePercentual = map(ldrBruto, 0, 4095, 0, 100);

  StaticJsonDocument<256> doc;
  doc["codigo_dispositivo"] = codigoDispositivo;
  doc["temperatura"] = temperatura;
  doc["umidade"] = umidade;
  doc["pressao"] = pressao;
  doc["chuva"] = chuvaPercentual;
  doc["luminosidade"] = luminosidadePercentual;

  String payload;
  serializeJson(doc, payload);

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    int httpCode = http.POST(payload);
    Serial.println("Enviando JSON:");
    Serial.println(payload);
    Serial.print("Resposta HTTP: ");
    Serial.println(httpCode);

    if (httpCode > 0) {
      Serial.println(http.getString());
    }

    http.end();
  } else {
    conectarWiFi();
  }

  delay(10000);
}
